# STAC Validation Report

- **Catalog:** `https://raw.githubusercontent.com/eco4cast/challenge-catalogs/main/catalog.json`
- **Status:** ❌ **INVALID**
- **Generated:** 2026-09-05T00:26:06.028986

## Summary

| Metric | Count |
| --- | ---: |
| Catalogs validated | 4 |
| Collections validated | 17 |
| Items validated | 395 |
| Validation errors | 20 |
| Validation warnings | 0 |
| Distinct issues | 11 |

## Issues (11 distinct, 20 errors)

| # | Scope | Issue | Errors |
| ---: | --- | --- | ---: |
| 1 | **Catalog** ⚠️ | Catalog children could not be read | 1 |
| 2 | **Catalog** ⚠️ | Catalog children could not be read | 1 |
| 3 | **Collection** ⚠️ | Collection is being checked against an Item-only schema | 2 |
| 4 | **Collection** ⚠️ | Collection children could not be read | 1 |
| 5 | **Collection** ⚠️ | Collection children could not be read | 1 |
| 6 | **Collection** ⚠️ | `assets.thumbnail.title` has the wrong type | 1 |
| 7 | **Collection** ⚠️ | Collection children could not be read | 1 |
| 8 | **Collection** ⚠️ | Collection children could not be read | 1 |
| 9 | **Collection** ⚠️ | Collection children could not be read | 1 |
| 10 | **Collection** ⚠️ | Collection children could not be read | 1 |
| 11 | Item | `properties.providers.0.url` has the wrong type | 9 |

### 1. Catalog children could not be read ⚠️

- **Affects:** 1 catalog
- **Objects:** `neon4cast-stac`

**What it means:** Walking into `neon4cast-stac` failed, so anything below it was never validated. The counts in the summary are therefore incomplete.

**Suggested fix:** Check that the child links resolve (correct href, reachable network, valid JSON).

<details><summary>Example raw error</summary>

```
Failed to get children for catalog 'neon4cast-stac': HREF: 'https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/sites/collection.json' does not resolve to a STAC object
```

</details>

<details><summary>All 1 raw errors</summary>

**1.**

```
Failed to get children for catalog 'neon4cast-stac': HREF: 'https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/sites/collection.json' does not resolve to a STAC object
```

</details>

### 2. Catalog children could not be read ⚠️

- **Affects:** 1 catalog
- **Objects:** `vera4cast-stac`

**What it means:** Walking into `vera4cast-stac` failed, so anything below it was never validated. The counts in the summary are therefore incomplete.

**Suggested fix:** Check that the child links resolve (correct href, reachable network, valid JSON).

<details><summary>Example raw error</summary>

```
Failed to get children for catalog 'vera4cast-stac': HREF: 'https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/sites/collection.json' does not resolve to a STAC object
```

</details>

<details><summary>All 1 raw errors</summary>

**1.**

```
Failed to get children for catalog 'vera4cast-stac': HREF: 'https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/sites/collection.json' does not resolve to a STAC object
```

</details>

### 3. Collection is being checked against an Item-only schema ⚠️

