import os
import json
import ezdxf

def extract_entities(msp):
    entities = []
    for entity in msp.query('INSERT LINE TEXT POLYLINE POINT'):
        entity_data = {
            'type': entity.dxftype(),
            'handle': entity.dxf.handle,
        }
        if entity.dxftype() == 'INSERT':
            block = msp.doc.blocks.get(entity.dxf.name)
            entity_data['block_entities'] = extract_entities(block) if block else []
        if entity.dxftype() == 'POLYLINE':
            entity_data['points'] = [list(vertex.dxf.location) for vertex in entity.vertices]
        entities.append(entity_data)
    return entities

def process_dxf(dxf_path):
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    entities = extract_entities(msp)
    return {'entities': entities}

def main(dxf_folder, output_folder, final_output_folder):
    for dxf_filename in os.listdir(dxf_folder):
        if dxf_filename.endswith('.dxf'):
            name = os.path.splitext(dxf_filename)[0]
            dxf_path = os.path.join(dxf_folder, dxf_filename)
            output_path = os.path.join(output_folder, f"{name}_processed.json")
            data = process_dxf(dxf_path)
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=4)
    combine_outputs(output_folder, final_output_folder)

def combine_outputs(output_folder, final_output_folder):
    combined_output = {'entities': []}
    for output_filename in os.listdir(output_folder):
        if output_filename.endswith('_processed.json'):
            output_path = os.path.join(output_folder, output_filename)
            with open(output_path, 'r') as f:
                data = json.load(f)
                combined_output['entities'].extend(data.get('entities', []))
    final_output_path = os.path.join(final_output_folder, 'final_combined_output.json')
    with open(final_output_path, 'w') as f:
        json.dump(combined_output, f, indent=4)

# Define paths
dxf_folder = "/home/manny/Documents/Python/PythonProject12/DXFtoJSON/Dataset"
output_folder = "/home/manny/Documents/Python/PythonProject12/DXFtoJSON/JSON_Output"
final_output_folder = "/home/manny/Documents/Python/PythonProject12/DXFtoJSON/JSON_Output"

if __name__ == "__main__":
    main(dxf_folder, output_folder, final_output_folder)
