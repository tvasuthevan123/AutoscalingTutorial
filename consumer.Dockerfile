FROM ghcr.io/astral-sh/uv:python3.12-alpine

COPY src/ src/
COPY pyproject.toml pyproject.toml
COPY .python-version .python-version
COPY uv.lock uv.lock
COPY README.md README.md
RUN uv sync
CMD ["uv", "run", "src/autoscalingtutorial/consumer.py"]
