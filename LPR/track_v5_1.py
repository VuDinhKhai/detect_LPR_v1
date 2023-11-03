
import argparse

import os
# limit the number of cpus used by high performance libraries
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import sys
import numpy as np
from pathlib import Path

import pandas as pd
from collections import Counter
from collections import deque

import warnings
warnings.filterwarnings('ignore')

import torch
import torch.backends.cudnn as cudnn

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # yolov5 strongsort root directory
WEIGHTS = ROOT / 'weights'

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if str(ROOT / 'yolov5') not in sys.path:
    sys.path.append(str(ROOT / 'yolov5'))  # add yolov5 ROOT to PATH
if str(ROOT / 'strong_sort') not in sys.path:
    sys.path.append(str(ROOT / 'strong_sort'))  # add strong_sort ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

import logging
from LPR.models.common import DetectMultiBackend
try:
    from LPR.utils.dataloaders import VID_FORMATS, LoadImages, LoadStreams
except:
    import sys
    sys.path.append('yolov5/utils')
    from LPR.utils.dataloaders import VID_FORMATS, LoadImages, LoadStreams
from LPR.utils.general import (LOGGER, check_img_size, non_max_suppression, scale_boxes, check_requirements, cv2,
                                  check_imshow, xyxy2xywh, increment_path, strip_optimizer, colorstr, print_args, check_file)
