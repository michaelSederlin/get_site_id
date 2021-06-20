# get_site_id


A simple application which collects site IDs from the SL API "SL Platsuppslag" available at Trafiklab.  

In order to use it a valid API key is necessary. 

The application is used from the command line and collects the response for a given station and prints results. 
Can also plot the stations in an interactive map based on the geopandas_view extension to standard geopandas. 

Example:
```
python3 get_site_id.py --key <API KEY> --word <SEARCH STRING> --plot
```
