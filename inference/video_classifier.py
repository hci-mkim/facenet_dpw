#!/usr/bin/env python

from os import path
import joblib
import cv2
import argparse
import numpy as np
from PIL import Image
from face_recognition import preprocessing
from .util import draw_bb_on_img
from .constants import MODEL_PATH
import time

'python -m inference.video_classifier --video-path /home/dpw/codes/face-recognition/test/videoplayback.mp4 --save-dir videoplayback_output.mp4'

def parse_args():
    parser = argparse.ArgumentParser(
        'Visualize result and save as a mp4 format. save dir will be in "result" folder')
    parser.add_argument('--video-path', required=True, help='Path to image file.')
    parser.add_argument('--save-dir', help='If save dir is provided image will be saved to specified directory.')
    return parser.parse_args()

def main():
    args = parse_args()

    # cap = cv2.VideoCapture(0) #webcam

    cap = cv2.VideoCapture(args.video_path)
    face_recogniser = joblib.load(MODEL_PATH)
    preprocess = preprocessing.ExifOrientationNormalize()
    prevTime = 0 
    save_dir = args.save_dir

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter('./result/'+save_dir, cv2.VideoWriter_fourcc(*'mp4v'),25, (width, height))


    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        curTime = time.time()
        sec = curTime - prevTime
        prevTime = curTime
        
        fps = 1 / (sec)

        #Remark FPS in video
        str = "FPS : %0.1f" % fps
        cv2.putText(frame, str, (5, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
        
        #img to array
        img = Image.fromarray(frame)
        faces = face_recogniser(preprocess(img))
        if faces is not None:
            draw_bb_on_img(faces, img)

        # Display the resulting frame
        cv2.imshow('video', np.array(img))
        # Save the video
        writer.write(np.array(img))

        # Quit button('q')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    writer.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
