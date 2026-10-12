FROM texlive/texlive:latest-small@sha256:956ab3808fc77b0057c0f8b6db5329642b8db7a33492460b9891862b72334f3c

RUN apt-get update \
    && apt-get install --no-install-recommends -y python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY requirements.txt /workspace/requirements.txt
RUN python3 -m pip install --break-system-packages --no-cache-dir -r /workspace/requirements.txt

ENTRYPOINT ["python3", "scripts/resume.py"]
