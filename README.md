# get_site_id


A simple application which collects site IDs from the SL API "SL Platsuppslag" available at Trafiklab.  
Uses Geopandas and geopands_view under developement and available at: https://github.com/martinfleis/geopandas-view

In order to use it a valid API key is necessary. 

The application is used from the command line and collects the response for a given station and prints results. 
Can also plot the stations in an interactive map based on the geopandas_view extension to standard geopandas. 

The API key can either be provided as a string with argument `--key` or as a text file with argument `--keyfile`.
Example:
```
python3 get_site_id.py --keyfile <FILE WITH API KEYS> --word "Slussen" --plot
```

Which saves the following map into a file `map.html` and opens it in a browser for viewing
![test](slussen.gif)
