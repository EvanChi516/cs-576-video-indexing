# Import everything needed to edit video clips 
from moviepy.editor import *
   
# loading video gfg 
video_index = 8
start_time = 5
end_time = 20


clip = VideoFileClip("Videos/video"+str(video_index)+".mp4") 
# getting only first 5 seconds  
clip = clip.subclip(start_time, end_time)  

   
# showing  clip  
clip.ipython_display(width = 360)