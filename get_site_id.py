"""
TODO: Document
TODO: Refactor and clean
TODO: Remove superfluous property entries in leaflet map
"""

import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import io


def parse_arguments():

	parser = argparse.ArgumentParser()
	parser.add_argument("--keys", type=str, nargs = "+")
	parser.add_argument("--keyfile", type=str)
	parser.add_argument("--word", type=str, required=True)
	parser.add_argument("--format", default="json")
	parser.add_argument("--plot", default=False, action="store_true", help = "Saves interactive map with stations in html file to open in browser")

	args = parser.parse_args()
	return args

def get_platsuppslag(searched_word, key, api_format="json"):
	platsuppslag_url = "https://api.sl.se/api2/typeahead.<FORMAT>?key=<DIN NYCKEL>&searchstring=<SÖKORD>"
	platsuppslag_url = platsuppslag_url.replace("<FORMAT>", api_format)
	platsuppslag_url = platsuppslag_url.replace("<DIN NYCKEL>", key.strip("\n").strip(" "))
	platsuppslag_url = platsuppslag_url.replace("<SÖKORD>", searched_word)

	r = requests.get(platsuppslag_url)
	if r.ok:
		print("Platsuppslag OK")
		response_data = r.json()["ResponseData"]

		for stop in response_data:
			stop["X"] = float(stop["X"])/1e6
			stop["Y"] = float(stop["Y"])/1e6

		return pd.DataFrame(response_data)

	else:
		 return None

def get_sites_stops(model, key):
	sites_url = 'https://api.sl.se/api2/LineData.[mode]?model=[model]&key=[key]'
	sites_url = sites_url.replace("[mode]", "json").replace("[model]", model).replace("[key]", key.strip("\n").strip(" "))

	r = requests.get(sites_url)
	if r.ok:
		results = r.json()["ResponseData"]["Result"]
		return pd.DataFrame(results)

	else:
		return None

def get_gtfs_agency_mapping():
	agency_stops_url = "https://api.trafiklab.se/v2/samtrafiken/gtfs/extra/agency_stops.txt"
	r = requests.get(agency_stops_url)
	df = pd.read_csv(io.BytesIO(r.content), dtype=str)
	return df



if __name__== "__main__":
	args = parse_arguments()

	assert not all(arg is not None for arg in [args.keys, args.keyfile]), "Both keyfile and key cannot be specified"

	if args.keyfile is not None:
		with open(args.keyfile, 'r') as fid:
			platsuppslag_key, sites_key = fid.read().split(",")


	elif args.keys is not None:
		platsuppslag_key, sites_key = args.keys

	df_platsuppslag = get_platsuppslag(args.word, platsuppslag_key)
	df_platsuppslag = df_platsuppslag[["Name", "SiteId"]]

	df_sites = get_sites_stops("site", sites_key)
	df_sites = df_sites[["SiteId", "SiteName", "StopAreaNumber"]]

	df_stops = get_sites_stops("stop", sites_key)
	df_stops = df_stops[["StopPointNumber", "StopPointName", "StopAreaNumber", "LocationNorthingCoordinate", "LocationEastingCoordinate"]]
	df_stops = df_stops.astype({'LocationNorthingCoordinate': float, 'LocationNorthingCoordinate': float})

	df_agency = get_gtfs_agency_mapping()

	df = df_sites.merge(df_platsuppslag, on="SiteId")
	df = df.merge(df_stops, on="StopAreaNumber")
	df = df.merge(df_agency, left_on="StopPointNumber", right_on="agency_stop_id")
	df = df.rename(columns = {'stop_id': 'gtfs_stop_id'})

	print(df[["Name", "SiteId", "StopPointNumber", "gtfs_stop_id", "agency_id"]])


	if args.plot:
		import geopandas as gpd
		from geopandas_view import view
		import webbrowser
		gdf = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df.LocationEastingCoordinate, df.LocationNorthingCoordinate), crs=4326)
		gdf.to_crs(3857, inplace=True)  # To jive with leaflet


		m = view(gdf)

		m.save("map.html")


		webbrowser.open("map.html", new=2)
