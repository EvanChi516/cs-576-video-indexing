import datetime
import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from ffpyplayer.player import MediaPlayer

# Function to extract subclip
def extract_subclip():
    global vid_player, audio_player, end_time
    
    # Get start and end time from the entry fields
    index = 1
    start_time = 1
    end_time = 10
    path = "Videos/video"+str(index)+".mp4"

    # Initialize audio player
    audio_player = MediaPlayer("test.mp4")
    
    # Extract subclip
    ffmpeg_extract_subclip(path, start_time, end_time, targetname="test.mp4")
    
    # Load and display the subclip
    vid_player.load("test.mp4")
    vid_player.play()
    
    

# Function to play/pause audio and video
def play_media():
    global vid_player, audio_player
    audio_player.toggle_pause()
    if vid_player.is_paused():
        vid_player.play()
    else:
        vid_player.pause()
        

# Create the Tkinter window with specified dimensions
root = tk.Tk()
root.title("Tkinter Media Player")
root.geometry("800x600")  # Set window dimensions (width x height)

# Button to extract subclip and play
extract_button = tk.Button(root, text="Extract and Play", command=extract_subclip, padx=10, pady=5)
extract_button.pack()

# Create the TkinterVideo player
vid_player = TkinterVideo(scaled=True, master=root)
vid_player.pack(expand=True, fill="both")

# Button to play/pause audio and video
play_audio_button = tk.Button(root, text="Play/Pause", command=play_media, padx=10, pady=5)
play_audio_button.pack()

# Start the Tkinter event loop
root.mainloop()
