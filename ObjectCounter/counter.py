import cv2

thres = 0.45 # Threshold to detect object

cap = cv2.VideoCapture('ObjectCounter\\test.mp4')
cap.set(3,1280)
cap.set(4,720)
cap.set(10,70)

classNames= []
classFile = 'ObjectCounter\\coco.names'  # Use double backslashes for Windows paths
with open(classFile,'r') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ObjectCounter\\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'ObjectCounter\\frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

video_signature = []

while True:
    success,img = cap.read()
    if not success:
        break  # Break out of the loop if there are no more frames to read
    
    classIds, confs, bbox = net.detect(img,confThreshold=thres)

    frame_classes = []  # List to store class names for the current frame

    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId-1].upper()
            frame_classes.append(className)  # Add class name to the list
            cv2.rectangle(img,box,color=(0,255,0),thickness=2)
            cv2.putText(img, className, (box[0]+10,box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            cv2.putText(img, str(round(confidence*100,2)), (box[0]+200,box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)

    # Append the list of class names for the frame to the video signature
    video_signature.append(frame_classes)

    cv2.imshow("Output",img)
    cv2.waitKey(1)

# Print the video signature after the video ends
print("Video Signature:", video_signature)

# def encode_video_signature(video_signature):
#     encoded_string = ""
#     consecutive_blanks = 0
#     frame_number = 1  # Start with frame number 1
    
#     for frame_classes in video_signature:
#         if not frame_classes:  # Check if the frame is blank
#             consecutive_blanks += 1
#         else:
#             if consecutive_blanks > 0:
#                 encoded_string += f"{consecutive_blanks} BLANK "
#                 consecutive_blanks = 0
            
#             frame_dict = {}
#             for item in frame_classes:
#                 if item in frame_dict:
#                     frame_dict[item] += 1
#                 else:
#                     frame_dict[item] = 1

#             for item, count in frame_dict.items():
#                 encoded_string += f"{frame_number}:{count} {item} "  # Include frame number

#         frame_number += 1

#     # Add the count of consecutive blank frames at the end if there are any
#     if consecutive_blanks > 0:
#         encoded_string += f"{consecutive_blanks} BLANK "

#     return encoded_string.strip()

# print(encode_video_signature(video_signature))