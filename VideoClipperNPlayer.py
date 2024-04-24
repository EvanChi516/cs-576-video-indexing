import cv2
import subprocess
import tkinter as tk
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from PIL import Image, ImageTk
from pygame import mixer

def extract_subclip():
    # Get start and end time from the entry fields
    index = 18
    start_time = 5
    end_time = 20
    path = "Videos/video"+str(index)+".mp4"

    # Extract subclip
    ffmpeg_extract_subclip(path, start_time, end_time, targetname="test.mp4")
    # Load and display the subclip
    open_file("test.mp4")

# read the video file, load the audio file for playing
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

# Update the video frame by frame
def video_stream():
    global paused
    if paused:
        root.after(30, video_stream) # check if the status is updated after 30ms
        return
    is_read, frame = video.read() # read the next frame
    if is_read:
        frame_display = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA))) # format conversion for frame dispalying
        video_label.config(image=frame_display) # update the frame image
        video_label.image = frame_display # keep the frame visible
    else: # reach the end of the video, loop the media
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)   # restart video
        mixer.music.play()  # restart audio
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


video = None
paused = True # toggle the video play/pause (not inlucde audio)
mixer.init() # toggle the audio play/pause

root = tk.Tk()
root.title("Video Player")
root.geometry("600x600")  # Set window dimensions (width x height)

# Button to extract subclip and play
extract_button = tk.Button(root, text="Extract", command=extract_subclip, padx=10, pady=5)
extract_button.pack()

video_label = tk.Label(root)
video_label.pack(expand=True, fill="both")

# Button to play/pause audio and video
play_button = tk.Button(root, text="Play/Pause", command=media_play_pause, padx=10, pady=5)
play_button.pack()

video_stream()
root.mainloop()
