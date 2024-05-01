import librosa
import pickle
from scipy.spatial import distance

def extract_features(audio_path, sr=None):
    '''
    Extracts MFCC features from an audio file.
    '''
    audio, sr = librosa.load(audio_path, sr=sr)
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=20, hop_length=int(0.10*sr), n_fft=int(0.025*sr))
    return mfccs, sr

def load_audio_database(pkl_path):
    '''
    Loads the MFCC database from a pickle file.
    '''
    with open(pkl_path, 'rb') as f:
        database = pickle.load(f)
    return database

def find_best_match(query_mfcc, database, level):
    '''
    Finds the best matching audio in the database for the given query MFCC.
    level: 
        The number of coefficients being used to find the best match
        value can be 1, 2, ..., 20. 
    '''
    best_score = float('inf')
    best_match = None
    best_idx = None
    
    for key, data in database.items():
        ref_mfcc = data['mfccs']
        # Calculate distance between query and reference MFCC
        query_mfcc_first_two_coeffs = query_mfcc[0:level]  # Selecting the first [level] of coefficients
        for i in range(ref_mfcc.shape[1] - query_mfcc.shape[1] + 1):
            ref_segment_first_two_coeffs = ref_mfcc[0:level, i:i+query_mfcc.shape[1]]  # Selecting the first [level] of coefficients for the segment
            # Calculate the Euclidean distance on the flattened array of these two coefficients
            dist = distance.euclidean(query_mfcc_first_two_coeffs.flatten(), ref_segment_first_two_coeffs.flatten())
            if dist < best_score:
                best_score = dist
                best_match = key
                best_idx = i
    
    return best_match, best_idx, best_score

def query_audio_time(start_frame, sr, hop_length):
    '''
    Converts a frame index to time.
    '''
    return start_frame * hop_length / sr

def process_query(query_audio_path, database_path):
    # Load the database
    database = load_audio_database(database_path)
    
    # Extract features from the query audio
    query_mfcc, sr = extract_features(query_audio_path)
    
    # Find the best match
    match_index, frame_index, score = find_best_match(query_mfcc, database, 2)
    
    # Calculate the start and end times of the matched segment
    start_time = int(query_audio_time(frame_index, sr, int(0.10*sr)))
    end_time = int(query_audio_time(frame_index + query_mfcc.shape[1], sr, int(0.10*sr)))
    
    print(f"Video Index: {match_index + 1}")

    print(f"Start Time: {start_time:.2f} sec")
    start_min = int(start_time // 60)
    start_sec = int(start_time % 60)
    print(f"Start Timestamp: {start_min} min {start_sec} sec")
    # print(f"End Time: {end_time:.2f} sec")
    print(f"Duration: {end_time - start_time} sec")
    print(f"Start Frame: {int(start_time*30)} frame")

    match_index += 1

    return match_index, start_time, end_time
    # sec min format
    
    # end_min = int(end_time // 60)
    # end_sec = int(end_time % 60)
    # print(f"End Time: {end_min} min {end_sec} sec")

# Example usage
# process_query('QueryAudios\\video1_1_modified.wav', 'AudioMFCCs\\audio_mfcc_database.pkl')
