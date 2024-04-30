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

    total_objects_count = {}  # Dictionary to store total count of objects detected

    while True:
        success, img = cap.read()
        if not success:
            break  # Break out of the loop if there are no more frames to read
        
        frame_count += 1
        
        classIds, _, bbox = net.detect(img, confThreshold=thres)

        if len(classIds) != 0:
            for classId in classIds.flatten():
                className = classNames[classId - 1].upper()
                
                # Increment the count for the detected object class
                if className in total_objects_count:
                    total_objects_count[className] += 1
                else:
                    total_objects_count[className] = 1
                
                # Draw bounding boxes and labels on the image
                for classId, box in zip(classIds.flatten(), bbox):
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(img, classNames[classId-1].upper(), (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        # Display the processed frame
        cv2.imshow("Output", img)
        cv2.waitKey(1)

    return total_objects_count

# # Example usage:
# signature = generate_video_signature('Videos\\video3.mp4')
# print("Video Signature:", signature)

# signature = generate_video_signature('QueryVideos\\video3_1_modified.mp4')
# print("Video Signature:", signature)
