import cv2
import os

video_folder = "..\\Videos"      # Replace with path to videos folder 
video = "..\\Videos\\video1.mp4" # A single video for testing purposes

def disassemble_video(video):
    title = os.path.basename(video).split('\\')[-1].split('.')[0]
    vidcap = cv2.VideoCapture(video)
    success, image = vidcap.read()
    count = 0
    while success:
        # save frame as JPG file
        cv2.imwrite(video_folder + "\\frames\\%s_%d.jpg" % (title, count), image)
        count += 1
        success, image = vidcap.read()
        # if(count % 1000 == 0):
        #     print('Read in frame', count , success)

def load_videos(video_folder):
    images = []
    names = []
    for filename in os.listdir(video_folder + "\\frames"):
        img = cv2.imread(os.path.join(video_folder + "\\frames\\" + filename))
        name = str(filename)
        if img is not None:
            images.append(img),
            names.append(name)
    return images, names

def main():
    disassemble_video(video)

    frames = load_videos(video_folder)
    print(frames[1])

if __name__ == "__main__":
    main()
