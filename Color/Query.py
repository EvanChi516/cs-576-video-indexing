import cv2
import os
import json
import numpy as np

query_video = "..\\Queries\\video2_1_modified.mp4"
database_folder = "..\\Videos\\database"

def get_color(vidcap):
    success, image = vidcap.read()
    if success:
        image = image & (0b11111000)
        r_img = image.reshape(-1, image.shape[-1])
        col_range = (256, 256, 256)
        rmi = np.ravel_multi_index(r_img.T, col_range)
        # Returns most common color
        return np.unravel_index(np.bincount(rmi).argmax(), col_range)

def get_frames(video, color):
    video_data = json.load(open(video))
    red_frames = video_data["red"][str(color[0])]
    green_frames = video_data["green"][str(color[1])]
    blue_frames = video_data["blue"][str(color[2])]
    return set(red_frames) & set(green_frames) & set(blue_frames)

def main():
    video = database_folder + "\\video2.json"
    vidcap = cv2.VideoCapture(query_video)

    color = get_color(vidcap)
    print(color)

    frames = get_frames(video, color)
    print(sorted(frames))

if __name__ == "__main__":
    main()