import cv2
import os

video_folder = "..\\Videos"      # Replace with path to videos folder 
video = "..\\Videos\\video1.mp4" # A single video for testing purposes

def disassemble_video(video):
    title = video
    vidcap = cv2.VideoCapture(video)
    success, image = vidcap.read()
    count = 0
    while success:
        # save frame as JPG file
        cv2.imwrite(video_folder + "\\frames\\%s&%d.jpg" % (title, count), image)
        count += 1
        success, image = vidcap.read()
        # if(count % 1000 == 0):
        #     print('Read in frame', count , success)

def load_videos(video_folder):
    images = []
    names = []
    for filename in os.listdir(video_folder+"\\frames"):
        img = cv2.imread(os.path.join(video_folder, filename))
        name = str(filename)
        if img is not None:
            images.append(img),
            names.append(name)
    return images, names

def main():
    disassemble_video(video)

    vidcap = cv2.VideoCapture(video)
    success, image = vidcap.read()
    cv2.imwrite(video_folder + "\\frames\\test.jpg", image)
    
    # frames = load_videos(video_folder)
    # print(frames[1])

if __name__ == "__main__":
    main()
