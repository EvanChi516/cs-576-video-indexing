import json
from counter import generate_video_signature
import numpy as np

def find_video_with_objects(json_file, object_confidence):
    # Load the JSON file
    with open(json_file, 'r') as f:
        database_signatures = json.load(f)
    
    # Initialize variables to store the start and end seconds and the respective video
    start_second = None
    video_name = None
    
    # Iterate over each video in the database signatures
    for video, signatures in database_signatures.items():
        # Iterate over each second in the video signatures
        for second, objects_detected in signatures.items():
            # Check if the objects detected string matches the given object confidence string
            if str(objects_detected) == object_confidence:
                start_second = int(second)
                video_name = video
                break  # Exit the loop once a match is found
    
    return start_second, video_name


def find_query_video(video_path):
    json_file = 'ObjectCounter\\database_signatures.json'
    query_video_signature = generate_video_signature(video_path)
    
    # Convert values to strings
    query_video_signature = {key: {k: [str(val) for val in v] if isinstance(v, np.ndarray) else str(v) for k, v in value.items()} 
                     for key, value in query_video_signature.items()}
    
    for item in query_video_signature.items():
        print(item)
        start_second, video_name = find_video_with_objects(json_file, str(item[1]))
        print("Second: "+ str(start_second) +" Video Name: "+ str(video_name))
    pass

# Example usage:

# object_confidence = str({"TV": "[0.56387335]"})  # Example objects and confidence levels as strings
# print(object_confidence)
# start_second, end_second, video_name = find_video_with_objects(json_file, object_confidence)
# print("Start Second:", start_second)
# print("End Second:", end_second)
# print("Video Name:", video_name)

find_query_video('ObjectCounter\\test.mp4')