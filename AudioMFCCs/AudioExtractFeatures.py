import librosa #to install, run pip install librosa numpy
import numpy as np
import pickle


def extract_features(audio_path):
    '''
    Get mfcc coefficients of an audio
    mfcc data is stored in a NumPy 2D array, whose
    Rows: 
        mfcc coefficients from low to high order, 20
    Columns: 
        mfcc coefficients from the beginning of an audio to the end
    '''
    audio, sr = librosa.load(audio_path, sr=None)
    # n_mfcc: number of mfcc coefficient per sample
    # hop_length: sample rate
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=20, hop_length=int(0.10*sr), n_fft=int(0.025*sr))
    return mfccs, sr


def save_audio_feature_to_file(audio_paths, pkl_path):
    '''
    Save mfcc coefficients of all audio files into a pkl file
    using a list of dictionaries
    '''
    database = {}
    for i in range(20):
        print(f"Processing {audio_paths[i]}")
        mfccs, sr = extract_features(audio_paths[i])
        database[i] = {
            'mfccs': mfccs,
            'sr': sr, 
            'timestamps': librosa.frames_to_time(np.arange(mfccs.shape[1]), sr=sr, hop_length=int(0.10*sr))
        }
    with open(pkl_path, 'wb') as f:
        pickle.dump(database, f)
    print("All files processed and data saved in ", pkl_path)

# file paths to the audio files. video7_44.1k.wav is ignored here
audio_paths = []
for i in range(20):
    audio_paths.append("Audios/video"+str(i+1)+".wav")

save_audio_feature_to_file(audio_paths, 'AudioMFCCs\\audio_mfcc_database.pkl')