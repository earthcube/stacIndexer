for file in ./output/*; do
    echo "Processing $file"
    # Add your processing commands here
    temp_file=$(mktemp)
    jsonld format -q $file > $temp_file
    curl -i  -X POST -H 'Content-Type:text/x-nquads' --data-binary @$temp_file  http://localhost:7878/store
    rm $temp_file
done
