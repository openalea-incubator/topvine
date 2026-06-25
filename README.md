# Overview

`topvine` is a 3D statistical reconstruction model of grapevine (*Vitis vinifera* L.)
that simulates canopy structure accounting for (cultivar)-(training system) pairs.

# Development Environment Setup
## Prerequisites

The following tools must be installed and available in your shell before using the Makefile.

### 1. Conda

Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution). Verify with:

```bash
conda --version
```

### 2. conda-lock

Install `conda-lock` in your **base** conda environment (not in a project environment):

```bash
conda install -c conda-forge conda-lock
```

Verify with:

```bash
conda-lock --version
```

### 3. make

**Linux** — likely already installed. Verify with `make --version`. If not:

```bash
sudo apt install make        # Debian/Ubuntu
sudo dnf install make        # RHEL/Fedora
```

**Windows (PowerShell, run as administrator)** — install via winget:

```powershell
winget install GnuWin32.Make
```

Then add GnuWin32 to the system PATH (run as administrator):

```powershell
[Environment]::SetEnvironmentVariable(
    "Path",
    $env:Path + ";C:\Program Files (x86)\GnuWin32\bin",
    "Machine"
)
```

Restart your terminal and verify with `make --version`.

---

## Clone Project
Clone the repo into local machine; go to the directory where you would like to have the `topvine` code cloned then type
(replace `<topvine-parent-directory>` by your directory name):
```bash
cd <topvine-parent-directory>
git clone git@github.com:openalea-incubator/topvine.git
```

The dependency management workflow is driven by the following files:

```
project-root/
├── Makefile                        ← entry point for all environment commands
├── pyproject.toml                  ← single source of truth for all dependencies
├── scripts/
│   └── generate_env_specs.py            ← generates environment.yaml from pyproject.toml
└── conda/
    ├── meta.yaml                   ← conda-build recipe, reads from pyproject.toml
    ├── environment.yaml        ← generated, do not edit manually
    └── conda-lock.yml          ← committed to repo, used for reproducible installs
```

### Dependency ownership

| What | Where |
|---|---|
| Runtime pip-installable deps | `[project.dependencies]` in `pyproject.toml` |
| Conda-only runtime deps | `[tool.conda.environment.dependencies]` in `pyproject.toml` |
| Dev/contributor deps | `[project.optional-dependencies.dev]` in `pyproject.toml` |
| Conda channels | hardcoded in `scripts/generate_envs.py` |
| Conda-build recipe | `conda/meta.yaml` |

`conda/environment.yaml` and `conda/conda-lock.yml` are **generated artifacts** — never edit them manually. Always edit `pyproject.toml` and regenerate.

---

## Makefile Targets

| Target | Description |
|---|---|
| `make` or `make help` | Show available targets |
| `make generate` | Generate `conda/environment.yaml` from `pyproject.toml` |
| `make lock` | Generate `conda/conda-lock.yml` from `conda/environment.yaml` |
| `make env` | Create the dev conda environment from the lock file |
| `make update` | Regenerate env + relock + recreate dev environment in one shot |
| `make clean` | Remove generated environment file and lock file |

### Custom environment name

By default the environment is named after the project (e.g. `alinea-topvine`). You can override this at call time:

```bash
make env name=myenv
```

---

## First-Time Setup (Contributors)

Clone the repository, and run from inside the project directory:

```bash
make env
```

This single command:

1. Reads `pyproject.toml` and generates `conda/environment.yaml`
2. Runs `conda-lock` to resolve and lock all dependencies for `win-64` and `linux-64`
3. Creates a conda environment from the lock file

Then activate the environment:

```bash
conda activate <Your-Env-Name>
```

Test your installation
```bash
python -m unittest discover -s test -p "*.py"
```

---

## After Editing Dependencies

Whenever you add, remove, or change a dependency in `pyproject.toml`, run:

```bash
make update
```

This regenerates the environment file, relocks, and recreates the conda environment.
Commit the updated `conda/conda-lock.yml` so other contributors get the same resolution.

---

## Resetting the Environment

To remove all generated files and start fresh:

```bash
make clean
make env
```

---

## Notes

- `conda/environment.yaml` is ignored but `conda/conda-lock.yml` is committed to the repository. The lock file in particular should always be committed — it is the reproducibility artifact that guarantees identical environments across machines and over time.
- The lock file covers both `win-64` and `linux-64` platforms in a single file. `conda-lock install` automatically selects the correct platform at install time.
- `conda/meta.yaml` reads dependencies directly from `pyproject.toml` at build time and is unaffected by this workflow.



# Run the model with a qt-enabled console
cd example

ipython --gui=qt

%run tutorial.py

main()

_

# Citation

Gaëtan Louarn, Jérémie Lecoeur, Eric Lebon, A Three-dimensional Statistical Reconstruction Model of Grapevine (Vitis vinifera) Simulating Canopy Structure Variability within and between Cultivar/Training System Pairs, Annals of Botany, Volume 101, Issue 8, May 2008, Pages 1167–1184, https://doi.org/10.1093/aob/mcm170
