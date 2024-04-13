from moviepy.editor import VideoFileClip
import os

def play_video_segment(video_path, start_time, end_time):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Extract the specified segment
    segment_clip = video_clip.subclip(start_time, end_time)

    # Play the video segment
    segment_clip.preview()

    # Close the clips
    video_clip.close()
    segment_clip.close()

# Function to play a video by index and segment
def play_video_by_index(folder_path, index, start_time, end_time):
    video_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

    if index < 0 or index >= len(video_files):
        print("Invalid index.")
        return

    video_path = os.path.join(folder_path, video_files[index])

    # Play the segment of the video
    play_video_segment(video_path, start_time, end_time)

# Folder containing video files
video_folder = r"Videos"

# Play the video at the specified index from start time to end time
video_index = 19  # Change this to play different videos by index
start_time = 5  # Start at 5 seconds
end_time = 11  # End at 11 seconds

play_video_by_index(video_folder, video_index, start_time, end_time)
