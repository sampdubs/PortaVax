import numpy as np
import pandas as pd
import googlemaps
import multiprocess
import tqdm
import pickle
import os
import plotly.express as px

# import airport location data
airports = pd.read_csv(open("airport_locations.csv"), names=["country", "lat", "lon"])

# connect to google maps API
gmaps = googlemaps.Client(key="AIzaSyAb94zapDceVmspV65wFj_-iV2AWQk9kwY")

country_to_continent = {
  "AD": "Europe",
  "AE": "Asia",
  "AF": "Asia",
  "AG": "North America",
  "AI": "North America",
  "AL": "Europe",
  "AM": "Asia",
  "AN": "North America",
  "AO": "Africa",
  "AQ": "Antarctica",
  "AR": "South America",
  "AS": "Australia",
  "AT": "Europe",
  "AU": "Australia",
  "AW": "North America",
  "AZ": "Asia",
  "BA": "Europe",
  "BB": "North America",
  "BD": "Asia",
  "BE": "Europe",
  "BF": "Africa",
  "BG": "Europe",
  "BH": "Asia",
  "BI": "Africa",
  "BJ": "Africa",
  "BM": "North America",
  "BN": "Asia",
  "BO": "South America",
  "BR": "South America",
  "BS": "North America",
  "BT": "Asia",
  "BW": "Africa",
  "BY": "Europe",
  "BZ": "North America",
  "CA": "North America",
  "CC": "Asia",
  "CD": "Africa",
  "CF": "Africa",
  "CG": "Africa",
  "CH": "Europe",
  "CI": "Africa",
  "CK": "Australia",
  "CL": "South America",
  "CM": "Africa",
  "CN": "Asia",
  "CO": "South America",
  "CR": "North America",
  "CU": "North America",
  "CV": "Africa",
  "CX": "Asia",
  "CY": "Asia",
  "CZ": "Europe",
  "DE": "Europe",
  "DJ": "Africa",
  "DK": "Europe",
  "DM": "North America",
  "DO": "North America",
  "DZ": "Africa",
  "EC": "South America",
  "EE": "Europe",
  "EG": "Africa",
  "EH": "Africa",
  "ER": "Africa",
  "ES": "Europe",
  "ET": "Africa",
  "FI": "Europe",
  "FJ": "Australia",
  "FK": "South America",
  "FM": "Australia",
  "FO": "Europe",
  "FR": "Europe",
  "GA": "Africa",
  "GB": "Europe",
  "GD": "North America",
  "GE": "Asia",
  "GF": "South America",
  "GG": "Europe",
  "GH": "Africa",
  "GI": "Europe",
  "GL": "North America",
  "GM": "Africa",
  "GN": "Africa",
  "GP": "North America",
  "GQ": "Africa",
  "GR": "Europe",
  "GS": "Antarctica",
  "GT": "North America",
  "GU": "Australia",
  "GW": "Africa",
  "GY": "South America",
  "HK": "Asia",
  "HN": "North America",
  "HR": "Europe",
  "HT": "North America",
  "HU": "Europe",
  "ID": "Asia",
  "IE": "Europe",
  "IL": "Asia",
  "IM": "Europe",
  "IN": "Asia",
  "IO": "Asia",
  "IQ": "Asia",
  "IR": "Asia",
  "IS": "Europe",
  "IT": "Europe",
  "JE": "Europe",
  "JM": "North America",
  "JO": "Asia",
  "JP": "Asia",
  "KE": "Africa",
  "KG": "Asia",
  "KH": "Asia",
  "KI": "Australia",
  "KM": "Africa",
  "KN": "North America",
  "KP": "Asia",
  "KR": "Asia",
  "KW": "Asia",
  "KY": "North America",
  "KZ": "Asia",
  "LA": "Asia",
  "LB": "Asia",
  "LC": "North America",
  "LI": "Europe",
  "LK": "Asia",
  "LR": "Africa",
  "LS": "Africa",
  "LT": "Europe",
  "LU": "Europe",
  "LV": "Europe",
  "LY": "Africa",
  "MA": "Africa",
  "MC": "Europe",
  "MD": "Europe",
  "ME": "Europe",
  "MG": "Africa",
  "MH": "Australia",
  "MK": "Europe",
  "ML": "Africa",
  "MM": "Asia",
  "MN": "Asia",
  "MO": "Asia",
  "MP": "Australia",
  "MQ": "North America",
  "MR": "Africa",
  "MS": "North America",
  "MT": "Europe",
  "MU": "Africa",
  "MV": "Asia",
  "MW": "Africa",
  "MX": "North America",
  "MY": "Asia",
  "MZ": "Africa",
  "NA": "Africa",
  "NC": "Australia",
  "NE": "Africa",
  "NF": "Australia",
  "NG": "Africa",
  "NI": "North America",
  "NL": "Europe",
  "NO": "Europe",
  "NP": "Asia",
  "NR": "Australia",
  "NU": "Australia",
  "NZ": "Australia",
  "OM": "Asia",
  "PA": "North America",
  "PE": "South America",
  "PF": "Australia",
  "PG": "Australia",
  "PH": "Asia",
  "PK": "Asia",
  "PL": "Europe",
  "PM": "North America",
  "PN": "Australia",
  "PR": "North America",
  "PS": "Asia",
  "PT": "Europe",
  "PW": "Australia",
  "PY": "South America",
  "QA": "Asia",
  "RE": "Africa",
  "RO": "Europe",
  "RS": "Europe",
  "RU": "Europe",
  "RW": "Africa",
  "SA": "Asia",
  "SB": "Australia",
  "SC": "Africa",
  "SD": "Africa",
  "SE": "Europe",
  "SG": "Asia",
  "SH": "Africa",
  "SI": "Europe",
  "SJ": "Europe",
  "SK": "Europe",
  "SL": "Africa",
  "SM": "Europe",
  "SN": "Africa",
  "SO": "Africa",
  "SR": "South America",
  "ST": "Africa",
  "SV": "North America",
  "SY": "Asia",
  "SZ": "Africa",
  "TC": "North America",
  "TD": "Africa",
  "TF": "Antarctica",
  "TG": "Africa",
  "TH": "Asia",
  "TJ": "Asia",
  "TK": "Australia",
  "TM": "Asia",
  "TN": "Africa",
  "TO": "Australia",
  "TR": "Asia",
  "TT": "North America",
  "TV": "Australia",
  "TW": "Asia",
  "TZ": "Africa",
  "UA": "Europe",
  "UG": "Africa",
  "US": "North America",
  "UY": "South America",
  "UZ": "Asia",
  "VC": "North America",
  "VE": "South America",
  "VG": "North America",
  "VI": "North America",
  "VN": "Asia",
  "VU": "Australia",
  "WF": "Australia",
  "WS": "Australia",
  "YE": "Asia",
  "YT": "Africa",
  "ZA": "Africa",
  "ZM": "Africa",
  "ZW": "Africa"
}

