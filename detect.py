import cv2
import json
import numpy as np
from pyzbar.pyzbar import decode
import time 
import datetime
import argparse


def real_time_detect(idx) : 
    i = 0
    cap = cv2.VideoCapture(2)
    while True : 
        with open(f"ckpt_{idx}.json") as f:
            data = json.load(f)
            ok, img = cap.read()
            if not ok :
                break
            for code in decode(img) :
                qr_data = code.data.decode()
                detected_timestamp = datetime.datetime.now().isoformat()
                if qr_data in data['ids'] :
                    continue
                print(f'QR code Detected with data : {qr_data} at time : {detected_timestamp}')
                data['ids'][qr_data] = detected_timestamp
                print(data)
    
                rect = code.rect
                pts = np.array([code.polygon],np.int32)
                cv2.polylines(img,[pts],isClosed = True,color = (0,0,255),thickness = 4)# BGR
                cv2.putText(img,qr_data,(rect[0],rect[1]),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0))
            i+=1;
            print(i)
            if i%20==0:
                cv2.imwrite(f"backup/image_{i}.jpg", img)
    
        with open(f"ckpt_{idx}.json", "w") as f:
            json.dump(data, f)
        cv2.imshow('preview',img)
        cv2.waitKey(1)

    cap.release()


if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument('--race_id', type=str, default=0)
    parser.add_argument('--ckpt_id', type=str, default=1)
    args = parser.parse_args()
    data = {'race_id' : args.race_id , 'ckpt_id' : args.ckpt_id,'ids' : {}}
    with open(f"ckpt_{args.ckpt_id}.json", "w") as f:
        json.dump(data, f)
    real_time_detect(args.ckpt_id)
    print(data)
