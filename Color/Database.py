import cv2
import os
import json

frames_folder = "..\\Videos\\frames"        # Path to folder with input frames
output_file = "..\\Videos\\frames.json"     # Path to output file

def load_videos(frames_folder):
    images = []
    names = []
    for filename in os.listdir(frames_folder):
        img = cv2.imread(os.path.join(frames_folder + "\\" + filename))
        name = str(filename)
        if img is not None:
            images.append(img),
            names.append(name)
    return images, names

def create_database():
    pass

def main():
    # frames = load_videos(frames_folder)

    database = {"test" : "hello world"}

    with open(output_file, "w") as outfile:
        outfile.write(database)

if __name__ == "__main__":
    main()
