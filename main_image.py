import argparse
import os
import platform
import shutil
import time
from pathlib import Path
import numpy as np
import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
from models.experimental import attempt_load
from utils.dataloaders import LoadStreams, LoadImages
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_boxes,
    xyxy2xywh, strip_optimizer, set_logging)
from utils.torch_utils import select_device
from utils.plots import plot_one_box
from utils import utils_rotate,helper
import math


def letterbox(img, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True):
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, 64), np.mod(dh, 64)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)
def linear_equation(x1, y1, x2, y2):
    b = y1 - (y2 - y1) * x1 / (x2 - x1)
    a = (y1 - b) / x1
    return a, b

def check_point_linear(x, y, x1, y1, x2, y2):
    a, b = linear_equation(x1, y1, x2, y2)
    y_pred = a*x+b
    return(math.isclose(y_pred, y, abs_tol = 3))

def detect_recognition_letter(weights_reco,img0):
    device = select_device('')
    print('device:', device)
    half = device.type != 'cpu'
    # Load model
    model_reco = attempt_load(weights_reco, device=device)
    imgsz = check_img_size(512, s=model_reco.stride.max())
    save_img = True
    if half:
        model_reco.half()
    ##dataset = LoadImages(source, img_size=imgsz)
    # Get names and colors
    names = model_reco.module.names if hasattr(model_reco, 'module') else model_reco.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]
    # Run inference
    t0 = time.time()
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    # _ = model_detect(img) #if device.type != 'cpu' else None  # run once
    _ = model_reco(img.half() if half else img) if device.type != 'cpu' else None
    # img0 = cv2.imread(r'resultLP/3.jpg')
    # vid = cv2.VideoCapture(video_path)
    img = letterbox(img0, new_shape=512)[0]
        # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    # Inference
    pred = model_reco(img, augment=False)[0]
    # Apply NMS
    pred = non_max_suppression(pred, 0.4, 0.5, agnostic=False)
    #print("pred " + str(pred))  pred [tensor([[250.17928,  95.72924, 264.18994, 105.58556,   0.41472,   0.00000]])]
    # Process detections
    license_plate = ""
    for i, det in enumerate(pred):
        gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        if det is not None and len(det):
            # print("det : " + str(det))    det : tensor([[250.17928,  95.72924, 264.18994, 105.58556,   0.41472,   0.00000]])
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img0.shape).round()
            print("det : " + str(det))
            # Write results
            n=0
            bb_list =[]
            for *xyxy, conf, cls in reversed(det): # *xyxy : tọa độ bbox, conf : độ chính xác, cls : class mấy
                # Add bbox to image
                label = '%s %.2f' % (names[int(cls)], conf)
                name_cls = '%s' % (names[int(cls)])
                # print("label: %s" % label + "\t xy: %s" % (xyxy))
                x1, y1,x2,y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                bb_list.append([x1, y1, x2, y2, float(conf),name_cls])
                # print(x1,y1,x2,y2)
                crop = img0[y1:y2, x1:x2]
                # crop_save = img0[x1-30:x2+30, y1:y2]
                # cv2.imwrite(r'E:\AIPT\yolov5\resultLP\{}.jpg'.format(str(n)), crop)
                # cv2.imshow("crop" + str(n), crop)
                # cv2.rectangle(img0, (int(xyxy[0]),int(xyxy[1])), (int(xyxy[2]),int(xyxy[3])), color = (0,0,225), thickness = 2)
                # cv2.imshow("Image with : " ,img0)
                # # cv2.imshow("img0" + str(n), img0)
                # # cv2.imwrite(r'E:\AIPT\yolov5\result\{}.jpg'.format(str(n)), crop)
                # n=n+1
                    # plot_one_box(xyxy, img0, label=label, color=colors[int(cls)], line_thickness=3)
            # cv2.putText(img0, str(fps), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
            # print("time : ", time.time()- t0)
            print("bb_list : ", bb_list)
            center_list = []
            y_mean = 0
            y_sum = 0
            LP_type = None
            for bb in bb_list:
                x_c = (bb[0]+bb[2])/2
                y_c = (bb[1]+bb[3])/2
                y_sum += y_c
                center_list.append([x_c,y_c,bb[-1]])

            # find 2 point to draw line
            l_point = center_list[0]
            r_point = center_list[0]
            for cp in center_list:
                if cp[0] < l_point[0]:
                    l_point = cp
                if cp[0] > r_point[0]:
                    r_point = cp
            for ct in center_list:
                if l_point[0] != r_point[0]:
                    if (check_point_linear(ct[0], ct[1], l_point[0], l_point[1], r_point[0], r_point[1]) == False):
                        LP_type = "2"

            y_mean = int(int(y_sum) / len(bb_list))
            # 1 line plates and 2 line plates
            line_1 = []
            line_2 = []
            license_plate = ""
            if LP_type == "2":
                print("License plate 2 ")
                for c in center_list:
                    if int(c[1]) > y_mean:
                        line_2.append(c)
                    else:
                        line_1.append(c)
                for l1 in sorted(line_1, key = lambda x: x[0]):
                    license_plate += str(l1[2])
                license_plate += "-"
                for l2 in sorted(line_2, key = lambda x: x[0]):
                    license_plate += str(l2[2])
            else:
                print("License plate 1 ")
                for l in sorted(center_list, key = lambda x: x[0]):
                    license_plate += str(l[2])
            print("Licenseplate found : " + license_plate)
    return license_plate
