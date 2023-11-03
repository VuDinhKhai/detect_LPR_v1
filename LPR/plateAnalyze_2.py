import os
import time
import numpy as np
import cv2
import torch
from LPR.models.experimental import attempt_load
from LPR.utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_boxes,
    xyxy2xywh, strip_optimizer, set_logging)
from LPR.utils.torch_utils import select_device
from LPR.utils.plots import plot_one_box
from config import weights_detect,weights_reco,MAX_BUFFER_SIZE
import math
import queue

class Detection:
    def __init__(self):
        self.device = select_device('')
        self.half = self.device.type != 'cpu'
        self.weights_detect_path = weights_detect

        self.char_model, self.names = self.load_model(self.weights_detect_path )
        self.size=(640,640)
        
        self.iou_thres=0.1
        self.conf_thres=0.5

        self.conf_thres_reco = 0.5
        self.iou_thres_reco=0.1

        self.weights_recognition_path =weights_reco
        self.weights_recognition = attempt_load(self.weights_recognition_path, device=self.device)
        self.stride_ocr = self.weights_recognition.stride.max()
        self.imgsz_ocr = check_img_size(512, s=self.stride_ocr)
        self.names_ocr = self.weights_recognition.module.names if hasattr(self.weights_recognition, 'module') else self.weights_recognition.names

        # self.output_folder = r'E:\AIPT\detect_LPR\images'
        # if not os.path.exists(self.output_folder):
        #     os.makedirs(self.output_folder)

    def detect(self, frame):
        
        frame, lp_list = self.char_detection_yolo(frame)

        return frame, lp_list
    
    def preprocess_image(self, original_image):

        resized_img = self.ResizeImg(original_image,size=self.size)
        image = resized_img.copy()[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        image = np.ascontiguousarray(image)

        image = torch.from_numpy(image).to(self.device)
        image = image.float()
        image = image / 255.0
        if image.ndimension() == 3:
            image = image.unsqueeze(0)
        return image, resized_img
    
    def char_detection_yolo(self, image, classes=None, \
                            agnostic_nms=True, max_det=1000):
        t0 = time.time()
        lp_list = []
        try:
            lp_list = []
            colors =(255,255,0)
            img,resized_img = self.preprocess_image(image.copy())
            pred = self.char_model(img, augment=False)[0]
            
            detections = non_max_suppression(pred, conf_thres=self.conf_thres,
                                                iou_thres=self.iou_thres,
                                                classes=[4,5],
                                                agnostic=agnostic_nms,
                                                multi_label=True,
                                                labels=(),
                                                max_det=max_det)
            results=[]
            value_LP = ""
            for i, det in enumerate(detections):
                # # det[:, :4]=scale_coords(resized_img.shape,det[:, :4],image.shape).round()
                # det=det.tolist()
                # if len(det):
                #     for *xyxy, conf, cls in det:
                #         # xc,yc,w_,h_=(xyxy[0]+xyxy[2])/2,(xyxy[1]+xyxy[3])/2,(xyxy[2]-xyxy[0]),(xyxy[3]-xyxy[1])
                #         result=[self.names[int(cls)], str(conf), (xyxy[0],xyxy[1],xyxy[2],xyxy[3])]
                #         results.append(result)
                if det is not None and len(det):
                    det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], image.shape).round()
                    for *xyxy, conf, cls in reversed(det): # *xyxy : tọa độ bbox, conf : độ chính xác, cls : class mấy
                        # Add bbox to image
                        
                        if conf > 0.7:
                            # label = '%s %.2f' % (self.names_detect[int(cls)], conf)
                            x1, y1,x2,y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                            crop = image[y1:y2, x1:x2]
                            value_LP = self.detect_recognition_letter(crop)
                            lp_list.append([value_LP,(x1, y1,x2,y2)])
                            plot_one_box(xyxy, image, label=value_LP, color=colors, line_thickness=3)
            # print(results)
            print("time detect: ", time.time() - t0)
            t0 = time.time()
            return image,lp_list

        except Exception as e:
            print(f"[plateAnalyze_2][detect] {e}")
            return image , lp_list
        
    def detect_recognition_letter(self,crop_image):
        t0 = time.time()
        img = self.letterbox(crop_image, new_shape=640)[0]
        # frame_name = os.path.join(self.output_folder, f"d_{t0}.jpg")
        # cv2.imwrite(frame_name, img)
        # cv2.imshow(f"{n}",img)
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
        pred = non_max_suppression(pred, self.conf_thres_reco, self.iou_thres_reco, agnostic=False)
        license_plate = ""
        for i, det in enumerate(pred):
            # gn = torch.tensor(crop_image.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if det is not None and len(det):
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], crop_image.shape).round()
                bb_list =[]
                for *xyxy, conf, cls in reversed(det): # *xyxy : tọa độ bbox, conf : độ chính xác, cls : class mấy
                    # Add bbox to image
                    # label = '%s %.2f' % (self.names_ocr[int(cls)], conf)
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
        print("time reco: ", time.time() - t0)
        t0 = time.time()
        return license_plate
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


    def ResizeImg(self, img, size):
        h1, w1, _ = img.shape
        # print(h1, w1, _)
        h, w = size
        if w1 < h1 * (w / h):
            # print(w1/h1)
            img_rs = cv2.resize(img, (int(float(w1 / h1) * h), h))
            mask = np.zeros((h, w - (int(float(w1 / h1) * h)), 3), np.uint8)
            img = cv2.hconcat([img_rs, mask])
            trans_x = int(w / 2) - int(int(float(w1 / h1) * h) / 2)
            trans_y = 0
            trans_m = np.float32([[1, 0, trans_x], [0, 1, trans_y]])
            height, width = img.shape[:2]
            img = cv2.warpAffine(img, trans_m, (width, height))
            return img
        else:
            img_rs = cv2.resize(img, (w, int(float(h1 / w1) * w)))
            mask = np.zeros((h - int(float(h1 / w1) * w), w, 3), np.uint8)
            img = cv2.vconcat([img_rs, mask])
            trans_x = 0
            trans_y = int(h / 2) - int(int(float(h1 / w1) * w) / 2)
            trans_m = np.float32([[1, 0, trans_x], [0, 1, trans_y]])
            height, width = img.shape[:2]
            img = cv2.warpAffine(img, trans_m, (width, height))
            return img
    def load_model(self,path, train = False):
        # print(self.device)
        self.device = select_device('')
        model = attempt_load(path, device=self.device)  # load FP32 model
        names = model.module.names if hasattr(model, 'module') else model.names  # get class names
        if train:
            model.train()
        else:
            model.eval()
        return model, names
    def xyxytoxywh(self, x):
        # Convert nx4 boxes from [x1, y1, x2, y2] to [x, y, w, h] where xy1=top-left, xy2=bottom-right
        y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
        y[0] = (x[0] + x[2]) / 2  # x center
        y[1] = (x[1] + x[3]) / 2  # y center
        y[2] = x[2] - x[0]  # width
        y[3] = x[3] - x[1]  # height
        return y

