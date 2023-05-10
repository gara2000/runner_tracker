from qreader import QReader
import json
import cv2
import time
import argparse


WIDTH = 500
HEIGHT = 500 

def real_time_detect(path, race_id, ckpt_id) : 
#    path1 = 0
    path1 = "firas.MOV"
    i=0
#    path1 = "iheb.MOV"
    cap = cv2.VideoCapture(path1)
    qreader = QReader()
    while True : 
        with open(path) as f:
            data = json.load(f)
            ok, img = cap.read()
            if not ok :
                break
            i+=1
            if i%1==0:
                print(i)
                decoded_text = qreader.detect_and_decode(image=img,return_bboxes=True)
                for ( (x1,y1,x2,y2),qr_data ) in  decoded_text :
                    detected_timestamp = time.time()
                    if qr_data == None :
                        continue
    #                if (qr_data in data['detected_ids']) :
    #                    continue
                    print(f'QR code Detected with data : {qr_data} at time : {detected_timestamp}')
                    data['ids'][qr_data] = detected_timestamp
                    print(data)
                    cv2.rectangle(img,(x1,y1),(x1+(x2-x1),y1+(y2-y1)),color = (0,0,255),thickness = 4)
                    
                    cv2.putText(img,qr_data,(x1,y1),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0))

        with open(path, "w") as f:
            json.dump(data, f)

        img=cv2.resize(img, (WIDTH, HEIGHT))
        cv2.imshow('preview',img)
        cv2.waitKey(1)

    cap.release()


def init_ckpt_data(race_id, ckpt_id):
    data = {'race_id' : race_id , 'ckpt_id' : ckpt_id,'ids' : {}}
    return data

if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument('--race_id', type=str, default=0)
    parser.add_argument('--ckpt_id', type=str, default=0)
    args = parser.parse_args()
    data = init_ckpt_data(args.race_id, args.ckpt_id)
    path = f"races_info/race_{args.race_id}/ckpt_{args.ckpt_id}.json"
    with open(f"races_info/race_{args.race_id}/ckpt_{args.ckpt_id}.json", "w") as f:
        json.dump(data, f)
    real_time_detect(path, args.race_id, args.ckpt_id)
    print(data)