def detect_recognition_letter_APP(weights_reco,img0,device):
    half = device.type != 'cpu'
    model_reco = attempt_load(weights_reco, device=device)
    imgsz = check_img_size(512, s=model_reco.stride.max())
    names = model_reco.module.names if hasattr(model_reco, 'module') else model_reco.names
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    _ = model_reco(img.half() if half else img) if device.type != 'cpu' else None
    img = letterbox(img0, new_shape=512)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    # Inference
    pred = model_reco(img, augment=False)[0]
    # Apply NMS
    pred = non_max_suppression(pred, 0.4, 0.5, agnostic=False)
    license_plate = ""
    for i, det in enumerate(pred):
        gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        if det is not None and len(det):
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img0.shape).round()
            # print("det : " + str(det))
            # Write results
            bb_list =[]
            for *xyxy, conf, cls in reversed(det): # *xyxy : tọa độ bbox, conf : độ chính xác, cls : class mấy
                # Add bbox to image
                label = '%s %.2f' % (names[int(cls)], conf)
                name_cls = '%s' % (names[int(cls)])
                x1, y1,x2,y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                bb_list.append([x1, y1, x2, y2, float(conf),name_cls])
            # print("bb_list : ", bb_list)
            center_list = []
            y_mean = 0
            y_sum = 0
            LP_type = None
            for bb in bb_list:
                x_c = (bb[0]+bb[2])/2
                y_c = (bb[1]+bb[3])/2
                y_sum += y_c
                center_list.append([x_c,y_c,bb[-1]])
            # find 2 point to draw line
            l_point = center_list[0]
            r_point = center_list[0]
            for cp in center_list:
                if cp[0] < l_point[0]:
                    l_point = cp
                if cp[0] > r_point[0]:
                    r_point = cp
            for ct in center_list:
                if l_point[0] != r_point[0]:
                    if (check_point_linear(ct[0], ct[1], l_point[0], l_point[1], r_point[0], r_point[1]) == False):
                        LP_type = "2"

            y_mean = int(int(y_sum) / len(bb_list))
            # 1 line plates and 2 line plates
            line_1 = []
            line_2 = []
            license_plate = ""
            if LP_type == "2":
                # print("License plate 2 ")
                for c in center_list:
                    if int(c[1]) > y_mean:
                        line_2.append(c)
                    else:
                        line_1.append(c)
                for l1 in sorted(line_1, key = lambda x: x[0]):
                    license_plate += str(l1[2])
                license_plate += "-"
                for l2 in sorted(line_2, key = lambda x: x[0]):
                    license_plate += str(l2[2])
            else:
                # print("License plate 1 ")
                for l in sorted(center_list, key = lambda x: x[0]):
                    license_plate += str(l[2])
            # print("Licenseplate found : " + license_plate)
    return license_plate

value_LP = None

def detect_APP(weights_detect,weights_reco,img0):
    global value_LP
    device = select_device('')
    half = device.type != 'cpu'
    # Load model
    model_detect = attempt_load(weights_detect, device=device)  # load FP32 model
    imgsz = check_img_size(512, s=model_detect.stride.max())  # check img_size
    model_reco = attempt_load(weights_reco, device=device)
    if half:
        model_detect.half()
    ##dataset = LoadImages(source, img_size=imgsz)
    # Get names and colors
    names = model_detect.module.names if hasattr(model_detect, 'module') else model_detect.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    _ = model_detect(img.half() if half else img) if device.type != 'cpu' else None
    img = letterbox(img0, new_shape=512)[0]
        # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    pred = model_detect(img, augment=False)[0]

    # Apply NMS
    pred = non_max_suppression(pred, 0.4, 0.5, classes=0, agnostic=False)
    #print("pred " + str(pred))  pred [tensor([[250.17928,  95.72924, 264.18994, 105.58556,   0.41472,   0.00000]])]
    # Process detections
    for i, det in enumerate(pred):
        gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        if det is not None and len(det):
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img0.shape).round()
            for *xyxy, conf, cls in reversed(det): # *xyxy : tọa độ bbox, conf : độ chính xác, cls : class mấy
                # Add bbox to image
                if conf > 0.7:
                    label = '%s %.2f' % (names[int(cls)], conf)
                    x1, y1,x2,y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                    crop = img0[y1:y2, x1:x2]
                    value_LP = detect_recognition_letter_APP(weights_reco,crop,device)
                    plot_one_box(xyxy, img0, label=value_LP, color=colors[int(cls)], line_thickness=3)
        return img0,value_LP
