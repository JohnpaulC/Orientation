import time
import numpy as np
import cv2
import torch

from utils.datasets import letterbox
from utils.models import *
from Utils_orientation import *

# Image path
base_file = 'Video/' + str(71) + '.jpg'
rotate_file = 'Video/' + str(99) + '.jpg'

# Configuration file path
cfg = 'cfg/yolov3.cfg'
data_cfg = 'cfg/coco.data'
weights = 'cfg/yolov3.pt'

# Model parameter
img_size=640
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# Initialize model and load weights
model = Darknet(cfg, img_size)
model.load_state_dict(torch.load(weights, map_location=device)['model'])
model.to(device).eval()

# Detection Process Transform tensor into numpy array
if device == torch.device("cpu"):
    detection_base = object_detection(model, base_file).numpy()
    detection_rotate = object_detection(model, rotate_file).numpy()
else:
    detection_base = object_detection(model, base_file).cpu().numpy()
    detection_rotate = object_detection(model, rotate_file).cpu().numpy()
    
# Image Orientation Calculation
show_results = True
show_images = True
mode = "SIFT"
# The index of object using to calculation the capture image
detection_index = 2

print(detection_base)
print(detection_base.shape)
print(detection_rotate)
print(detection_rotate.shape)

object_num = min(detection_base.shape[0], detection_rotate.shape[0])


img_base, img_rotate = object_capture(base_file, rotate_file)
histogram_gradient(img_base, img_rotate, mag_thres= 80, bin_num= 360)
median, mean, time = angle_cal(img_base, img_rotate, mode, show_results= show_results, show_images= show_images)
print(mode + "real Result: median({0:6.3f}), mean({1:6.3f}) in {2:.3f}".format(median, mean, time))


for detection_index in range(object_num):
    img_base, img_rotate = object_capture(base_file, rotate_file,
                       bool_cap = True, detection_index = detection_index,
                       detection_base = detection_base, detection_rotate = detection_rotate)
    histogram_gradient(img_base, img_rotate, mag_thres= 50, bin_num= 360)
    median, mean, time = angle_cal(img_base, img_rotate, mode, show_results= show_results, show_images= show_images)
    print(mode + "real Result: median({0:6.3f}), mean({1:6.3f}) in {2:.3f}".format(median, mean, time))