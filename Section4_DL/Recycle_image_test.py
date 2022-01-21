import numpy as np
import cv2
import time
import os
import glob
# import pycuda.autoinit


min_confidence = 0.5

width = 1080 # 1920*1080
#width = 800 # 1280*720

height = 0
show_ratio = 0.3
title_name = 'Custom Yolo'
# Load Yolo
# v4
net = cv2.dnn.readNet("./model/yolov4-custom-recycle_best.weights", "./model/yolov4-custom-recycle.cfg")


# Activate CUDA

# os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
# os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
# print(cv2.cuda_DeviceInfo)


classes = []
with open("./model/classes.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
color_lists = np.array([[127.0,170.0,255.0], [255.0,255.0,255.0], [0,255.0,0], [0,85.0,170.0], [0,255.0,255.0], [170.0,255.0,255.0], [0,0,255.0], [0,85.0,0], [0,0,85.0], [255.0,0,0], [255.0,0,255.0], [255.0,170.0,170.0]])



layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


detected_obj = 0
detected_PET_colorless = 0
detected_PET_white = 0
detected_PET_green = 0
detected_PET_brown = 0
detected_PET_mixed = 0
detected_Glass_colorless = 0
detected_Glass_mixed = 0
detected_Glass_green = 0
detected_Glass_brown = 0
detected_Glass_blue = 0
detected_Can = 0
detected_PET_thin = 0



def detectAndDisplay(image):
    global detected_obj
    global detected_PET_colorless
    global detected_PET_white
    global detected_PET_green
    global detected_PET_brown
    global detected_PET_mixed
    global detected_Glass_colorless
    global detected_Glass_mixed
    global detected_Glass_green
    global detected_Glass_brown
    global detected_Glass_blue
    global detected_Can
    global detected_PET_thin

    
    
    h, w = image.shape[:2]
    height = int(h * width / w)
    img = cv2.resize(image, (width, height))

    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), swapRB=True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)
    
    confidences = []
    names = []
    boxes = []
    colors = []
    label_num = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > min_confidence:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                names.append(classes[class_id])
                colors.append(color_lists[class_id])
                label_num.append(str(class_id))
                

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            #label = '{} {:,.2%}'.format(names[i], confidences[i])
            label = '{}'.format(names[i])
            confidence = 'c:{:,.2%}'.format(confidences[i])
            color = colors[i]
            
            
            
            #print(i, label, confidence, x, y, w, h)

            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.circle(img, (round(x+w/2) , round(y+h/2)), 4, color, -1)
            cv2.putText(img, label, (x, y + 15), font, 1, (255,255,255), 1)
            cv2.putText(img, confidence, (x, y + 30), font, 1, (255,255,255), 1)
            
            if label_num[i] == '0' :
                detected_PET_colorless = detected_PET_colorless + 1
            
            if label_num[i] == '1':
                detected_PET_white = detected_PET_white + 1
            
            if label_num[i] == '2':
                detected_PET_green = detected_PET_green + 1

            if label_num[i] == '3':
                detected_PET_brown = detected_PET_brown + 1

            if label_num[i] == '4':
                detected_PET_mixed = detected_PET_mixed + 1

            if label_num[i] == '5':
                detected_Glass_colorless = detected_Glass_colorless + 1

            if label_num[i] == '6':
                detected_Glass_mixed = detected_Glass_mixed + 1

            if label_num[i] == '7':
                detected_Glass_green = detected_Glass_green + 1

            if label_num[i] == '8':
                detected_Glass_brown = detected_Glass_brown + 1

            if label_num[i] == '9':
                detected_Glass_blue = detected_Glass_blue + 1

            if label_num[i] == '10':
                detected_Can = detected_Can + 1

            if label_num[i] == '11':
                detected_PET_thin = detected_PET_thin + 1


    cv2.imshow(title_name, img)
    cv2.moveWindow(title_name, 830,0)
    

    detected_obj = detected_obj + len(indexes)



#----------------------------------------

# load images
img_files = glob.glob('./test_image/*.jpg')
txt_files = glob.glob('./test_image/*.txt')

TEST_PATH = glob.glob('./test_image/')

label_data = []


cnt = len(img_files)
idx = 0
total_time = 0
gt_obj = 0
gt_PET_colorless = 0
gt_PET_white = 0
gt_PET_green = 0
gt_PET_brown = 0
gt_PET_mixed = 0
gt_Glass_colorless = 0
gt_Glass_mixed = 0
gt_Glass_green = 0
gt_Glass_brown = 0
gt_Glass_blue = 0
gt_Can = 0
gt_PET_thin = 0


