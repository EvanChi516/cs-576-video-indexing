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
    objects_per_second = {}  # Dictionary to store object counts per second
    video_signature = []  # List to store video signature

    while True:
        success, img = cap.read()
        if not success:
            break  # Break out of the loop if there are no more frames to read
        
        frame_count += 1
        current_second = int(frame_count / frame_rate)

        classIds, _, bbox = net.detect(img, confThreshold=thres)

        if len(classIds) != 0:
            for classId in classIds.flatten():
                className = classNames[classId - 1].upper()
                
                # Increment the count for the detected object class
                if className in total_objects_count:
                    total_objects_count[className] += 1
                else:
                    total_objects_count[className] = 1
                
                # Update object counts per second
                if current_second in objects_per_second:
                    if className in objects_per_second[current_second]:
                        objects_per_second[current_second][className] += 1
                    else:
                        objects_per_second[current_second][className] = 1
                else:
                    objects_per_second[current_second] = {className: 1}
                
                # Draw bounding boxes and labels on the image
                for classId, box in zip(classIds.flatten(), bbox):
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(img, classNames[classId-1].upper(), (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                # Update video signature
                if current_second >= len(video_signature):
                    video_signature.extend([0] * (current_second - len(video_signature) + 1))
                video_signature[current_second] = classNames[classId-1].upper()

        # Display the processed frame
        cv2.imshow("Output", img)
        cv2.waitKey(1)

    # Fill remaining seconds with 0 if no object detected
    for i in range(len(video_signature), int(frame_count / frame_rate) + 1):
        video_signature.append(0)

    # Find the most observed object per second
    most_observed_per_second = {}
    for second, counts in objects_per_second.items():
        most_observed_per_second[second] = max(counts, key=counts.get)

    return video_signature


# # Example usage:
# signature1 = generate_video_signature('Videos\\Video3.mp4')
# print("Video Signature:", signature1)

# signature2 = generate_video_signature('QueryVideos\\video3_1_modified.mp4')
# print("Video Signature:", signature2)


# signature1= ['PERSON', 'PERSON', 'SURFBOARD', 'REFRIGERATOR', 'BOOK', 'REFRIGERATOR', 'VASE', 'PERSON', 'BOWL', 'PERSON', 'PERSON', 'WINE GLASS', 'BOOK', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'TOOTHBRUSH', 'PERSON', 'PERSON', 'BOTTLE', 'HANDBAG', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'BOTTLE', 'PERSON', 'SPORTS BALL', 'HANDBAG', 'HANDBAG', 'PERSON', 'HANDBAG', 'CHAIR', 'PERSON', 'PERSON', 'PERSON', 'BICYCLE', 'SUITCASE', 'HANDBAG', 'HANDBAG', 'CUP', 'PERSON', 'HANDBAG', 'PERSON', 'DINING TABLE', 'PERSON', 'PERSON', 'DONUT', 'DONUT', 'PERSON', 'PERSON', 'CHAIR', 'CHAIR', 'BOWL', 'PERSON', 'PERSON', 'CUP', 'DONUT', 'BOWL', 'CHAIR', 'CHAIR', 'BOWL', 'PERSON', 'CUP', 'CHAIR', 'PERSON', 'CUP', 'DONUT', 'DONUT', 'DINING TABLE', 'PERSON', 'DONUT', 'PERSON', 'DONUT', 'HOT DOG', 'CUP', 'PERSON', 'PERSON', 'CUP', 'CAKE', 'PERSON', 'DINING TABLE', 'CHAIR', 'CUP', 'DINING TABLE', 'DINING TABLE', 'DINING TABLE', 'CAKE', 'DONUT', 'BOWL', 'PERSON', 'DINING TABLE', 'CAKE', 'KNIFE', 'DINING TABLE', 'DONUT', 'PERSON', 'BOWL', 'DINING TABLE', 'DINING TABLE', 'DINING TABLE', 'DINING TABLE', 'DONUT', 'CUP', 'DONUT', 'DINING TABLE', 'DONUT', 'DINING TABLE', 'DONUT', 'DINING TABLE', 'BOWL', 'DINING TABLE', 'DINING TABLE', 'DINING TABLE', 'DONUT', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'SANDWICH', 'SANDWICH', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'SPOON', 'BASEBALL BAT', 'SPOON', 'BASEBALL BAT', 'PERSON', 'PIZZA', 'PERSON', 'DONUT', 'PERSON', 'BOWL', 'PERSON', 'PERSON', 'SANDWICH', 'PERSON', 'PERSON', 'FORK', 'DONUT', 'REFRIGERATOR', 'HOT DOG', 'DINING TABLE', 'CUP', 'CUP', 'PERSON', 'PERSON', 'PERSON', 'CUP', 'CUP', 'CUP', 'PERSON', 'PERSON', 'PERSON', 'CUP', 'PERSON', 'VASE', 'DINING TABLE', 'VASE', 'BASEBALL GLOVE', 'BIRD', 'VASE', 'CAKE', 'CAKE', 'DINING TABLE', 'PERSON', 'KNIFE', 'DINING TABLE', 'CAR', 'CUP', 'PERSON', 'KNIFE', 'DINING TABLE', 'DINING TABLE', 'CAKE', 'CAKE', 'KNIFE', 'CAKE', 'CAKE', 'BANANA', 'BOWL', 'CAKE', 'FORK', 'CAKE', 'SPOON', 'PERSON', 'PERSON', 'CUP', 'PERSON', 'PERSON', 'CUP', 'DINING TABLE', 'AIRPLANE', 'BOTTLE', 'PERSON', 'PERSON', 'PERSON', 'CLOCK', 'CLOCK', 'CLOCK', 'PERSON', 'PERSON', 'PERSON', 'CLOCK', 'PERSON', 'VASE', 'PERSON', 'BROCCOLI', 'BOTTLE', 'PERSON', 'CLOCK', 'CLOCK', 'BOWL', 'PERSON', 'CLOCK', 'POTTED PLANT', 'BOWL', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'POTTED PLANT', 'PERSON', 'TIE', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'CHAIR', 'CHAIR', 'BIRD', 'SPOON', 'PERSON', 'PERSON', 'BOWL', 'FORK', 'SPORTS BALL', 'SPORTS BALL', 'FRISBEE', 'SPORTS BALL', 'PERSON', 'CAKE', 'KNIFE', 'SPOON', 'DONUT', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'BOWL', 'PERSON', 'BOWL', 'BOWL', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'BOWL', 'PERSON', 'OVEN', 'BOWL', 'OVEN', 'BOWL', 'BOWL', 'BOWL', 'PERSON', 'BOWL', 'OVEN', 'OVEN', 'BOWL', 'PERSON', 'OVEN', 'OVEN', 'OVEN', 'PERSON', 'OVEN', 'SINK', 'PERSON', 'SINK', 'PERSON', 'PERSON', 'FORK', 'BOWL', 'OVEN', 'OVEN', 'PERSON', 'PERSON', 'OVEN', 'OVEN', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'BOWL', 'BOWL', 'KNIFE', 'PERSON', 'PERSON', 'BOWL', 'BOWL', 'CHAIR', 'KNIFE', 'BOWL', 'BOWL', 'PERSON', 'BOWL', 'OVEN', 'BOWL', 'BOWL', 'BOWL', 'PERSON', 'PERSON', 'BOWL', 'BOTTLE', 'PERSON', 'BOTTLE', 'PERSON', 'PERSON', 'CELL PHONE', 'BENCH', 'PERSON', 'PERSON', 'HANDBAG', 'HANDBAG', 'HANDBAG', 'PERSON', 'PERSON', 'HOT DOG', 'PERSON', 'PERSON', 'DONUT', 'PERSON', 'PERSON', 'CHAIR', 'DONUT', 'PERSON', 'PERSON', 'TIE', 'TIE', 'FRISBEE', 'PERSON', 'CHAIR', 'PERSON', 'KNIFE', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 0, 'TV', 'PERSON', 'PERSON', 'TRUCK', 'PERSON', 'BASEBALL BAT', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'CHAIR', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'TOILET', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'DINING TABLE', 'CHAIR', 'CHAIR', 'PERSON', 'CHAIR', 'HANDBAG', 'HANDBAG', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'DONUT', 'TRAIN', 'PERSON', 'PERSON', 'HANDBAG', 'TEDDY BEAR', 'DONUT', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'HANDBAG', 'CUP', 'TEDDY BEAR', 'DINING TABLE', 'VASE', 'PERSON', 'HANDBAG', 'PERSON', 'TEDDY BEAR', 'TRAIN', 'BACKPACK', 'TEDDY BEAR', 'PERSON', 'TEDDY BEAR', 'PERSON', 'TRUCK', 'BOOK', 'BOOK', 'BOOK', 'PERSON', 'OVEN', 'OVEN', 'DONUT', 'PERSON', 'PERSON', 'DONUT', 'DONUT', 'CAKE', 'CAKE', 'OVEN', 'OVEN', 'TV', 'PERSON', 'LAPTOP', 'PERSON', 'LAPTOP', 'LAPTOP', 'OVEN', 'OVEN', 'OVEN', 'PERSON', 'PERSON', 'OVEN', 'PERSON', 'DONUT', 'PERSON', 'PERSON', 'CAKE', 'DONUT', 'DONUT', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'OVEN', 'PERSON', 'OVEN', 'REFRIGERATOR', 'TV', 'OVEN', 'PERSON', 'DONUT', 'PERSON', 'PERSON', 'PERSON', 'OVEN', 'OVEN', 'PERSON', 'PERSON', 'OVEN', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'OVEN', 'OVEN', 'OVEN', 'OVEN', 'OVEN', 'TV', 'CAKE', 'TV', 'OVEN', 'PERSON', 'OVEN', 'TV', 'TV', 'OVEN', 'TV', 'PERSON', 'OVEN', 'OVEN', 'PERSON', 'PERSON', 'REFRIGERATOR', 'BOTTLE', 'PERSON', 'BOWL', 'PERSON', 'PERSON', 'PERSON', 'DINING TABLE', 'SANDWICH', 'DINING TABLE', 'CAKE', 'CAKE', 'SANDWICH', 'DINING TABLE', 'SANDWICH', 'PERSON', 'SPOON', 'PERSON', 'PIZZA', 'KNIFE', 'PERSON', 'HANDBAG', 'HANDBAG', 'BENCH', 'FORK', 'FORK', 'FORK', 'FORK', 'CAKE', 'FORK', 'SPOON', 'FORK', 'TRUCK', 'PARKING METER', 'CAR', 'CAR', 'BUS', 'BUS', 'BUS', 'BUS', 'CAR', 'PARKING METER', 'CAR', 'CAR', 'BOTTLE', 'BOTTLE', 'CUP', 'BOWL', 'PERSON', 'PERSON', 'BOWL', 'BOWL', 'BOWL', 'PERSON', 'PERSON', 'BOWL', 'BOWL', 'BOTTLE', 'BOTTLE', 'BOTTLE', 'BOWL', 'BOWL', 'BOTTLE', 'BOWL', 'BOWL', 'BOWL', 'CUP', 'BOWL', 'PERSON', 'PERSON', 'SINK', 'TOILET', 'PERSON', 'OVEN', 'OVEN', 'OVEN', 'PERSON', 'PERSON', 'BOWL', 'PERSON', 'PERSON', 'OVEN', 'PERSON', 'OVEN', 'PERSON', 'OVEN', 'PERSON', 'PERSON', 'SPOON', 'PERSON', 'PERSON', 'PERSON', 'SPOON', 'PERSON', 'OVEN', 'SPOON', 'PERSON', 'SPOON', 'SPOON', 'BOTTLE', 'SPOON', 'BOTTLE', 'BOWL', 'BOWL', 'BOWL', 'BOWL', 'BOWL', 'PERSON', 'BOWL', 'PERSON', 'PERSON', 'BOWL', 'PERSON', 'PERSON', 'BOWL', 'BOTTLE', 'PERSON', 'CHAIR', 'REFRIGERATOR', 'PIZZA', 'HOT DOG', 'BANANA', 'BANANA', 'SANDWICH', 'HOT DOG', 'HOT DOG', 'SANDWICH', 'PERSON', 'POTTED PLANT', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'BANANA', 'HOT DOG', 'SANDWICH', 'SANDWICH', 'PERSON', 'DONUT', 'PERSON', 'PERSON', 'SANDWICH', 'HOT DOG', 'CAKE', 'DINING TABLE', 'CAKE', 'HOT DOG']
# signature2= ['PIZZA', 'PERSON', 'SINK', 'OVEN', 'TV', 'TV', 'OVEN', 'SUITCASE', 'CAKE', 'SUITCASE', 'CHAIR', 'SUITCASE', 'MOTORCYCLE', 'OVEN', 'TV', 'TV', 'PERSON', 'PERSON', 'PERSON', 'PERSON', 'PERSON']



# # Call the function with signature1 and signature2
# start_index, end_index = find_best_match(signature1, signature2)

# # Print the result
# print("Start:", start_index)
# print("End:", end_index)

