# Notes on fixing issues

# dates
pending is not a date

## href
arrays and null is not a valid href
changed to a valid empty href.

{
      "rel": "item",
      "href": [],
      "type": "text/html",
      "title": "Link for Model Code"
    }

https://github.com/earthcube/stacIndexer/blob/yl/data/challenge/neon4cast-stac/forecasts/models/model_items/GLEON_physics.json
```

should not generate an asset, or may point to example.com

```
{
      "rel": "item",
      "href": "https://github.com/radiantearth",
      "type": "text/html",
      "title": "Link for Model Code"
    }
## hrefs cannot be arrays
https://github.com/earthcube/stacIndexer/blob/8a64765c652a85438c54a5b773d0e5a09571ad30/data/challenge/neon4cast-stac/summaries/Aquatics/Daily_Chlorophyll_a/collection.json#L281
'/Users/valentin/development/dev_earthcube/stacIndexer/data/challenge/neon4cast-stac/summaries/Aquatics/Daily_Chlorophyll_a/collection.json'

['s3://anonymous@bio230014-bucket01/challenges/forecasts/parquet/project_id=neon4cast/duration=P1D/variable=chla?endpoint_override=sdsc.osn.xsede.org', 's3://anonymous@bio230014-bucket01/challenges/forecasts/parquet/project_id=usgsrc4cast/duration=P1D/variable=chla?endpoint_override=sdsc.osn.xsede.org']


## bbox should not be lists

"bbox": [
    
      -156.6194,
      71.2824,
      -66.7987,
      71.2824
    
  ],

(used two replace in files (
1:
"bbox": [
    [

2:

))

the bbox should be 
"bbox": [
      -156.6194,
      71.2824,
      -66.7987,
      71.2824
  ],
