import cv2

def generate_video_signature(video_path):
    thres = 0.45  # Threshold to detect object

    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0

    classNames = []
    classFile = 'ObjectCounter\\coco.names'  # Use double backslashes for Windows paths
    with open(classFile, 'r') as f:
        classNames = f.read().rstrip('\n').split('\n')

    configPath = 'ObjectCounter\\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'ObjectCounter\\frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    video_signature = {}  # Dictionary to store objects detected per second

    while True:
        success, img = cap.read()
        if not success:
            break  # Break out of the loop if there are no more frames to read
        
        frame_count += 1
        second = int(frame_count / frame_rate) + 1  # Calculate the current second
        
        classIds, confs, bbox = net.detect(img, confThreshold=thres)

        frame_objects = {}  # Dictionary to store objects detected in the current frame
        
        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                className = classNames[classId - 1].upper()
                
                # Add the detected object and its confidence to the dictionary
                if className in frame_objects:
                    frame_objects[className].append(confidence)
                else:
                    frame_objects[className] = [confidence]
                
                # Draw bounding boxes and labels on the image
                cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                cv2.putText(img, className, (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (0, 255, 0), 2)

        # Update the video signature with objects detected in the current second
        video_signature[second] = frame_objects

        # Display the processed frame
        cv2.imshow("Output", img)
        cv2.waitKey(1)

    return video_signature

# Example usage:
# video_path = 'ObjectCounter\\test.mp4'
# signature = generate_video_signature(video_path)
# print("Video Signature:", signature)