def getcontinent(coords):
    lat, lon = coords
    try:
        address = gmaps.reverse_geocode((lat, lon))[0]["address_components"]
        for component in address:
            if "country" in component["types"]:
                country = component["short_name"]
                return country_to_continent[country]
    except (KeyError, IndexError):
        return ""
    return ""

latlon = airports[["lat", "lon"]].values
# if not precomputed, determine continent for each airport
if not os.path.exists("continents.pkl"):
    print('Computing continents...')
    with multiprocess.Pool() as p:
        continents = list(tqdm.tqdm(p.imap(getcontinent, latlon), total=len(latlon)))
        print(continents)
        pickle.dump(continents, open("continents.pkl", "wb"))
else:
    print('Loading continents...')
    continents = pickle.load(open("continents.pkl", "rb"))

airports["continents"] = continents

# drop all rows with continents not Africa
airports = airports[airports["continents"] == "Africa"].reset_index()

def haversine(airport, allothers, to_radians=True, earth_radius=3958.8):
    """
    slightly modified version: of http://stackoverflow.com/a/29546836/2901002

    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees or in radians)

    All (lat, lon) coordinates must have numeric dtypes and be of equal length.

    """
    if to_radians:
        lat1 = np.radians(airport[0])
        lon1 = np.radians(airport[1])
        lat2 = np.radians(allothers[:,0])
        lon2 = np.radians(allothers[:,1])

    a = np.sin((lat2-lat1)/2.0)**2 + \
        np.cos(lat1) * np.cos(lat2) * np.sin((lon2-lon1)/2.0)**2

    return earth_radius * 2 * np.arcsin(np.sqrt(a))

airports["distance"] = None
airports["mindist"] = None

def find_distances(airport):
    # distance from this airport to all other airports
    airport["distance"] = haversine(airport[["lat", "lon"]], airports[["lat", "lon"]].values)
    return airport

for i in range(len(airports)):
    airports.iloc[i] = find_distances(airports.iloc[i])
    # distance to second nearest airport (first nearest is itself)
    airports.loc[i, 'mindist'] = np.partition(airports.loc[i, 'distance'], 1)[1]

# print distance to nearest airport for each airport
print(np.sort(airports['mindist'].values))

# display airport dotplot on world map
fig = px.scatter_geo(airports, lat='lat', lon='lon', hover_name="mindist")
fig.update_layout(title='World map', title_x=0.5)
fig.show()