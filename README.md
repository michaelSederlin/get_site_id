# get_site_id


A simple application which collects site IDs from the SL API "SL Platsuppslag" and from "SL Hållplatser och Linjer" available at Trafiklab. 
The purpose of the application is to search for a site with a partial string and find the corresponding stop id used in the gtfs data. To aid in this the application can plot the collected points on an interactive map containing the information for each point. 
Uses Geopandas and geopands_view under developement and available at: https://github.com/martinfleis/geopandas-view

In order to use it a valid API key for both the API "Platsuppslag" (https://www.trafiklab.se/api/sl-platsuppslag/dokumentation) and "SL Hållplatser och Linjer 2" (https://www.trafiklab.se/api/sl-hallplatser-och-linjer-2/dokumentation) is necessary. 

The application is used from the command line and collects the response for a given station and prints results. 


The API key can either be provided as a string with argument `--key` or as a text file with argument `--keyfile`.
Example:
```
python3 get_site_id.py --keyfile <FILE WITH API KEYS> --word "Slussen" --plot
```

Which saves the following map into a file `map.html` and opens it in a browser for viewing
![test](slussen.gif)
