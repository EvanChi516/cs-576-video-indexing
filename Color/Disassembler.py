import cv2
import os

# video = "..\\Videos\\video1.mp4"          # A single video for testing purposes
video_folder = "..\\Videos"                 # Path to folder with input videos
frames_folder = "..\\Videos\\frames"        # Path to folder with output frames

def disassemble_video(video):
    title = os.path.basename(video).split('\\')[-1].split('.')[0]
    vidcap = cv2.VideoCapture(video)
    success, image = vidcap.read()
    count = 0
    while success:
        # save frame as JPG file
        cv2.imwrite(frames_folder + "\\%s_%d.jpg" % (title, count), image)
        count += 1
        success, image = vidcap.read()
        # if(count % 1000 == 0):
        #     print('Read in frame', count , success)

def main():

    for filename in os.listdir(video_folder):
        if filename.split('.')[-1] == "mp4":
            disassemble_video(video_folder + "\\" + filename)

if __name__ == "__main__":
    main()
