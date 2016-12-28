# google_timeline_parser
parse your google location history (timeline) after exporting from google takeout

* Export your timeline data with google takeout
* Convert the json into a smaller JSON only with the fields we want using jq `cat LocationHistory.json |jq "[.locations[] | {latitudeE7, longitudeE7, timestampMs}]" > filtered_locations.json ` 
* Convert the json summary into CSV with jsonv `cat filtered_locations.json |jsonv  latitudeE7,longitudeE7,timestampMs > filtered_locations.csv` 
* Import the csv into your db. If using BigQuery you can just copy to gcloud and create an external table pointing to your file. Fields are timestamp(TIMESTAMP), date(DATE), lat(FLOAT),lng(FLOAT), and locality(STRING). All of them are required
* Execute your query. I have an example to calculate whole absence days from the UK based on the collected data
