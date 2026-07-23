# topvine

A 3D statistical reconstruction model of grapevine (*Vitis vinifera* L.) that simulates canopy structure
accounting for (cultivar)-(training system) pairs.


## Quick Links

- **For end-users:** [Installation](#installation) | [Usage](#usage)
- **For contributors:** [Development Setup](#development-environment-setup) | [Contributing](#contributing)

---

## Installation

### Requirements

- Python 3.8+
- Conda (Miniconda or Anaconda)

### Install from source

```bash
git clone git@github.com:openalea-incubator/topvine.git
cd topvine
conda env create -f conda/conda-lock.yml
conda activate topvine
```

Or, with a custom environment name:

```bash
conda install --name myenv --file conda/conda-lock.yml
conda activate myenv
```

### Verify installation

```bash
python -c "import topvine; print(topvine.__version__)"
```

---

## Usage

See the [`examples/`](examples/) directory for usage examples.

---


## Development Environment Setup

### Prerequisites

The following tools must be installed and available in your shell before using the Makefile.
Ensure that these prerequisites are installed in the **base** conda environment.

#### 1. Conda

Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution).

Verify:
```bash
conda --version
```

#### 2. conda-lock

```bash
conda install -c conda-forge conda-lock
```

Verify:
```bash
conda-lock --version
```

#### 3. make

**Linux:**
```bash
make --version  # Check if installed
```
If not installed:
```bash
sudo apt install make        # Debian/Ubuntu
sudo dnf install make        # RHEL/Fedora
```

**macOS:**
Usually pre-installed. If not:
```bash
brew install make
```

**Windows (PowerShell, run as administrator):**
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

Restart your terminal and verify:
```bash
make --version
```

---

### Dependency management

Dependencies are defined in a single source of truth: **`pyproject.toml`**

The workflow is:

1. **Edit** `pyproject.toml` with your changes
2. **Run** `make update` to regenerate lock files and recreate the environment
3. **Commit** the updated `conda/conda-lock.yml` to the repository

**Key files:**

```
project-root/
├── Makefile                        ← entry point for all environment commands
├── pyproject.toml                  ← single source of truth for all dependencies
├── scripts/
│   └── generate_env_specs.py       ← generates environment.yaml from pyproject.toml
└── conda/
    ├── meta.yaml                   ← conda-build recipe
    ├── environment.yaml            ← generated (do not edit)
    └── conda-lock.yml              ← generated (committed to repo for reproducibility)
```

⚠️ **Important:** `conda/environment.yaml` and `conda/conda-lock.yml` are generated artifacts. Always edit `pyproject.toml` and regenerate them using `make update`.

### Dependency ownership

| What | Where |
|---|---|
| Runtime pip-installable deps | `[project.dependencies]` in `pyproject.toml` |
| Conda-only runtime deps | `[tool.conda.environment.dependencies]` in `pyproject.toml` |
| Dev/contributor deps | `[project.optional-dependencies.dev]` in `pyproject.toml` |
| Conda channels | hardcoded in `scripts/generate_envs.py` |
| Conda-build recipe | `conda/meta.yaml` |

---

### Makefile targets

| Target | Description |
|---|---|
| `make` or `make help` | Show available targets |
| `make generate` | Generate `conda/environment.yaml` from `pyproject.toml` |
| `make lock` | Generate `conda/conda-lock.yml` from `conda/environment.yaml` |
| `make env` | Create the dev conda environment from the lock file |
| `make update` | Regenerate env + relock + recreate dev environment (all-in-one) |
| `make clean` | Remove generated environment file and lock file |

#### Custom environment name

By default, the environment is named `openalea-topvine`. Override at call time:

```bash
make env name=myenv
```

---

### First-time setup

Clone the repository and run from inside the project directory:

```bash
make env
```

This single command:

1. Reads `pyproject.toml` and generates `conda/environment.yaml`
2. Runs `conda-lock` to resolve and lock all dependencies for `win-64` and `linux-64`
3. Creates a conda environment from the lock file

Then activate the environment:

```bash
conda activate openalea-topvine
```

---

### After editing dependencies

Whenever you add, remove, or update a dependency in `pyproject.toml`, run:

```bash
make update
```

This regenerates the environment, relocks, and recreates the conda environment in one step.

**Always commit the updated `conda/conda-lock.yml`** so other contributors get the exact same dependency resolution.

---

### Resetting the environment

To remove all generated files and start fresh:

```bash
make clean
make env
```

---

## Testing

Run the test suite:

```bash
python -m unittest discover -s test -p "*.py"
```

Or with coverage:

```bash
# Add coverage command here when available
```

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes and add tests
4. Run the test suite to ensure nothing breaks
5. Commit with clear messages
6. Push to your fork and open a pull request

---

## Troubleshooting

### Conda environment not found

Ensure you've run `make env` in the project root and activated the environment:

```bash
conda activate openalea-topvine
```

### `conda-lock` command not found

Install it in your base environment:

```bash
conda install -c conda-forge conda-lock
```

### Lock file conflicts after pulling

If `conda/conda-lock.yml` was updated, regenerate your environment:

```bash
make update
```

### Permission denied on Windows (PowerShell PATH update)

Run PowerShell as administrator before executing the PATH update command.

---

## Citation

If you use topvine in your research, please cite:

> Gaëtan Louarn, Jérémie Lecoeur, Eric Lebon, "A Three-dimensional Statistical Reconstruction Model of Grapevine (*Vitis vinifera*) Simulating Canopy Structure Variability within and between Cultivar/Training System Pairs," *Annals of Botany*, Volume 101, Issue 8, May 2008, Pages 1167–1184. https://doi.org/10.1093/aob/mcm170

---

## License

CECILL-C

---

## Authors

Gaetan LOUARN (gaetan.louarn@inrae.fr)
Rami ALBASHA (rami.albasha@inrae.fr)
Stathis DELIVORIAS (stathissupagro@gmx.com)