import cv2
import os

video_folder = "..\\Videos"      #Replace with path to videos folder 
video = "..\\Videos\\video1.mp4"


def disassemble_video(video):
    title = video.str
    vidcap = cv2.VideoCapture(video)
    success, image = vidcap.read()
    count = 0
    success = True
    while success:
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        # save frame as JPEG file
        cv2.imwrite("/path/to/video_extract/frame&%d&%s.jpg" % count, title, image)    
        count += 1

def load_videos(video_folder):
    images = []
    names = []
    for filename in os.listdir(video_folder):
        img = cv2.imread(os.path.join(video_folder, filename))
        name = str(filename)
        if img is not None:
            images.append(img),
            names.append(name)
    return images, names

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()
