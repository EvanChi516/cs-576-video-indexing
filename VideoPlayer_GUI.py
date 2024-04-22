import datetime
import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
from ffpyplayer.player import MediaPlayer


def update_duration(event):
    """ updates the duration after finding the duration """
    duration = vid_player.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration


def update_scale(event):
    """ updates the scale value """
    progress_value.set(vid_player.current_duration())


def load_video():
    """ loads the video """
    file_path = "__temp__.mp4"

    if file_path:
        vid_player.load(file_path)

        # Load video file with ffpyplayer
        global player
        player = MediaPlayer(file_path)
        player.set_pause(True)

        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)


def seek(value):
    """ used to seek a specific timeframe """
    vid_player.seek(int(value))
    player.set_time(int(value * 1000))  # Set time in milliseconds for ffpyplayer


def skip(value: int):
    """ skip seconds """
    vid_player.seek(int(progress_slider.get()) + value)
    player.set_time(int(progress_slider.get() + value) * 1000)  # Set time in milliseconds for ffpyplayer
    progress_value.set(progress_slider.get() + value)


def play_pause():
    """ pauses and plays """
    player.set_mute
    if vid_player.is_paused():
        vid_player.play()
        player.set_pause(False)
        play_pause_btn["text"] = "Pause"

    else:
        vid_player.pause()
        player.set_pause(True)
        play_pause_btn["text"] = "Play"


def video_ended(event):
    """ handle video ended """
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)


root = tk.Tk()
root.title("Tkinter media")

load_btn = tk.Button(root, text="Load", command=load_video)
load_btn.pack()

vid_player = TkinterVideo(scaled=True, master=root)
vid_player.pack(expand=True, fill="both")

play_pause_btn = tk.Button(root, text="Play", command=play_pause)
play_pause_btn.pack()

start_time = tk.Label(root, text=str(datetime.timedelta(seconds=0)))
start_time.pack(side="left")

progress_value = tk.IntVar(root)

progress_slider = tk.Scale(root, variable=progress_value, from_=0, to=0, orient="horizontal", command=seek)
progress_slider.pack(side="left", fill="x", expand=True)

end_time = tk.Label(root, text=str(datetime.timedelta(seconds=0)))
end_time.pack(side="left")

vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<SecondChanged>>", update_scale)
vid_player.bind("<<Ended>>", video_ended)



root.mainloop()
