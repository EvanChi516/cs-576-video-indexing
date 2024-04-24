"""
This is not needed for preprocessing

This is a helper program to better understand the structure of 'audio_database.pkl'
"""
import pickle

# Read the feature database
data_file_path = 'audio_mfcc_database.pkl'   # Path where the pickle file is stored
# Read the list of dictionaries from the file using pickle
with open(data_file_path, 'rb') as file:
    loaded_data = pickle.load(file)
print("Data successfully loaded from", data_file_path)

audio_file_paths = []
for i in range(20):
    audio_file_paths.append("Audios/video"+str(i+1)+".wav")

for i in range(20):
    mfccs = loaded_data[i]["mfccs"]
    sr = loaded_data[i]["sr"]
    timestamps = loaded_data[i]["timestamps"]
    length = len(mfccs[0])
    print(audio_file_paths[i], " length:", length, " sample rate:", sr, " audio duration:", timestamps[length-1])