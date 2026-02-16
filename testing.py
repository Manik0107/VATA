import json

def find_text_fields(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "text" and isinstance(v, str):
                print(v)
            find_text_fields(v)
    elif isinstance(obj, list):
        for item in obj:
            find_text_fields(item)

with open("/Users/manikmanavenddram/VATA/output/linear_regression_notes.json") as f:
    data = json.load(f)

find_text_fields(data)