import json
import requests

# Send a GET request to the specified URL
rep = requests.get("https://dikhanbabanan.kz/")

# Ensure the response is in JSON format
try:
    data = rep.text
except ValueError:
    print("Error: Response is not in JSON format")
    data = None

if data:
    # Open a file in write mode
    with open("data.json", "w") as out_file:
        # Dump the JSON data to the file with indentation for readability
        json.dump(data, out_file, indent=4)

#rep = requests.get("https://www.youtube.com/results?", params={'search_query':'rauan'})

def parse_for_all_objects(html):
    """Parses input html to find all objects of the videos"""
    result = []

