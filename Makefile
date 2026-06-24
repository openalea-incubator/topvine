# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

name		?= topvine-dev
PYTHON		?= python
PLATFORMS	?= win-64 linux-64

ENV_FILE  := conda/environment.yaml
LOCK_FILE := conda/conda-lock.yml

GENERATE_SCRIPT := scripts/generate_env_specs.py

# ---------------------------------------------------------------------------
# Help (default target)
# ---------------------------------------------------------------------------

.PHONY: help
help:
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "  generate       Generate environment.yaml from pyproject.toml"
	@echo "  lock           Generate conda-lock.yml from environment.yaml"
	@echo "  env        Create the dev conda environment from lock file (contributors)"
	@echo "  update         Regenerate env + relock + recreate dev environment"
	@echo "  clean          Remove generated environment file and lock file"
	@echo ""

# ---------------------------------------------------------------------------
# Step 1 — Generate environment.yaml from pyproject.toml
# ---------------------------------------------------------------------------

.PHONY: generate
generate:
	$(PYTHON) $(GENERATE_SCRIPT)

# ---------------------------------------------------------------------------
# Step 2 — Lock the dev environment (cross-platform)
# ---------------------------------------------------------------------------

.PHONY: lock
lock: generate
	conda-lock lock \
		-f $(ENV_FILE) \
		$(foreach p,$(PLATFORMS),--platform $(p)) \
		--lockfile $(LOCK_FILE)

# ---------------------------------------------------------------------------
# Step 3 — Create dev environment from lock file (contributors)
# ---------------------------------------------------------------------------

.PHONY: env
env: lock
	conda-lock install --name $(name) $(LOCK_FILE)
	conda run -n $(name) pip install -e .

# ---------------------------------------------------------------------------
# Convenience — regenerate + relock + recreate dev env in one shot
# ---------------------------------------------------------------------------

.PHONY: update
update: generate lock
	conda-lock install --name $(name) $(LOCK_FILE)

# ---------------------------------------------------------------------------
# Clean generated files (sources in pyproject.toml are untouched)
# ---------------------------------------------------------------------------

.PHONY: clean
clean:
	rm -f $(ENV_FILE) $(LOCK_FILE)