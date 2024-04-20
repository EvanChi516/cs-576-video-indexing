import cv2
import numpy as np
from ffpyplayer.player import MediaPlayer
import os
import tkinter as tk

class VideoPlayer:
    def __init__(self, video_folder, video_index, start_time, end_time, master = None):
        self.video_folder = video_folder
        self.video_index = video_index
        self.start_time = start_time
        self.end_time = end_time
        self.master = master

    def get_video_source(self, source, width, height):
        cap = cv2.VideoCapture(source)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        return cap

    def play_video(self):
        video_files = [f for f in os.listdir(self.video_folder) if f.endswith('.mp4')]
        
        if self.video_index < 0 or self.video_index >= len(video_files):
            print("Invalid video index.")
            return
        
        source_path = os.path.join(self.video_folder, video_files[self.video_index])
        camera = self.get_video_source(source_path, 720, 480)
        player = MediaPlayer(source_path)
        
        frame_rate = camera.get(cv2.CAP_PROP_FPS)
        start_frame = int(self.start_time * frame_rate)
        end_frame = int(self.end_time * frame_rate)

        # Seek video and audio to start frames
        camera.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        player.seek(self.start_time)

        while True:
            ret, frame = camera.read()
            audio_frame, val = player.get_frame()
        
            if not ret or camera.get(cv2.CAP_PROP_POS_FRAMES) >= end_frame:
                print("End of video")
                break

            if camera.get(cv2.CAP_PROP_POS_FRAMES) >= start_frame:
                frame = cv2.resize(frame, (720, 480))
                cv2.imshow('Camera', frame)

            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    video_folder = r"Videos"
    video_index = 10  # Change this to play different videos by index
    start_time = 1   # Start time in seconds
    end_time = 30    # End time in seconds

    # root = tk.Tk()
    # root.geometry("800x500")
    # root.title("Video Player")
    # frame = tk.Frame(root, bg="black")
    # frame.pack(expand=True, fill="both")
    
    video_player = VideoPlayer(video_folder, video_index, start_time, end_time)
    video_player.play_video()

    # root.mainloop()