- **Affects:** 2 collections
- **Property:** `type`
- **Failed schema keyword:** `const`
- **Schema:** [scientific extension v1.0.0](https://stac-extensions.github.io/scientific/v1.0.0/schema.json)
- **Offending values:** `'Collection'`
- **Objects:** [`inventory`](https://raw.githubusercontent.com/eco4cast/usgsrc4cast-ci/main/catalog/inventory/collection.json), [`sites`](https://raw.githubusercontent.com/eco4cast/usgsrc4cast-ci/main/catalog/sites/collection.json)

**What it means:** The `scientific extension v1.0.0` schema asserts `type: Feature`, which only Items have. A Collection can never satisfy it, so this fires for every collection that declares the extension. This usually means the extension URL or version in `stac_extensions` is wrong for this object type, rather than the metadata itself being bad.

**Suggested fix:** Check the `stac_extensions` entry — use the version of the extension whose schema covers Collections, or drop it from Collection documents.

<details><summary>Example raw error</summary>

```
Collection 'inventory' validation failed: Validation failed for Collection at https://raw.githubusercontent.com/eco4cast/usgsrc4cast-ci/main/catalog/inventory/collection.json with ID inventory against schema at https://stac-extensions.github.io/scientific/v1.0.0/schema.json
'Feature' was expected

Failed validating 'const' in schema[0]['allOf'][1]['properties']['type']:
    {'const': 'Feature'}

On instance['type']:
    'Collection'
```

</details>

<details><summary>All 2 raw errors</summary>

**1.**

```
Collection 'inventory' validation failed: Validation failed for Collection at https://raw.githubusercontent.com/eco4cast/usgsrc4cast-ci/main/catalog/inventory/collection.json with ID inventory against schema at https://stac-extensions.github.io/scientific/v1.0.0/schema.json
'Feature' was expected

Failed validating 'const' in schema[0]['allOf'][1]['properties']['type']:
    {'const': 'Feature'}

On instance['type']:
    'Collection'
```

**2.**

```
Collection 'sites' validation failed: Validation failed for Collection at https://raw.githubusercontent.com/eco4cast/usgsrc4cast-ci/main/catalog/sites/collection.json with ID sites against schema at https://stac-extensions.github.io/scientific/v1.0.0/schema.json
'Feature' was expected

Failed validating 'const' in schema[0]['allOf'][1]['properties']['type']:
    {'const': 'Feature'}

On instance['type']:
    'Collection'
```

</details>

### 4. Collection children could not be read ⚠️

- **Affects:** 1 collection
- **Objects:** `daily-scores`

**What it means:** Walking into `daily-scores` failed, so anything below it was never validated. The counts in the summary are therefore incomplete.

**Suggested fix:** Check that the child links resolve (correct href, reachable network, valid JSON).

<details><summary>Example raw error</summary>

```
Failed to get items for collection 'daily-scores': HREF: 'https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/scores/Aquatics/Daily_Dissolved_oxygen/models/GLEON_lm_lag_1day.json' does not resolve to a STAC object
```

</details>

<details><summary>All 1 raw errors</summary>

**1.**

```
Failed to get items for collection 'daily-scores': HREF: 'https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/scores/Aquatics/Daily_Dissolved_oxygen/models/GLEON_lm_lag_1day.json' does not resolve to a STAC object
```

</details>

### 5. Collection children could not be read ⚠️

- **Affects:** 1 collection
- **Objects:** `noaa-forecasts`

**What it means:** Walking into `noaa-forecasts` failed, so anything below it was never validated. The counts in the summary are therefore incomplete.

**Suggested fix:** Check that the child links resolve (correct href, reachable network, valid JSON).

<details><summary>Example raw error</summary>

```
Failed to get items for collection 'noaa-forecasts': HREF: 'https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/noaa_forecasts/Pseudo/collection.json' does not resolve to a STAC object
```

</details>

<details><summary>All 1 raw errors</summary>

**1.**

```
Failed to get items for collection 'noaa-forecasts': HREF: 'https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/noaa_forecasts/Pseudo/collection.json' does not resolve to a STAC object
```

</details>

### 6. `assets.thumbnail.title` has the wrong type ⚠️

- **Affects:** 1 collection
- **Property:** `assets.thumbnail.title`
- **Failed schema keyword:** `type`
- **Schema:** [STAC v1.1.0 collection-spec](https://schemas.stacspec.org/v1.1.0/collection-spec/json-schema/collection.json)
- **Offending values:** `{}`
- **Objects:** [`targets`](https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/targets/collection.json)

**What it means:** {} is not of type 'string'

**Suggested fix:** Correct the value's type.

<details><summary>Example raw error</summary>

```
Collection 'targets' validation failed: Validation failed for Collection at https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/targets/collection.json with ID targets against schema at https://schemas.stacspec.org/v1.1.0/collection-spec/json-schema/collection.json
{} is not of type 'string'

Failed validating 'type' in schema['allOf'][0]['properties']['assets']['additionalProperties']['allOf'][0]['properties']['title']:
    {'title': 'Asset title', 'type': 'string'}

On instance['assets']['thumbnail']['title']:
    {}
```

</details>

<details><summary>All 1 raw errors</summary>

**1.**

```
Collection 'targets' validation failed: Validation failed for Collection at https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/targets/collection.json with ID targets against schema at https://schemas.stacspec.org/v1.1.0/collection-spec/json-schema/collection.json
{} is not of type 'string'

Failed validating 'type' in schema['allOf'][0]['properties']['assets']['additionalProperties']['allOf'][0]['properties']['title']:
    {'title': 'Asset title', 'type': 'string'}

On instance['assets']['thumbnail']['title']:
    {}
```

</details>

### 7. Collection children could not be read ⚠️

- **Affects:** 1 collection
- **Objects:** `summaries`

**What it means:** Walking into `summaries` failed, so anything below it was never validated. The counts in the summary are therefore incomplete.

**Suggested fix:** Check that the child links resolve (correct href, reachable network, valid JSON).

<details><summary>Example raw error</summary>

```
Failed to get items for collection 'summaries': HREF: 'https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/summaries/Aquatics/Daily_Dissolved_oxygen/models/GLEON_lm_lag_1day.json' does not resolve to a STAC object
```

</details>

<details><summary>All 1 raw errors</summary>

**1.**

```
Failed to get items for collection 'summaries': HREF: 'https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/summaries/Aquatics/Daily_Dissolved_oxygen/models/GLEON_lm_lag_1day.json' does not resolve to a STAC object
```

</details>

### 8. Collection children could not be read ⚠️

- **Affects:** 1 collection
- **Objects:** `daily-scores`

**What it means:** Walking into `daily-scores` failed, so anything below it was never validated. The counts in the summary are therefore incomplete.

**Suggested fix:** Check that the child links resolve (correct href, reachable network, valid JSON).

<details><summary>Example raw error</summary>

```
Failed to get items for collection 'daily-scores': HREF: 'https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/scores/Biological/Daily_Chlorophyll-a/models/asl.persistence.json' does not resolve to a STAC object
```

</details>

<details><summary>All 1 raw errors</summary>

**1.**

```
Failed to get items for collection 'daily-scores': HREF: 'https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/scores/Biological/Daily_Chlorophyll-a/models/asl.persistence.json' does not resolve to a STAC object
```

</details>

### 9. Collection children could not be read ⚠️

- **Affects:** 1 collection
- **Objects:** `noaa-forecasts`

**What it means:** Walking into `noaa-forecasts` failed, so anything below it was never validated. The counts in the summary are therefore incomplete.

**Suggested fix:** Check that the child links resolve (correct href, reachable network, valid JSON).

<details><summary>Example raw error</summary>

```
Failed to get items for collection 'noaa-forecasts': HREF: 'https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/noaa_forecasts/Pseudo/collection.json' does not resolve to a STAC object
```

</details>

<details><summary>All 1 raw errors</summary>

**1.**

```
Failed to get items for collection 'noaa-forecasts': HREF: 'https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/noaa_forecasts/Pseudo/collection.json' does not resolve to a STAC object
```

</details>

### 10. Collection children could not be read ⚠️

- **Affects:** 1 collection
- **Objects:** `summaries`

**What it means:** Walking into `summaries` failed, so anything below it was never validated. The counts in the summary are therefore incomplete.

**Suggested fix:** Check that the child links resolve (correct href, reachable network, valid JSON).

<details><summary>Example raw error</summary>

```
Failed to get items for collection 'summaries': HREF: 'https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/summaries/Biological/Daily_Chlorophyll-a/models/asl.persistence.json' does not resolve to a STAC object
```

</details>

<details><summary>All 1 raw errors</summary>

**1.**

```
Failed to get items for collection 'summaries': HREF: 'https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/summaries/Biological/Daily_Chlorophyll-a/models/asl.persistence.json' does not resolve to a STAC object
```

</details>

### 11. `properties.providers.0.url` has the wrong type

- **Affects:** 9 items
- **Property:** `properties.providers.0.url`
- **Failed schema keyword:** `type`
- **Schema:** [STAC v1.1.0 item-spec](https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json)
- **Offending values:** `None`
- **Objects:** [`bee_bake_RFModel_2024_temperature_P1D_forecast (daily-forecasts)`](https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/forecasts/Aquatics/Daily_Water_temperature/models/bee_bake_RFModel_2024.json), [`asl.persistence_Chla_ugL_mean_P1D_forecast (daily-forecasts)`](https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Biological/Daily_Chlorophyll-a/models/asl.persistence.json), [`LSTM_Chla_ugL_mean_P1D_forecast (daily-forecasts)`](https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Biological/Daily_Chlorophyll-a/models/LSTM.json), [`asl.persistence_Bloom_binary_mean_P1D_forecast (daily-forecasts)`](https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Biological/Daily_Bloom_binary/models/asl.persistence.json), [`persistenceFO_Temp_C_mean_P1D_forecast (daily-forecasts)`](https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Physical/Daily_Water_temperature/models/persistenceFO.json), [`flareGOTM_Temp_C_mean_P1D_forecast (daily-forecasts)`](https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Physical/Daily_Water_temperature/models/flareGOTM.json), [`asl.persistence_Temp_C_mean_P1D_forecast (daily-forecasts)`](https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Physical/Daily_Water_temperature/models/asl.persistence.json), [`asl.persistence_Secchi_m_sample_P1D_forecast (daily-forecasts)`](https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Physical/Daily_Secchi/models/asl.persistence.json), … and 1 more

**What it means:** None is not of type 'string'

**Suggested fix:** Correct the value's type.

<details><summary>Example raw error</summary>

```
Item 'bee_bake_RFModel_2024_temperature_P1D_forecast' in collection 'daily-forecasts' validation failed: Validation failed for Feature at https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/forecasts/Aquatics/Daily_Water_temperature/models/bee_bake_RFModel_2024.json with ID bee_bake_RFModel_2024_temperature_P1D_forecast against schema at https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json
None is not of type 'string'

Failed validating 'type' in schema['allOf'][0]['allOf'][2]['properties']['properties']['allOf'][0]['allOf'][6]['properties']['providers']['items']['properties']['url']:
    {'title': 'Organization homepage', 'type': 'string', 'format': 'iri'}

On instance['properties']['providers'][0]['url']:
    None
```

</details>

<details><summary>All 9 raw errors</summary>

**1.**

```
Item 'bee_bake_RFModel_2024_temperature_P1D_forecast' in collection 'daily-forecasts' validation failed: Validation failed for Feature at https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/forecasts/Aquatics/Daily_Water_temperature/models/bee_bake_RFModel_2024.json with ID bee_bake_RFModel_2024_temperature_P1D_forecast against schema at https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json
None is not of type 'string'

Failed validating 'type' in schema['allOf'][0]['allOf'][2]['properties']['properties']['allOf'][0]['allOf'][6]['properties']['providers']['items']['properties']['url']:
    {'title': 'Organization homepage', 'type': 'string', 'format': 'iri'}

On instance['properties']['providers'][0]['url']:
    None
```

**2.**

```
Item 'asl.persistence_Chla_ugL_mean_P1D_forecast' in collection 'daily-forecasts' validation failed: Validation failed for Feature at https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Biological/Daily_Chlorophyll-a/models/asl.persistence.json with ID asl.persistence_Chla_ugL_mean_P1D_forecast against schema at https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json
None is not of type 'string'

Failed validating 'type' in schema['allOf'][0]['allOf'][2]['properties']['properties']['allOf'][0]['allOf'][6]['properties']['providers']['items']['properties']['url']:
    {'title': 'Organization homepage', 'type': 'string', 'format': 'iri'}

On instance['properties']['providers'][0]['url']:
    None
```

**3.**

```
Item 'LSTM_Chla_ugL_mean_P1D_forecast' in collection 'daily-forecasts' validation failed: Validation failed for Feature at https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Biological/Daily_Chlorophyll-a/models/LSTM.json with ID LSTM_Chla_ugL_mean_P1D_forecast against schema at https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json
None is not of type 'string'

Failed validating 'type' in schema['allOf'][0]['allOf'][2]['properties']['properties']['allOf'][0]['allOf'][6]['properties']['providers']['items']['properties']['url']:
    {'title': 'Organization homepage', 'type': 'string', 'format': 'iri'}

On instance['properties']['providers'][0]['url']:
    None
```

**4.**

```
Item 'asl.persistence_Bloom_binary_mean_P1D_forecast' in collection 'daily-forecasts' validation failed: Validation failed for Feature at https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Biological/Daily_Bloom_binary/models/asl.persistence.json with ID asl.persistence_Bloom_binary_mean_P1D_forecast against schema at https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json
None is not of type 'string'

Failed validating 'type' in schema['allOf'][0]['allOf'][2]['properties']['properties']['allOf'][0]['allOf'][6]['properties']['providers']['items']['properties']['url']:
    {'title': 'Organization homepage', 'type': 'string', 'format': 'iri'}

On instance['properties']['providers'][0]['url']:
    None
```

**5.**

```
Item 'persistenceFO_Temp_C_mean_P1D_forecast' in collection 'daily-forecasts' validation failed: Validation failed for Feature at https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Physical/Daily_Water_temperature/models/persistenceFO.json with ID persistenceFO_Temp_C_mean_P1D_forecast against schema at https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json
None is not of type 'string'

Failed validating 'type' in schema['allOf'][0]['allOf'][2]['properties']['properties']['allOf'][0]['allOf'][6]['properties']['providers']['items']['properties']['url']:
    {'title': 'Organization homepage', 'type': 'string', 'format': 'iri'}

On instance['properties']['providers'][0]['url']:
    None
```

**6.**

```
Item 'flareGOTM_Temp_C_mean_P1D_forecast' in collection 'daily-forecasts' validation failed: Validation failed for Feature at https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Physical/Daily_Water_temperature/models/flareGOTM.json with ID flareGOTM_Temp_C_mean_P1D_forecast against schema at https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json
None is not of type 'string'

Failed validating 'type' in schema['allOf'][0]['allOf'][2]['properties']['properties']['allOf'][0]['allOf'][6]['properties']['providers']['items']['properties']['url']:
    {'title': 'Organization homepage', 'type': 'string', 'format': 'iri'}

On instance['properties']['providers'][0]['url']:
    None
```

**7.**

```
Item 'asl.persistence_Temp_C_mean_P1D_forecast' in collection 'daily-forecasts' validation failed: Validation failed for Feature at https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Physical/Daily_Water_temperature/models/asl.persistence.json with ID asl.persistence_Temp_C_mean_P1D_forecast against schema at https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json
None is not of type 'string'

Failed validating 'type' in schema['allOf'][0]['allOf'][2]['properties']['properties']['allOf'][0]['allOf'][6]['properties']['providers']['items']['properties']['url']:
    {'title': 'Organization homepage', 'type': 'string', 'format': 'iri'}

On instance['properties']['providers'][0]['url']:
    None
```

**8.**

```
Item 'asl.persistence_Secchi_m_sample_P1D_forecast' in collection 'daily-forecasts' validation failed: Validation failed for Feature at https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Physical/Daily_Secchi/models/asl.persistence.json with ID asl.persistence_Secchi_m_sample_P1D_forecast against schema at https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json
None is not of type 'string'

Failed validating 'type' in schema['allOf'][0]['allOf'][2]['properties']['properties']['allOf'][0]['allOf'][6]['properties']['providers']['items']['properties']['url']:
    {'title': 'Organization homepage', 'type': 'string', 'format': 'iri'}

On instance['properties']['providers'][0]['url']:
    None
```

**9.**

```
Item 'asl.persistence_DO_mgL_mean_P1D_forecast' in collection 'daily-forecasts' validation failed: Validation failed for Feature at https://raw.githubusercontent.com/LTREB-reservoirs/vera4cast-catalog/main/forecasts/Chemical/Daily_oxygen_concentration/models/asl.persistence.json with ID asl.persistence_DO_mgL_mean_P1D_forecast against schema at https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json
None is not of type 'string'

Failed validating 'type' in schema['allOf'][0]['allOf'][2]['properties']['properties']['allOf'][0]['allOf'][6]['properties']['providers']['items']['properties']['url']:
    {'title': 'Organization homepage', 'type': 'string', 'format': 'iri'}

On instance['properties']['providers'][0]['url']:
    None
```

</details>

## Warnings (0)

No warnings.
