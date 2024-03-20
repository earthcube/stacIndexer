#!/bin/bash

urls=$(curl -L   -H "Accept: application/vnd.github+json"    -H "X-GitHub-Api-Version: 2022-11-28"   https://api.github.com/repos/earthcube/stacIndexer/contents/data/output | jq '.[].download_url'
)

  # Create a filename based on the URL (remove special characters)
filename="sitemap.xml"

echo "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">" > "$filename"

# Loop through each URL
for urlin in $urls; do

  url=${urlin//\"}
  # Create a basic sitemap structure with the URL
  echo "  <url>" >> "$filename"
  echo "    <loc>$url</loc>" >> "$filename"
  echo "  </url>" >> "$filename"

  # Print a message for clarity
  # echo "Created sitemap: $filename"
done

echo "</urlset>" >> "$filename"
