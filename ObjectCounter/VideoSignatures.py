import os
import json
import numpy as np  # Import numpy for data type conversion
from counter import generate_video_signature  # Import the function from the file where it's defined

# Path to the directory containing the video files
video_dir = 'Videos'

# Dictionary to store video signatures
database_signatures = {}

# Iterate over each video file in the directory
for video_file in os.listdir(video_dir):
    if video_file.endswith('.mp4'):  # Assuming all video files have the extension .mp4
        video_path = os.path.join(video_dir, video_file)
        signature = generate_video_signature(video_path)
        
        # Convert values to strings
        signature = {key: {k: [str(val) for val in v] if isinstance(v, np.ndarray) else str(v) for k, v in value.items()} 
                     for key, value in signature.items()}
        
        database_signatures[video_file] = signature

# Save the database signatures to a JSON file
output_file = 'ObjectCounter\\database_signatures.json'
with open(output_file, 'w') as f:
    json.dump(database_signatures, f)

print(f"Database signatures saved to {output_file}")