def import_label(text,image):
    h, w = image.shape[:2]
    height = int(h * width / w)
    img = cv2.resize(image, (width, height))
    global total_obj
    global gt_obj
    global gt_PET_colorless
    global gt_PET_white
    global gt_PET_green
    global gt_PET_brown
    global gt_PET_mixed
    global gt_Glass_colorless
    global gt_Glass_mixed
    global gt_Glass_green
    global gt_Glass_brown
    global gt_Glass_blue
    global gt_Can
    global gt_PET_thin 
    
    if os.path.exists(text):
            with open(text, 'rb') as f:
                lines = f.readlines()
            for line in lines:
                line = line.decode().replace('\n', '').replace('\r', '')
                splits = line.split(' ')
                label_num_gt = splits[0]
                #
                x_cen, y_cen, w, h = splits[1:]
                x_cen = int(float(x_cen) * width)
                y_cen = int(float(y_cen) * height)
                w = int(float(w) * width)
                h = int(float(h) * height)
                x1 = int(x_cen - w / 2)
                y1 = int(y_cen - h / 2)
                x2 = int(x_cen + w / 2)
                y2 = int(y_cen + h / 2)
                label_data.append([ x1, y1, x2, y2, label_num_gt])
                img_arr = cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
                if label_num_gt =='0':
                    gt_PET_colorless = gt_PET_colorless + 1
            
                if label_num_gt == '1':
                    gt_PET_white = gt_PET_white + 1
                
                if label_num_gt == '2':
                    gt_PET_green = gt_PET_green + 1

                if label_num_gt == '3':
                    gt_PET_brown = gt_PET_brown + 1

                if label_num_gt == '4':
                    gt_PET_mixed = gt_PET_mixed + 1

                if label_num_gt == '5':
                    gt_Glass_colorless = gt_Glass_colorless + 1

                if label_num_gt == '6':
                    gt_Glass_mixed = gt_Glass_mixed + 1

                if label_num_gt == '7':
                    gt_Glass_green = gt_Glass_green + 1

                if label_num_gt == '8':
                    gt_Glass_brown = gt_Glass_brown + 1

                if label_num_gt == '9':
                    gt_Glass_blue = gt_Glass_blue + 1

                if label_num_gt == '10':
                    gt_Can = gt_Can + 1

                if label_num_gt == '11':
                    gt_PET_thin = gt_PET_thin + 1

                

            
            gt_obj = gt_obj + len(lines)
            return img_arr

                


while True:
    img = cv2.imread(img_files[idx])
    text = txt_files[idx]

    if img is None: # 이미지가 없는 경우
        print('Image load failed!')
        break

    start = time.time()

    img_arr = import_label(text,img)

    detectAndDisplay(img_arr)
    # writeFrame(img)


    #print(label_data)
    d_time = time.time() - start
    total_time = total_time + d_time
    
    print('\t>>> detection time: {}'.format(d_time))
    
    print('\t------------------------------')

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    


    idx += 1
    # 종료
    if idx == cnt:
        print('\t>>> gt PET_colorless: {}'.format(gt_PET_colorless))
        print('\t>>> detected PET_colorless: {}'.format(detected_PET_colorless))

        print('\t>>> gt PET_white: {}'.format(gt_PET_white))
        print('\t>>> detected PET_white: {}'.format(detected_PET_white))

        print('\t>>> gt PET_green: {}'.format(gt_PET_green))
        print('\t>>> detected PET_green: {}'.format(detected_PET_green))

        print('\t>>> gt PET_brown: {}'.format(gt_PET_brown))
        print('\t>>> detected PET_brown: {}'.format(detected_PET_brown))

        print('\t>>> gt PET_mixed: {}'.format(gt_PET_mixed))
        print('\t>>> detected PET_mixed: {}'.format(detected_PET_mixed))

        print('\t>>> gt Glass_colorless: {}'.format(gt_Glass_colorless))
        print('\t>>> detected Glass_colorless: {}'.format(detected_Glass_colorless))

        print('\t>>> gt Glass_mixed: {}'.format(gt_Glass_mixed))
        print('\t>>> detected Glass_mixed: {}'.format(detected_Glass_mixed))

        print('\t>>> gt Glass_green: {}'.format(gt_Glass_green))
        print('\t>>> detected Glass_green: {}'.format(detected_Glass_green))

        print('\t>>> gt Glass_brown: {}'.format(gt_Glass_brown))
        print('\t>>> detected Glass_brown: {}'.format(detected_Glass_brown))

        print('\t>>> gt Glass_blue: {}'.format(gt_Glass_blue))
        print('\t>>> detected Glass_blue: {}'.format(detected_Glass_blue))

        print('\t>>> gt Can: {}'.format(gt_Can))
        print('\t>>> detected Can: {}'.format(detected_Can))

        print('\t>>> gt PET_thin: {}'.format(gt_PET_thin))
        print('\t>>> detected PET_thin: {}'.format(detected_PET_thin))

        print('\t>>> number of object: {}'.format(gt_obj))
        print('\t>>> detected object: {}'.format(detected_obj))
        print('\t>>> total time: {}'.format(total_time))
        print('\t>>> average time: {}'.format(total_time/(idx+1)))

        print('End of Test!')
        break

    if cv2.waitKey(1000000) & 0xFF == ord('a'):
        continue

cv2.destroyAllWindows()

