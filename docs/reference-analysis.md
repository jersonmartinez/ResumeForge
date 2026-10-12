# Reference analysis

The repository contains four user-supplied references:

- English PDF and DOCX.
- Spanish PDF and DOCX.

The PDFs are the visual source of truth. The DOCX files are useful for confirming editable text structure and section boundaries.

## Observations

- Both PDFs render on A4 pages and contain two pages.
- The body uses a single-column layout with compact but readable spacing.
- The header has two columns: name, title, and specialization on the left; phone, email, LinkedIn, and website on the right.
- The name and professional headline have strong typographic emphasis.
- A purple horizontal divider separates the header from the summary.
- Hyperlinks are blue and visibly interactive.
- Section headings are uppercase and visually distinct.
- Experience entries use a bold role, a bold company line, italic dates, and nested bullet points.
- Skills are grouped by category, with category names in bold.
- Education and certifications appear after the skills section.
- The English and Spanish versions preserve the same content hierarchy while translating narrative content and section labels.
- The visual density is intentionally high enough to fit a substantial professional history in two pages.

## Initial template implications

- Use A4 geometry and a two-page target for the synthetic example.
- Use XeLaTeX with `fontspec` and `polyglossia` so accented Spanish text is handled as Unicode.
- Keep the first template single-column rather than introducing a sidebar that would make profile filtering harder.
- Represent job entries, skills, education, and certifications as structured YAML collections.
- Keep summaries and other long narrative fields in Markdown so an agent can revise them without editing LaTeX.
- Preserve links as structured fields and render them with `hyperref`.
- Add page-count validation because content selection can change pagination.

The exact font size, line height, and margins will be tuned after the first Dockerized LaTeX render is compared with the supplied PDFs.
