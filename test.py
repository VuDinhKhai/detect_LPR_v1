import os
import cv2
import LPR.plateAnalyze_2 as plateAnalyze_2
import time
plateAnalyze = plateAnalyze_2.Detection()
path = r"E:\AIPT\detect_LPR\vehicles.MOV"
rtsp = "rtsp://admin:HFCMJC@192.168.1.3:554/1"
cap = cv2.VideoCapture(path)
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
# output_folder = r'E:\AIPT\detect_LPR\images'
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)
# frames_per_second = 0.3
# frame_skip = int(cap.get(cv2.CAP_PROP_FPS) / frames_per_second)
frame_count = 0
delay_frames = 6
while True:
    # for _ in range(frame_skip - 1):
    #     ret, _ = cap.read()
    #     if not ret:
            # break
    t0 = time.time()
    ret,frame = cap.read()
    # if frame_count % delay_frames == 0:
    if not ret:
        break
    # frame = cv2.resize(frame,(1280,720))
    frame,lp = plateAnalyze.detect(frame)
    # out.write(frame)
    cv2.imshow("Capture", frame)
    print("time:" + str(time.time() - t0))
    t0 = time.time()
    if cv2.waitKey(1) == 27:  # Press Esc to exit
        break
cap.release()
# out.release()
cv2.destroyAllWindows()