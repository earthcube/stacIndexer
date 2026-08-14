# stac indexer

## About

A testing repo for code to index STAC catalogs
into RDF

## Setup

Dependencies are managed with [uv](https://docs.astral.sh/uv/).

```bash
uv sync            # create .venv and install locked dependencies
uv sync --no-dev   # runtime dependencies only (as CI does)
```

Set a GitHub token for catalog downloads:

```bash
export GITHUB_TOKEN=your_token_here
```

## Usage

```bash
# Process from local catalog file
uv run main.py --configfile ./data/neon/catalog.json

# Process from URL
uv run main.py --configfile https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/stac/catalog.json

# Generate only sitemaps
uv run main.py --configfile ./data/neon/catalog.json --sitemap_only

# Validate a catalog (reports written to ./validation_reports/)
uv run main.py --configfile ./data/neon/catalog.json --validate
```

## Managing dependencies

```bash
uv add <package>          # add a runtime dependency
uv add --dev <package>    # add a dev dependency
uv lock --upgrade         # refresh uv.lock
```
