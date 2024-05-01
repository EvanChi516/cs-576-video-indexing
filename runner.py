
import sys
from findQueryAudio import process_query
from VideoClipperNPlayer import player

def main(query_video, query_audio):

    #audio proceesing method
    database_path = 'audio_mfcc_database.pkl'
    index, start_time, end_time = process_query(query_audio,database_path)
    player(index, start_time, end_time)

    pass

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python your_script.py query_video query_audio")
        sys.exit(1)
    
    # Extract command-line arguments/
    video_path = sys.argv[1]
    query_path = sys.argv[2]
    
    # Call the main function with the provided arguments
    main(video_path, query_path)