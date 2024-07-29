import os
import json
import pandas as pd

def label_and_combine_json_files(input_dir, output_file):
    combined_data = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(input_dir, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                
                label = os.path.splitext(filename)[0]  # Extract the file name without extension
                labeled_data = {"label": label, "entities": data.get("entities", [])}
                
                combined_data.append(labeled_data)

    with open(output_file, 'w') as outfile:
        json.dump(combined_data, outfile, indent=4)

    return combined_data

def flatten_json(combined_data, output_csv):
    flat_data = []
    
    for item in combined_data:
        label = item["label"]
        entities = item["entities"]
        
        for entity in entities:
            flat_entity = {"label": label}
            flat_entity.update(entity)
            flat_data.append(flat_entity)
    
    df = pd.json_normalize(flat_data)
    df.to_csv(output_csv, index=False)

input_directory = "/home/manny/Documents/Python/PythonProject12/DXFtoJSON/JSON_Output"  # Change this to your actual input directory
combined_json_output = "/home/manny/Documents/Python/PythonProject12/DXFtoJSON/JSON_Output/combined_data.json"
flattened_csv_output = "/home/manny/Documents/Python/PythonProject12/DXFtoJSON/JSON_Output/flattened_data.csv"

combined_data = label_and_combine_json_files(input_directory, combined_json_output)
flatten_json(combined_data, flattened_csv_output)

print("JSON files combined and labeled. Output saved to:", combined_json_output)
print("Flattened data saved to:", flattened_csv_output)