def detect(weights_detect,weights_reco,video_path):
    device = select_device('')
    print('device:', device)
    half = device.type != 'cpu'
    # Load model
    model_detect = attempt_load(weights_detect, device=device)  # load FP32 model
    imgsz = check_img_size(512, s=model_detect.stride.max())  # check img_size
    model_reco = attempt_load(weights_reco, device=device)
    imgsz1 = check_img_size(512, s=model_reco.stride.max())
    save_img = True
    if half:
        model_detect.half()
        model_reco.half()
    ##dataset = LoadImages(source, img_size=imgsz)
    # Get names and colors
    names = model_detect.module.names if hasattr(model_detect, 'module') else model_detect.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]
    # Run inference
    t0 = time.time()
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    # _ = model_detect(img) #if device.type != 'cpu' else None  # run once
    _ = model_detect(img.half() if half else img) if device.type != 'cpu' else None
    _ = model_reco(img.half() if half else img) if device.type != 'cpu' else None
    img0 = cv2.imread(r'E:\AIPT\APP_QT\detect_LPR\test_image\5.jpg')
    # vid = cv2.VideoCapture(video_path)
    img = letterbox(img0, new_shape=512)[0]
        # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    pred = model_detect(img, augment=False)[0]

    # Apply NMS
    pred = non_max_suppression(pred, 0.4, 0.5, classes=0, agnostic=False)
    #print("pred " + str(pred))  pred [tensor([[250.17928,  95.72924, 264.18994, 105.58556,   0.41472,   0.00000]])]
    # Process detections
    for i, det in enumerate(pred):
        gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        if det is not None and len(det):
            # print("det : " + str(det))    det : tensor([[250.17928,  95.72924, 264.18994, 105.58556,   0.41472,   0.00000]])
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img0.shape).round()
            # Write results
            n=1
            list_read_plates = set()
            for *xyxy, conf, cls in reversed(det): # *xyxy : tọa độ bbox, conf : độ chính xác, cls : class mấy
                # Add bbox to image
                if conf > 0.7:
                    label = '%s %.2f' % (names[int(cls)], conf)
                    x1, y1,x2,y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                    # print(x1,y1,x2,y2)
                    crop = img0[y1:y2, x1:x2]
                    # crop_save = img0[x1-30:x2+30, y1:y2]
                    cv2.imwrite(r'E:\AIPT\yolov5\resultLP\{}.jpg'.format(str(n)), crop)
                    cv2.imshow("crop" + str(n), crop)
                    detect_recognition_letter(weights_reco,crop)
                    cv2.rectangle(img0, (int(xyxy[0]),int(xyxy[1])), (int(xyxy[2]),int(xyxy[3])), color = (0,0,225), thickness = 2)
                    # cv2.imshow("img0" + str(n), img0)
                    # cv2.imwrite(r'E:\AIPT\yolov5\result\{}.jpg'.format(str(n)), crop)
                    n=n+1
                        # plot_one_box(xyxy, img0, label=label, color=colors[int(cls)], line_thickness=3)
        # new_frame_time = time.time()
        # fps = 1/(new_frame_time-prev_frame_time)
        # prev_frame_time = new_frame_time
        # fps = int(fps)
        # cv2.putText(img0, str(fps), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
        # print("time : ", time.time()- t0)
        # t0 = time.time()
        cv2.imshow('frame', img0)
        return img0

if __name__ == '__main__':
    weights_detect=r'E:\AIPT\APP_QT\detect_LPR\model\LP_detector_nano_61.pt'
    weights_reco = r'E:\AIPT\APP_QT\detect_LPR\model\best_188.pt'
    video_path = r'E:\AIPT\yolov5\test_image\4.mp4'
    with torch.no_grad():
        detect(weights_detect,weights_reco,video_path=video_path)
        cv2.waitKey(0)
