import cv2
import LPR.plateAnalyze_2 as plateAnalyze_2
import LPR.plateAnalyze_tracking_strongSORT as plateAnalyze_tracking
import LPR.track_v5_1 as track_v5
import time
plateAnalyze = plateAnalyze_tracking.Detection()

# path = r"E:\AIPT\detect_LPR\1.mp4"
plateAnalyze.detection()
# path = r"E:\AIPT\detect_LPR\1.mp4"
# img0 = cv2.imread(path)

# detectobj = track_v5.PlateAnalyze()
# detectobj.run()
# results,lp=plateAnalyze.detect(img0)
# print("Results: ", lp)
# cv2.imshow("PlateAnalyze" , results)
# cv2.imshow("PlateAnalyze" , resized_img)
# for name,conf,box in results:
#      resized_img=cv2.putText(resized_img, "{}".format(name), (int(box[0]), int(box[1])-3),
#                               cv2.FONT_HERSHEY_SIMPLEX, 0.5,
#                               (255, 0, 255), 2)
#      resized_img = cv2.rectangle(resized_img, (int(box[0]),int(box[1])), (int(box[2]),int(box[3])), (0,0,255), 1)
# cv2.imshow("PlateAnalyze1" , resized_img)
# for i in lp:
#      print(i)
# cv2.waitKey(0)
