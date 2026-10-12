from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import fitz
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "resume.yml"
PROFILES_PATH = ROOT / "profiles"
TEMPLATE_PATH = ROOT / "templates"
OUTPUT_PATH = ROOT / "output"
BUILD_PATH = ROOT / ".resume-build"
LANGUAGES = {"en": "english", "es": "spanish"}
LABELS = {
    "en": {
        "experience": "Experience",
        "skills": "Skills",
        "education": "Education",
        "certifications": "Certifications",
    },
    "es": {
        "experience": "Experiencia",
        "skills": "Habilidades",
        "education": "Educación",
        "certifications": "Certificaciones",
    },
}


class ResumeError(Exception):
    """Raised for actionable input or rendering errors."""


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as file:
            value = yaml.safe_load(file)
    except FileNotFoundError as exc:
        raise ResumeError(f"Missing configuration file: {path}") from exc
    except yaml.YAMLError as exc:
        raise ResumeError(f"Invalid YAML in {path}: {exc}") from exc

    if not isinstance(value, dict):
        raise ResumeError(f"Expected a YAML mapping in {path}")
    return value


def localized(value: Any, language: str) -> Any:
    if isinstance(value, dict) and language in value:
        return value[language]
    return value


def latex_escape(value: Any) -> str:
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(character, character) for character in text)


def url_escape(value: Any) -> str:
    return str(value).replace("%", "%25").replace("#", "%23").replace(" ", "%20")


def validate_model(data: dict[str, Any], profile: dict[str, Any], language: str) -> None:
    required_data = {"personal", "experience", "skills", "education", "certifications"}
    missing = required_data - data.keys()
    if missing:
        raise ResumeError(f"Missing data sections: {', '.join(sorted(missing))}")

    personal = data["personal"]
    for field in ("name", "headline", "phone", "location", "email", "linkedin", "website"):
        if localized(personal.get(field), language) in (None, ""):
            raise ResumeError(f"Missing personal.{field} for language '{language}'")

    experience_by_id = {item.get("id"): item for item in data["experience"]}
    included_experience = profile.get("include", {}).get("experience", [])
    missing_experience = set(included_experience) - experience_by_id.keys()
    if missing_experience:
        raise ResumeError(f"Profile references unknown experience IDs: {', '.join(sorted(missing_experience))}")

    skill_names = {localized(item.get("name"), "en") for item in data["skills"]}
    included_skills = profile.get("include", {}).get("skills", [])
    missing_skills = set(included_skills) - skill_names
    if missing_skills:
        raise ResumeError(f"Profile references unknown skill names: {', '.join(sorted(missing_skills))}")

    summary_path = ROOT / localized(profile.get("summary"), language)
    if not summary_path.is_file():
        raise ResumeError(f"Missing summary file for language '{language}': {summary_path}")


def build_context(data: dict[str, Any], profile: dict[str, Any], language: str) -> dict[str, Any]:
    included_experience = profile["include"]["experience"]
    experience_by_id = {item["id"]: item for item in data["experience"]}
    experience = []
    for item_id in included_experience:
        item = experience_by_id[item_id].copy()
        item["title"] = localized(item["title"], language)
        item["dates"] = localized(item["dates"], language)
        item["bullets"] = [localized(bullet, language) for bullet in item["bullets"][language]]
        experience.append(item)

    included_skills = profile["include"]["skills"]
    skills_by_name = {item["name"]["en"]: item for item in data["skills"]}
    skills = []
    for skill_name in included_skills:
        item = skills_by_name[skill_name].copy()
        item["name"] = localized(item["name"], language)
        item["values"] = localized(item["values"], language)
        skills.append(item)

    education = []
    for item in data["education"]:
        localized_item = item.copy()
        localized_item["title"] = localized(item["title"], language)
        localized_item["dates"] = localized(item["dates"], language)
        education.append(localized_item)

    personal = data["personal"].copy()
    personal["headline"] = localized(personal["headline"], language)
    summary_path = ROOT / localized(profile["summary"], language)
    summary = summary_path.read_text(encoding="utf-8").strip()

    return {
        "personal": personal,
        "summary": summary,
        "experience": experience,
        "skills": skills,
        "education": education,
        "certifications": data["certifications"],
        "labels": LABELS[language],
        "language": language,
        "latex_language": LANGUAGES[language],
    }


def load_profile(name: str) -> dict[str, Any]:
    profile = load_yaml(PROFILES_PATH / f"{name}.yml")
    if profile.get("name") != name:
        raise ResumeError(f"Profile name does not match its filename: {name}")
    return profile


def render(data: dict[str, Any], profile: dict[str, Any], language: str) -> Path:
    validate_model(data, profile, language)
    context = build_context(data, profile, language)
    environment = Environment(
        loader=FileSystemLoader(TEMPLATE_PATH),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        variable_start_string="<<",
        variable_end_string=">>",
        block_start_string="[%",
        block_end_string="%]",
        comment_start_string="[!",
        comment_end_string="!]",
    )
    environment.filters["latex"] = latex_escape
    environment.filters["url"] = url_escape
    template = environment.get_template("professional/resume.tex.j2")

    build_dir = BUILD_PATH / f"{profile['name']}-{language}"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True)
    tex_path = build_dir / "resume.tex"
    tex_path.write_text(template.render(**context), encoding="utf-8")

    command = [
        "xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        "resume.tex",
    ]
    for _ in range(2):
        result = subprocess.run(command, cwd=build_dir, capture_output=True, text=True, check=False)
        if result.returncode:
            log = (result.stdout + "\n" + result.stderr)[-5000:]
            raise ResumeError(f"XeLaTeX failed for {profile['name']} ({language}):\n{log}")

    pdf_path = build_dir / "resume.pdf"
    if not pdf_path.is_file():
        raise ResumeError(f"XeLaTeX did not produce {pdf_path}")

    page_count = len(fitz.open(pdf_path))
    if not 1 <= page_count <= 3:
        raise ResumeError(f"Generated PDF has {page_count} pages; expected between 1 and 3")

    OUTPUT_PATH.mkdir(exist_ok=True)
    output_path = OUTPUT_PATH / f"{profile['name']}-{language}.pdf"
    shutil.copy2(pdf_path, output_path)
    print(f"Generated {output_path.relative_to(ROOT)} ({page_count} pages)")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and build ResumeForge profiles")
    parser.add_argument("command", choices=("validate", "build"))
    parser.add_argument("--profile", help="Profile name, such as example")
    parser.add_argument("--language", choices=sorted(LANGUAGES), help="Language to render")
    parser.add_argument("--all", action="store_true", help="Render every supported language")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.profile and not args.all:
        raise ResumeError("Provide --profile NAME or use --all")
    if args.profile and args.all:
        raise ResumeError("Use either --profile NAME or --all, not both")

    data = load_yaml(DATA_PATH)
    profile_names = [args.profile] if args.profile else sorted(path.stem for path in PROFILES_PATH.glob("*.yml"))
    languages = [args.language] if args.language else sorted(LANGUAGES)

    for profile_name in profile_names:
        profile = load_profile(profile_name)
        for language in languages:
            validate_model(data, profile, language)
            print(f"Validated profile '{profile_name}' ({language})")
            if args.command == "build":
                render(data, profile, language)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ResumeError as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
