"""
This is not needed for preprocessing

A helper program to 
1. show how to get audio feature data from the pkl file
2. better understand the structure of 'audio_database.pkl'
"""
import librosa
import librosa.display
import matplotlib.pyplot as plt # to install, use pip install matplotlib
import pickle

# Read the feature database
data_file_path = 'audio_mfcc_database.pkl'   # Path where the pickle file is stored
# Read the list of dictionaries from the file using pickle
with open(data_file_path, 'rb') as file:
    loaded_data = pickle.load(file)
print("Data successfully loaded from", data_file_path)

# change this to visualize different audio file's features
index = int(input("Enter an index here (0 represents Video 1): "))

mfccs = loaded_data[index]["mfccs"]
sample_rate = loaded_data[index]["sr"]
timestamps = loaded_data[index]['timestamps']

# plot the feature
plt.figure(figsize=(10, 4))
librosa.display.specshow(mfccs, sr=sample_rate, x_axis='time', x_coords=timestamps)
plt.colorbar(label='MFCC amplitude')
plt.title('MFCCs over time')
plt.xlabel('Time (seconds)')
plt.ylabel('MFCC Coefficients')
plt.show()