import cv2
import subprocess
import tkinter as tk
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from PIL import Image, ImageTk
from pygame import mixer

def extract_subclip(index, start_time, end_time):
    # Get start and end time from the entry fields
    path = f"Videos/video{index}.mp4"

    # Extract subclip
    ffmpeg_extract_subclip(path, start_time, end_time, targetname="test.mp4")
    # Load and display the subclip
    open_file("test.mp4")

# Read the video file, load the audio file for playing
def open_file(filepath):
    global video, paused
    mixer.music.stop()
    if not filepath:
        return
    video = cv2.VideoCapture(filepath)
    audio_file = "audio.mp3"
    subprocess.run(f"ffmpeg -y -i \"{filepath}\" {audio_file}", shell=True)
    mixer.music.load(audio_file)
    mixer.music.play()
    mixer.music.pause()
    paused = True

# Function to update the video frame by frame
def video_stream():
    global paused, video, root, video_label
    if paused:
        root.after(30, video_stream) # Check if the status is updated after 30ms
        return
    is_read, frame = video.read() # Read the next frame
    if is_read:
        frame_display = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA))) # Format conversion for frame displaying
        video_label.config(image=frame_display) # Update the frame image
        video_label.image = frame_display # Keep the frame visible
    else: # Reach the end of the video, loop the media
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)   # Restart video
        mixer.music.play()  # Restart audio
        paused = False
    root.after(30, video_stream)

# Function to play/pause audio and video
def media_play_pause():
    global paused
    if paused:
        mixer.music.unpause()
    else:
        mixer.music.pause()
    paused = not paused

def player(index, start_time, end_time):
    global video, paused, root, video_label
    video = None
    paused = True # Toggle the video play/pause (not include audio)
    mixer.init() # Toggle the audio play/pause

    root = tk.Tk()
    root.title("Video Player")
    root.geometry("600x600")  # Set window dimensions (width x height)

    # Button to extract subclip and play
    extract_button = tk.Button(root, text="Extract", command=lambda: extract_subclip(index, start_time, end_time), padx=10, pady=5)
    extract_button.pack()

    video_label = tk.Label(root)
    video_label.pack(expand=True, fill="both")

    # Button to play/pause audio and video
    play_button = tk.Button(root, text="Play/Pause", command=media_play_pause, padx=10, pady=5)
    play_button.pack()

    video_stream()
    root.mainloop()

# player(1,540,570)
