import json
from counter import generate_video_signature
import numpy as np


def find_best_match(signature1, signature2):
    max_match_count = 0
    best_start_index = -1
    best_end_index = -1

    for i in range(len(signature1) - len(signature2) + 1):
        match_count = sum(1 for a, b in zip(signature1[i:i+len(signature2)], signature2) if a == b)
        if match_count > max_match_count:
            max_match_count = match_count
            best_start_index = i
            best_end_index = i + len(signature2) - 1

    return best_start_index, best_end_index, max_match_count

def find_query_video(video_path):
    json_file = 'ObjectCounter\\database_signatures_1.json'
    query_video_signature = generate_video_signature(video_path)
    
    # Load the JSON file
    with open(json_file, 'r') as f:
        database_signatures = json.load(f)
    
    # Iterate over each video in the database signatures
    for video, signatures in database_signatures.items():
        print(video)
        start_second, end_second, match_count = find_best_match(signatures, query_video_signature)
        print(start_second, end_second, match_count)
    

# Example usage:

# object_confidence = str({"TV": "[0.56387335]"})  # Example objects and confidence levels as strings
# print(object_confidence)
# start_second, end_second, video_name = find_video_with_objects(json_file, object_confidence)
# print("Start Second:", start_second)
# print("End Second:", end_second)
# print("Video Name:", video_name)

#testing on video clip from the database
find_query_video('ObjectCounter\\test.mp4')


#testing on video clip from Query Video Database
find_query_video('QueryVideos\\video1_1_modified.mp4')
