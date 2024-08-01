import json
import matplotlib.pyplot as plt

# Load the JSON file
with open('/home/manny/Documents/Python/PythonProject12/DXFtoJSON/JSON_Output/FlFrTrouser_Size34_FRONT_processed.json') as f:
    data = json.load(f)

# Initialize a plot
fig, ax = plt.subplots()

# Example: Iterate over line entities
for entity in data['entities']:
    if entity['type'] == 'LINE':
        start = entity['start']
        end = entity['end']
        ax.plot([start['x'], end['x']], [start['y'], end['y']], 'k-')  # Plot a black line

# Example: Plot points
for entity in data['entities']:
    if entity['type'] == 'POINT':
        point = entity['location']
        ax.plot(point['x'], point['y'], 'ro')  # Plot a red point

# Set equal scaling
ax.set_aspect('equal', 'box')

# Zoom out to view a larger area
ax.set_xlim(-500, 500)  # Adjust these values based on your data range
ax.set_ylim(-500, 500)  # Adjust these values based on your data range

plt.show()