class PlateAnalyze:
    def __init__(self):

        self.frame_generate_buffer = queue.Queue(maxsize=MAX_BUFFER_SIZE)
        self.conf_thres_detect = 0.1
        self.iou_thres_detect= 0.5

        self.conf_thres_reco = 0.5
        self.iou_thres_reco=0.5


        self.device = select_device('')
        self.half = self.device.type != 'cpu'
        self.weights_detect_path = weights_detect
        self.weights_recognition_path =weights_reco

        self.weights_detect = attempt_load(self.weights_detect_path, device=self.device)
        # self.weights_detect = Detection(weights_path=self.weights_detect_path,device=self.device,iou_thres=self.iou_thres_detect,conf_thres=self.conf_thres_detect)
        
        self.stride_detect = self.weights_detect.stride.max()
        self.imgsz_detect = check_img_size(512, s=self.stride_detect)
        self.names_detect = self.weights_detect.module.names if hasattr(self.weights_detect, 'module') else self.weights_detect.names
        

        self.weights_recognition = attempt_load(self.weights_recognition_path, device=self.device)
        self.stride_ocr = self.weights_recognition.stride.max()
        self.imgsz_ocr = check_img_size(512, s=self.stride_ocr)
        self.names_ocr = self.weights_recognition.module.names if hasattr(self.weights_recognition, 'module') else self.weights_recognition.names

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

    def detect_recognition_letter(self,crop_image,n):
        t0 = time.time()
        img = self.letterbox(crop_image, new_shape=512)[0]
        # cv2.imshow(f"{n}",img)
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
        pred = non_max_suppression(pred, self.conf_thres_reco, self.iou_thres_reco, agnostic=False)
        license_plate = ""
        for i, det in enumerate(pred):
            # gn = torch.tensor(crop_image.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if det is not None and len(det):
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], crop_image.shape).round()
                bb_list =[]
                for *xyxy, conf, cls in reversed(det): # *xyxy : tọa độ bbox, conf : độ chính xác, cls : class mấy
                    # Add bbox to image
                    # label = '%s %.2f' % (self.names_ocr[int(cls)], conf)
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
        print("time reco: ", time.time() - t0)
        t0 = time.time()
        return license_plate

    def detect(self,img0):
        t0 = time.time()
        lp_list = []
        try:
            img = self.letterbox(img0, new_shape=512)[0]
                # Convert
            img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
            img = np.ascontiguousarray(img)
            img = torch.from_numpy(img).to(self.device)
            img = img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            colors =(255,255,0)
            # Inference
            pred = self.weights_detect(img, augment=False)[0]
            # Apply NMS
            value_LP = ""
            pred = non_max_suppression(pred, self.conf_thres_detect ,self.iou_thres_detect, classes=[4,5], agnostic=False)
            # Process detections
            n=0
            output_dir = r"E:\AIPT\detect_LPR\crop"
            os.makedirs(output_dir, exist_ok=True)
            for i, det in enumerate(pred):
                if det is not None and len(det):
                    det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img0.shape).round()
                    for *xyxy, conf, cls in reversed(det): # *xyxy : tọa độ bbox, conf : độ chính xác, cls : class mấy
                        # Add bbox to image
                        
                        if conf > 0.7:
                            # label = '%s %.2f' % (self.names_detect[int(cls)], conf)
                            x1, y1,x2,y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                            crop = img0[y1:y2, x1:x2]
                            # cv2.imshow(f"{n + 1}"  , crop)
                            # output_filename = os.path.join(output_dir, f"crop_{n}.jpg")
                            # cv2.imwrite(output_filename, crop)
                            # n += 1
                            # resized_image = cv2.resize(crop, (460, 230), interpolation=cv2.INTER_NEAREST)
                            value_LP = self.detect_recognition_letter(crop,n+100)
                            lp_list.append(value_LP)
                            plot_one_box(xyxy, img0, label=value_LP, color=colors, line_thickness=3)
            print("time detect: ", time.time() - t0)
            t0 = time.time()
            return img0,lp_list
        except Exception as e:
            print(f"[plateAnalyze_2][detect] {e}")
            return img0 , lp_list
