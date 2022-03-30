import jsonlines
import os
import re

from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from datetime import datetime

# pip install -U spacy
# python -m spacy download en_core_web_lg
import spacy

def get_date_from_fa(fa_string):
    try:
        date = parse(fa_string, fuzzy_with_tokens=True)[0]

        if date.month == datetime.now().month and date.day == datetime.now().day:
            return date.strftime("%Y")

        elif date.day == datetime.now().day:
            return date.strftime("%B %Y")

        else:
            return date.strftime("%d %B %Y")
        return parse(fa_string, fuzzy_with_tokens=True)[0].strftime("%Y")
    except ParserError:
        return ""
    
    
def get_names_from_fa(fa_string, nlp_model):
    
    doc = nlp_model(fa_string)
    entities = []
    labels = []
    position_start = []
    position_end = []

    persons = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
    
    return persons

# Load NLP model
nlp_model = spacy.load("en_core_web_lg")

# Path to directory containing route jsonline files
path_to_routes = "<PATH_TO_DATA>"

print(f"Looking in {path_to_routes}")

# Get all files in dir
files = os.listdir(path_to_routes)

# Filter to just routes files (xx-routes.jsonlines)
r_routes = re.compile("[a-z]{2}-routes.jsonlines")

# Iterate over generator returned by filter function
for file in filter(r_routes.match, files):

    # Get absolute path to routes files
    path = os.path.join(path_to_routes, file)

    # open JSONlines file and iterate
    with jsonlines.open(path, mode="r") as f:

        print(f)

        # Convert reader object to a list for the starting dataset
        route_data = []

        for route in f:
            route_data.append(route)
            print(route["fa"])
            
            names = get_names_from_fa(route["fa"], nlp_model)
            date = get_date_from_fa(route["fa"])
            print(f"{names=},{date=}\n")

            route_data[-1]["fa_2"] = [names, date]

    # Write back to JSONlines object
    with jsonlines.open(path, mode="w") as f:
        for route in route_data:
            f.write(route)
