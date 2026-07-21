"""
generate_envs.py
----------------
Generates environment.yaml from pyproject.toml.

Usage:
    python scripts/generate_envs.py

Both output files are placed at the repository root and are compatible
with conda-lock:
    conda-lock lock -f environment.yaml -p win-64 -p linux-64
"""

import tomllib
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration — edit here if project conventions change
# ---------------------------------------------------------------------------

CHANNELS = [
    "openalea3",
    "conda-forge"
]

REPO_ROOT = Path(__file__).parent.parent.resolve()
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
ENV_DEV_PATH = REPO_ROOT / "conda/environment.yaml"


# ---------------------------------------------------------------------------
# TOML parsing helpers
# ---------------------------------------------------------------------------

def load_pyproject(path: Path) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def get_python_version(pyproject: dict) -> str:
    """
    Extracts the lower bound from requires-python and returns a conda
    version string. e.g. '>=3.12' -> 'python >=3.12'
    """
    requires_python = pyproject.get("project", {}).get("requires-python", "")
    if not requires_python:
        return "python"
    return f"python {requires_python}"


def get_pip_deps(pyproject: dict) -> list[str]:
    """Runtime deps declared in [project.dependencies] (pip-installable)."""
    return pyproject.get("project", {}).get("dependencies", [])


def get_conda_deps(pyproject: dict) -> list[str]:
    """Conda-only deps declared in [tool.conda.environment.dependencies]."""
    return (
        pyproject
        .get("tool", {})
        .get("conda", {})
        .get("environment", {})
        .get("dependencies", [])
    )


def get_dev_deps(pyproject: dict) -> list[str]:
    """Dev deps declared in [project.optional-dependencies.dev]."""
    return (
        pyproject
        .get("project", {})
        .get("optional-dependencies", {})
        .get("dev", [])
    )


# ---------------------------------------------------------------------------
# YAML serialisation (stdlib only — no PyYAML)
# ---------------------------------------------------------------------------

def _indent(lines: list[str], level: int = 1) -> list[str]:
    prefix = "  " * level
    return [f"{prefix}{line}" for line in lines]


def _yaml_list(items: list[str], indent: int = 1) -> list[str]:
    return _indent([f"- {item}" for item in items], level=indent)


def render_env(
    name: str,
    channels: list[str],
    conda_deps: list[str],
    pip_deps: list[str],
    editable_install: bool = False
) -> str:
    """
    Renders a conda environment YAML string.

    conda_deps  : packages resolved by conda
    pip_deps    : packages resolved by pip (listed under pip: subsection)
    editable_install : if True, adds '-e .' to the pip subsection
    """
    lines = []

    lines.append(f"name: {name}")
    lines.append("")

    lines.append("channels:")
    lines.extend(_yaml_list(channels, indent=1))
    lines.append("")

    lines.append("dependencies:")
    lines.extend(_yaml_list(conda_deps, indent=1))

    if pip_deps or editable_install:
        lines.append("  - pip:")
        pip_entries = list(pip_deps)
        if editable_install:
            pip_entries.append("-e .. --config-settings editable_mode=compat")
        lines.extend(_yaml_list(pip_entries, indent=2))

    lines.append("")  # trailing newline
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    pyproject = load_pyproject(PYPROJECT_PATH)
    project_name = pyproject.get("project", {}).get("name", "project").split(".")[-1]

    python_version   = get_python_version(pyproject)
    pip_deps         = get_pip_deps(pyproject)
    conda_only_deps  = get_conda_deps(pyproject)
    dev_deps         = get_dev_deps(pyproject)


    # --- environment.yaml (runtime + dev, editable install) ------------
    # pip deps: runtime pip deps + dev-only pip deps
    # editable install added so contributors get the local package
    dev_pip_deps = pip_deps + dev_deps
    env_dev_conda_deps = [python_version, "pip"] + conda_only_deps
    env_dev_content = render_env(
        name=f"{project_name}",
        channels=CHANNELS,
        conda_deps=env_dev_conda_deps,
        pip_deps=dev_pip_deps,
        editable_install=True,
    )
    ENV_DEV_PATH.write_text(env_dev_content, encoding="utf-8")


if __name__ == "__main__":
    main()