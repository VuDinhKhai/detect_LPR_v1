import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import numpy as np
import cv2
import torch
from LPR.models.experimental import attempt_load
from LPR.utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_boxes,
    xyxy2xywh, strip_optimizer, set_logging)
from LPR.utils.torch_utils import select_device
from LPR.utils.plots import plot_one_box
from config import weights_detect,weights_reco
import math
# from sort import *
from LPR.sort import Sort  # Import Sort class

tracker = None
class PlateAnalyze:
    def __init__(self):
        self.device = select_device('')
        self.half = self.device.type != 'cpu'
        self.weights_detect_path = weights_detect
        self.weights_recognition_path =weights_reco

        self.weights_detect = attempt_load(self.weights_detect_path, device=self.device)
        self.stride_detect = self.weights_detect.stride.max()
        self.names_detect = self.weights_detect.module.names if hasattr(self.weights_detect, 'module') else self.weights_detect.names
        self.imgsz_detect = check_img_size(512, s=self.stride_detect)

        self.weights_recognition = attempt_load(self.weights_recognition_path, device=self.device)
        self.stride_ocr = self.weights_recognition.stride.max()
        self.imgsz_ocr = check_img_size(512, s=self.stride_ocr)
        self.names_ocr = self.weights_recognition.module.names if hasattr(self.weights_recognition, 'module') else self.weights_recognition.names
    def init_tracker():
        global tracker
        
        sort_max_age = 10
        sort_min_hits = 2
        sort_iou_thresh = 0.5
        tracker =Sort(max_age=sort_max_age,min_hits=sort_min_hits,iou_threshold=sort_iou_thresh)

    def letterbox(self,img, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True):
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
    def linear_equation(self,x1, y1, x2, y2):
        b = y1 - (y2 - y1) * x1 / (x2 - x1)
        a = (y1 - b) / x1
        return a, b

    def check_point_linear(self,x, y, x1, y1, x2, y2):
        a, b = self.linear_equation(x1, y1, x2, y2)
        y_pred = a*x+b
        return(math.isclose(y_pred, y, abs_tol = 3))

    def detect_recognition_letter(self,crop_image):
        img = self.letterbox(crop_image, new_shape=512)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        # Inference
        pred = self.weights_recognition(img, augment=False)[0]
        # Apply NMS
        pred = non_max_suppression(pred, 0.4, 0.5, agnostic=False)
        license_plate = ""
        for i, det in enumerate(pred):
            gn = torch.tensor(crop_image.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if det is not None and len(det):
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], crop_image.shape).round()
                bb_list =[]
                for *xyxy, conf, cls in reversed(det): # *xyxy : tọa độ bbox, conf : độ chính xác, cls : class mấy
                    # Add bbox to image
                    label = '%s %.2f' % (self.names_ocr[int(cls)], conf)
                    name_cls = '%s' % (self.names_ocr[int(cls)])
                    x1, y1,x2,y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                    bb_list.append([x1, y1, x2, y2, float(conf),name_cls])
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
                        if (self.check_point_linear(ct[0], ct[1], l_point[0], l_point[1], r_point[0], r_point[1]) == False):
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
                    for l in sorted(center_list, key = lambda x: x[0]):
                        license_plate += str(l[2])
        return license_plate

    def detect(self, img0):
        LP_list = []
        try:
            img = self.letterbox(img0, new_shape=512)[0]
            img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
            img = np.ascontiguousarray(img)
            img = torch.from_numpy(img).to(self.device)
            img = img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)
            colors = (255, 255, 0)
            # Inference
            pred = self.weights_detect(img, augment=False)[0]
            value_LP = ""
            if pred is not None and len(pred):
                pred = non_max_suppression(pred, 0.4, 0.5, classes=None, agnostic=False)
                # Process detections and track objects
                dets = []  # List to store bounding boxes for tracking
                for i, det in enumerate(pred):
                    if det is not None and len(det):
                        det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img0.shape).round()
                        for x1, y1, x2, y2, conf, cls in det:
                            if conf > 0.7:
                                dets.append([x1, y1, x2, y2, conf])
                                # You can add your recognition code here
                                # value_LP = self.detect_recognition_letter(crop)
                                # LP_list.append(value_LP)

                dets = np.array(dets)
                if tracker is not None:
                    trackers = tracker.update(dets)
                    # Draw tracking results on the image
                    for j, (x1, y1, x2, y2, track_id, *other_values) in enumerate(trackers):
                        x1, y1, x2, y2, track_id = int(x1), int(y1), int(x2), int(y2), int(track_id)
                        # Add bbox to image
                        label = f'{value_LP} - Track {track_id}'
                        plot_one_box([x1, y1, x2, y2], img0, label=label, color=colors, line_thickness=3)
            return img0
        except Exception as e:
            print(f"[plateAnalyze_2][detect] {e}")
            return img0

