import cv2
import numpy as np

def compute_motion_statistics(video_path):
    cap = cv2.VideoCapture(video_path)
    prev_frame = None
    motion_statistics = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if prev_frame is not None:
            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

            # Calculate magnitude of optical flow vectors
            magnitude = np.sqrt(flow[..., 0] ** 2 + flow[..., 1] ** 2)

            # Compute motion statistics for the frame
            motion_stat = np.mean(magnitude)  # Example: Average magnitude of motion
            motion_statistics.append(motion_stat)

        prev_frame = frame

    cap.release()
    return motion_statistics

def main():
    video_path = "test.mp4"  # Replace with path to your video file
    motion_stats = compute_motion_statistics(video_path)
    print("Motion statistics:", motion_stats)

if __name__ == "__main__":
    main()
