import cv2
import os
import json
import numpy as np
import time

input_folder = "..\\Videos\\frames"         # Path to folder with input frames
output_folder = "..\\Videos\\database"      # Path to output folder

def load_frame(frame_name):
    img = cv2.imread(frame_name[2]) & (0b11111000)

    a2D = img.reshape(-1, img.shape[-1])
    col_range = (256, 256, 256)
    a1D = np.ravel_multi_index(a2D.T, col_range)
    
    return np.unravel_index(np.bincount(a1D).argmax(), col_range)

def main():

    videos = {}

    for i in range(1,21):
        videos["video"+str(i)] = {"red": {}, "green": {}, "blue": {}}

    for key in videos:
        for r in range(0, 256, 8):
            videos[key]["red"][str(r)] = []
        for g in range(0, 256, 8):
            videos[key]["green"][str(g)] = []
        for b in range(0, 256, 8):
            videos[key]["blue"][str(b)] = []

    count = 0
    for filename in os.listdir(input_folder):
        if count % 5000 == 0:
            print("Processing " + filename)
        video_name, frame_num = filename.split("_")
        frame_num = frame_num.split(".")[0]
        frame_name = (video_name, frame_num, os.path.join(input_folder, filename))
        frame_data = load_frame(frame_name)
        # print(frame_data)
        videos[video_name]["red"][str(frame_data[0])].append(frame_num)
        videos[video_name]["green"][str(frame_data[1])].append(frame_num)
        videos[video_name]["blue"][str(frame_data[2])].append(frame_num)
        count = count + 1
    
    # print(videos["video10"])
    for key in videos: # range(10, 11):
        with open(os.path.join(output_folder, key + ".json"), "w") as outfile:
            json.dump(videos[key], outfile)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    seconds = end - start
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    print("Runtime: %d:%02d:%02d" % (hours, minutes, seconds))