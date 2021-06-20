import requests
import json
import matplotlib.pyplot as plt

import argparse

def get_gdf(res, coordinate_scaling = 1/1e6, s_srs = 4326, t_srs = None):

	for entry in res:
		entry["X"] = float(entry["X"])*coordinate_scaling
		entry["Y"] = float(entry["Y"])*coordinate_scaling

	gdf = gpd.GeoDataFrame(res)
	gdf["geometry"] = gpd.GeoSeries(gpd.points_from_xy(gdf.X, gdf.Y), crs = s_srs)
	if t_srs is not None:
		gdf.to_crs(t_srs, inplace=True)

	return gdf

def parse_arguments():

	parser = argparse.ArgumentParser()
	parser.add_argument("--key", type=str)
	parser.add_argument("--keyfile", type=str)
	parser.add_argument("--word", type=str, required=True)
	parser.add_argument("--format", default="json")
	parser.add_argument("--plot", default=False, action="store_true", help = "Saves interactive map with stations in html file to open in browser")

	args = parser.parse_args()
	return args

if __name__== "__main__":
	args = parse_arguments()

	assert not all(arg is not None for arg in [args.key, args.keyfile]), "Both keyfile and key cannot be specified"

	if args.keyfile is not None:
		with open(args.keyfile, 'r') as fid:
			key = fid.read().strip("\n")

	elif args.key is not None:
		key = args.key

	url = "https://api.sl.se/api2/typeahead.<FORMAT>?key=<DIN NYCKEL>&searchstring=<SÖKORD>"

	url = url.replace("<FORMAT>", args.format)
	url = url.replace("<DIN NYCKEL>", key)
	url = url.replace("<SÖKORD>", args.word)

	r = requests.get(url).json()["ResponseData"]

	longest = max([len(res["Name"]) for res in r])
	for stop in r:
		print("Name: ", stop["Name"].ljust(longest), "Site id:", stop["SiteId"], "\tType: ", stop["Type"])
	if args.plot:
		import geopandas as gpd
		from geopandas_view import view
		import webbrowser

		gdf = get_gdf(r, t_srs=3857)

		m = view(gdf)

		m.save("map.html")

		webbrowser.open("map.html", new=2)
