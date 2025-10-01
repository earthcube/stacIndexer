# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a STAC (SpatioTemporal Asset Catalog) indexer that converts STAC catalogs into RDF/JSON-LD format with schema.org metadata. The system processes ecological forecasting data from multiple sources (neon4cast, vera4cast, usgsrc4cast) and generates structured metadata for better discoverability.

## Core Architecture

### Main Entry Point
- `main.py`: CLI entry point that accepts config file, branch, and sitemap_only parameters
- Calls `defs.walkstac.walk_stac()` which orchestrates the entire indexing process

### Key Modules
- `defs/walkstac.py`: Core orchestration and STAC traversal logic
- `defs/convertas.py`: Coordinate conversion utilities
- `defs/datacitation.py`: Citation metadata generation
- `archive/spatial.py`: Spatial data processing with S2 cells and schema.org geo markup
- `archive/s2cells.py`: S2 spherical geometry cell generation

### Data Flow
1. Downloads STAC catalogs from GitHub repositories or processes URLs
2. Cleans malformed JSON data (fixes null hrefs, invalid timestamps)
3. Recursively walks catalog → collections → items → assets
4. Converts each item to schema.org JSON-LD Dataset format
5. Generates spatial coverage using bounding boxes, S2 cells, and coordinates
6. Outputs structured JSON files and XML sitemaps

## Common Commands

### Running the Indexer
```bash
# Process from local catalog file
python main.py --configfile ./data/neon/catalog.json

# Process from URL
python main.py --configfile https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/stac/catalog.json

# Generate only sitemaps
python main.py --configfile ./data/neon/catalog.json --sitemap_only

# Specify GitHub branch for output URLs
python main.py --configfile ./data/neon/catalog.json --branch develop
```

### Validating STAC Catalogs
```bash
# Validate a URL-based STAC catalog and generate error report
python main.py --configfile https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/stac/catalog.json --validate

# Validate a local STAC catalog
python main.py --configfile ./data/neon/catalog.json --validate

# Validation reports are saved to ./validation_reports/ directory
```

### Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Set GitHub token for API access (required for downloading catalogs)
export GITHUB_TOKEN=your_token_here
```

### Development/Testing
```bash
# Enable debug output
export DEBUG=TRUE
python main.py --configfile ./data/examples/catalog.json

# Validate outputs
ls data/output/  # Check generated JSON-LD files
ls data/output/sitemap/  # Check generated XML sitemaps
```

## Key Implementation Details

### Data Cleaning Pipeline
The system handles malformed STAC data by applying systematic replacements:
- Fixes empty/null href values
- Corrects invalid timestamp formats (InfT00:00:00Z patterns)
- Adjusts nested bbox arrays

### Output Structure
- `data/output/{repo-name}/`: JSON-LD Dataset files (10-char hash names)
- `data/output/sitemap/`: XML sitemaps for each processed repository
- Files use schema.org Dataset vocabulary with spatial coverage, citations, and distributions

### Spatial Data Enhancement
- Converts bounding boxes to S2 spherical cells (level 13)
- Generates schema.org Place objects with GeoShape and GeoCoordinates
- Links to STKO knowledge graph ontology for S2 cells

### Error Handling
- Graceful handling of missing collections, items, or malformed data
- Comprehensive logging with item/collection/catalog context
- Continues processing when individual items fail

## Environment Variables
- `GITHUB_TOKEN`: Required for downloading STAC catalogs from GitHub API
- `DEBUG`: Set to "TRUE" to enable detailed icecream debugging output