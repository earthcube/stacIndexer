# stac indexer

## About

A  repo for code to index STAC catalogs into JSON-LD Schema.org Dataset and DatasetCatalog files

A workflow validates the stac catalogs for [ecoforecast.org](https://ecoforecast.org) [catalog](https://raw.githubusercontent.com/eco4cast/challenge-catalogs/main/catalog.json) and outputs the results to a directory.

* The output is written to a directory of JSON-LD files [BRANCH data at data/output/](https://github.com/earthcube/stacIndexer/tree/data/data/output)
* the validated catalogs are written to the [BRANCH data in the directory data/validation_reports/](https://github.com/earthcube/stacIndexer/tree/data/data/validation_reports)
* The latest validation is available at [data/validation_reports/latest.md](https://github.com/earthcube/stacIndexer/blob/data/data/validation_reports/latest.md)


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
