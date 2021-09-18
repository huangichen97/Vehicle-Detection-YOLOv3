import cv2, sys
import logging
import numpy as np

import argparse
import time
from pathlib import Path

import glob
import os


def to_frames(video_file, max_frame=-1):
    out = []
    cap = cv2.VideoCapture(video_file)
    count = 0
    n_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    print("Number of frame {}, fps {}".format(n_frame, frame_rate))
    while count < max_frame or max_frame == -1:
        # Get frame
        ret, frame = cap.read()
        if not ret:
            break
        # Pass frame through yolo detector
        out.append(frame)
        count += 1
    print("Read {} frames".format(count))
    return out


def modify_frame(frames):
    out_frames = []
    count = 0
    for frame in frames:
        # # Crop image to 1:1
        # min_len = min(frame.shape[0], frame.shape[1])
        # frame = frame[:min_len, :min_len]
        # # Resize frame
        # frame = cv2.resize(frame, (344, 344))
        # TODO: pass through yolo and add bounding boxes
        cv2.imwrite('/Users/h1zhen/Downloads/final_processed_data/yolov3-master/out_demo2/' +
                    "frame%d.jpg" % count, frame)
        count += 1


        # model, classes, colors, output_layers = load_yolo()
        # blob, outputs = detect_objects(frame, model, output_layers)
        # boxes, confs, class_ids = get_box_dimensions(outputs, 344, 344)
        # draw_labels(boxes, confs, colors, class_ids, classes, frame)
        # out_frames.append(frame)
    return out_frames


def to_video(frames, name, frame_rate=30):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # out = cv2.VideoWriter(name, cv2.CAP_OPENCV_MJPEG, fourcc, 20.0, (344, 344))
    out = cv2.VideoWriter(name, fourcc, frame_rate, (344, 344))
    for f in frames:
        out.write(f)
    out.release()
    return out


def create_video():
    def get_key(fp):
        filename = os.path.splitext(os.path.basename(fp))[0]
        return int(filename[5:])        # frame###

    img_path = sorted(glob.glob("/Users/h1zhen/Downloads/final_processed_data/yolov3-master/labeled_2/*.jpg"), key=get_key)
    videoWriter = cv2.VideoWriter('demo_2.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 60, (1792, 1006))
    for path in img_path:
        img = cv2.imread(path)
        videoWriter.write(img)


def main(argv):
    video_file = argv[1]
    out_name = video_file.split(".")[0] + "_out" + ".mov"
    print("Processing input video file: {}, Outputing to {}".format(video_file, out_name))
    frames = to_frames(video_file, 1000)
    frames = modify_frame(frames)
    # out_video = to_video(frames, out_name, 10)


if __name__ == "__main__":
    # main(sys.argv)      # transfer video into images(frames)
    create_video()      # transfer labeled images into video
