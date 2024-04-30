import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Load your audio file
audio = AudioSegment.from_wav("Audios/video1.wav")

# Split the audio file into chunks on silence for better accuracy
chunks = split_on_silence(audio, min_silence_len=500, silence_thresh=audio.dBFS-14, keep_silence=500)

# Initialize the recognizer
recognizer = sr.Recognizer()

def recognize_speech_from_audio_chunk(chunk, start_time):
    # Export the audio chunk to a wav file
    chunk.export("temp_chunk.wav", format="wav")
    
    # Use the speech_recognition library to convert speech to text
    with sr.AudioFile("temp_chunk.wav") as source:
        audio_listened = recognizer.record(source)
        # Recognize the speech in the chunk
        try:
            text = recognizer.recognize_google(audio_listened)
            return f"Start Time: {start_time} - Text: {text}"
        except sr.UnknownValueError:
            return f"Start Time: {start_time} - Text: Speech could not be understood"
        except sr.RequestError:
            return f"Start Time: {start_time} - Text: API unavailable"

# Process each chunk
results = []
current_time = 0
for chunk in chunks:
    result = recognize_speech_from_audio_chunk(chunk, current_time)
    results.append(result)
    current_time += len(chunk) / 1000  # Update the start time by adding the duration of the current chunk

for result in results:
    print(result)