from LPR.utils.torch_utils import select_device, time_sync
from LPR.utils.plots import Annotator, colors, save_one_box
from strong_sort.utils.parser import get_config
from strong_sort.strong_sort import StrongSORT
from LPR.utils.plots import plot_one_box
class PlateAnalyze():
     def __init__(self):
          super().__init__()

          # self.rtsp = camera.rtsp
          # self.camera_id = camera.id
          # self.start_record = None
          # self.record_status = False
          # self.status = True 
          # self.frame_generate_buffer = queue.Queue(maxsize=MAX_BUFFER_SIZE)
          self.hide_class = False
          self.hide_conf  = False
          self.hide_labels = False
          self.draw = True
          self.show_video = True
          

          self.device = select_device('')
          self.half = self.device.type != 'cpu'

          self.list_vehicles_db = []

          self.conf_thres = 0.5
          self.iou_thres=0.1

          self.max_det = 1000

          self.list_id_lp_record = []
          self.output_video_lp = {}

          self.weights_detect_path = r"E:\code\StrongSORT-YOLO\weights\yolov5n.pt"
          # self.weights_recognition_path = weights_reco
          self.weights_detection = DetectMultiBackend(self.weights_detect_path, device=self.device, dnn=False, data=None, fp16=self.half)
          self.stride_detection, self.names_detection, self.pt_detection = self.weights_detection.stride, self.weights_detection.names, self.weights_detection.pt
          self.imgsz = (640, 640)
          self.imgsz = check_img_size(self.imgsz, s=self.stride_detection)

          # OCR
          # self.weights_recognition = attempt_load(self.weights_recognition_path, device=self.device)
          # self.stride_ocr = self.weights_recognition.stride.max()
          # self.imgsz_ocr = check_img_size(512, s=self.stride_ocr)
          # self.names_ocr = self.weights_recognition.module.names if hasattr(self.weights_recognition, 'module') else self.weights_recognition.names

          # StrongSort
          self.strong_sort_weights = r"E:\AIPT\detect_LPR\LPR\model\osnet_x0_25_msmt17.pt"
          self.config_strongsort = r'E:\AIPT\detect_LPR\LPR\strong_sort\configs\strong_sort.yaml'

          self.dataset = self.init_dataset()
          self.nr_sources = len(self.dataset)
          self.strongsort_list = self.init_strongsort()

     def init_dataset(self):
          source = str(r"E:\AIPT\detect_LPR\1.mp4")
          is_file = Path(source).suffix[1:] in (VID_FORMATS)
          is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
          self.webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)
          if is_url and is_file:
               source = check_file(source)  # download
          # Dataloader
          if self.webcam:
               cudnn.benchmark = True  # set True to speed up constant image size inference
               dataset = LoadStreams(source, img_size=self.imgsz, stride=self.stride_detection, auto=self.pt_detection)
          else:
               dataset = LoadImages(source, img_size=self.imgsz, stride=self.stride_detection, auto=self.pt_detection)
          return dataset
     def init_strongsort(self):
          strongsort_list = []
          self.cfg = get_config()
          self.cfg.merge_from_file(self.config_strongsort)

          for i in range(self.nr_sources):
               strongsort_list.append(
                    StrongSORT(
                         self.strong_sort_weights,
                         self.device,
                         self.half,
                         max_iou_distance=self.cfg.STRONGSORT.MAX_IOU_DISTANCE,
                         max_age=self.cfg.STRONGSORT.MAX_AGE,
                         n_init=self.cfg.STRONGSORT.N_INIT,
                         nn_budget=self.cfg.STRONGSORT.NN_BUDGET,
                         mc_lambda=self.cfg.STRONGSORT.MC_LAMBDA,
                         ema_alpha=self.cfg.STRONGSORT.EMA_ALPHA,
                    )
               )
          return strongsort_list
     def run(self):
          trajectory = {}
          outputs = [None] * self.nr_sources
          # Khi warmup được gọi với kích thước ảnh như trên, mô hình sẽ được khởi động trước với kích thước ảnh này để chuẩn bị cho quá trình detection. Điều này có thể cải thiện hiệu suất của mô hình khi thực hiện các thao tác detection sau này.
          self.weights_detection.warmup(imgsz=(1 if self.pt_detection else self.nr_sources, 3, *self.imgsz))  # Warmup the model
          dt, seen = [0.0, 0.0, 0.0, 0.0], 0
          curr_frames, prev_frames = [None] * self.nr_sources, [None] * self.nr_sources #các khung hình hiện tại sẽ được lưu vào curr_frames, và các khung hình trước đó sẽ được lưu vào prev_frames. Điều này có thể sử dụng để thực hiện các tác vụ như theo dõi sự thay đổi giữa các khung hình liên tiếp
          for frame_idx, (path, im, im0s, vid_cap, s) in enumerate(self.dataset):
               t1 = time_sync()
               im = torch.from_numpy(im).to(self.device)
               im = im.half() if self.half else im.float()  # uint8 to fp16/32
               im /= 255.0  # 0 - 255 to 0.0 - 1.0

               if len(im.shape) == 3:
                    im = im[None]  # expand for batch dim
               t2 = time_sync()
               dt[0] += t2 - t1

               # Inference
               # visualize = increment_path(save_dir / Path(path[0]).stem, mkdir=True) if visualize else False
               pred = self.weights_detection(im,augment=False, visualize=False)
               t3 = time_sync()
               dt[1] += t3 - t2

               # Apply NMS
               pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, classes = None, max_det=self.max_det)
               dt[2] += time_sync() - t3
               # Process detections
               for i, det in enumerate(pred):  # detections per image
                    seen += 1
                    if self.webcam:  # nr_sources >= 1
                         p, im0, _ = path[i], im0s[i].copy(), self.dataset.count
                         p = Path(p)  # to Path
                         s += f'{i}: '
                    else:
                         p, im0, _ = path, im0s.copy(), getattr(self.dataset, 'frame', 0)
                         p = Path(p)  # to Path

                    curr_frames[i] = im0
                    s += '%gx%g ' % im.shape[2:]  # print string

                    annotator = Annotator(im0, line_width=2, pil=not ascii)

                    if self.cfg.STRONGSORT.ECC:  # camera motion compensation
                         self.strongsort_list[i].tracker.camera_update(prev_frames[i], curr_frames[i])

                    if det is not None and len(det):
                         # Rescale boxes from img_size to im0 size
                         det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                         # Print results
                         for c in det[:, -1].unique():
                              n = (det[:, -1] == c).sum()  # detections per class
                              s += f"{n} {self.names_detection[int(c)]}{'s' * (n > 1)}, "  # add to string

                         xywhs = xyxy2xywh(det[:, 0:4])
                         confs = det[:, 4]
                         clss = det[:, 5]
                         
                         # pass detections to strongsort
                         t4 = time_sync()
                         outputs[i] = self.strongsort_list[i].update(xywhs.cpu(), confs.cpu(), clss.cpu(), im0)
                         t5 = time_sync()
                         dt[3] += t5 - t4

                         # draw boxes for visualization
                         if len(outputs[i]) > 0:
                              for j, (output, conf) in enumerate(zip(outputs[i], confs)):
          #
                                   bboxes = output[0:4]
                                   id = output[4]
                                   cls = output[5]
                                   bbox_left, bbox_top, bbox_right, bbox_bottom = bboxes
                                   c = int(cls)  # integer class
                                   id = int(id)  # integer id
                                   label = None if self.hide_labels else (f'{id} {self.names_detection[c]}' if self.hide_conf else \
                                        (f'{id} {conf:.2f}' if self.hide_class else f'{id} {self.names_detection[c]} {conf:.2f}'))
                                   annotator.box_label(bboxes, label, color=colors(c, True))
                                   if self.draw:
                                        # object trajectory
                                        center = ((int(bboxes[0]) + int(bboxes[2])) // 2,(int(bboxes[1]) + int(bboxes[3])) // 2)
                                        if id not in trajectory:
                                             trajectory[id] = []
                                        trajectory[id].append(center)
                                        for i1 in range(1,len(trajectory[id])):
                                             if trajectory[id][i1-1] is None or trajectory[id][i1] is None:
                                                  continue
                                             # thickness = int(np.sqrt(1000/float(i1+10))*0.3)
                                             thickness = 2
                                             try:
                                                  cv2.line(im0, trajectory[id][i1 - 1], trajectory[id][i1], (0, 0, 255), thickness)
                                             except:
                                                  pass
                         LOGGER.info(f'{s}Done. YOLO:({t3 - t2:.3f}s), StrongSORT:({t5 - t4:.3f}s)')
                    else:
                         self.strongsort_list[i].increment_ages()
                         LOGGER.info('No detections')


               if self.show_video:
                    cv2.imshow(str(p), im0)
                    if cv2.waitKey(1) == ord('q'):  # q to quit
                         break
                    prev_frames[i] = curr_frames[i]

          # Print results
          t = tuple(x / seen * 1E3 for x in dt)  # speeds per image
          LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS, %.1fms strong sort update per image at shape {(1, 3, *self.imgsz)}' % t)
# if __name__ == '__main__':
#      # Example usage:
#      detectobj = PlateAnalyze()
#      detectobj.run()

