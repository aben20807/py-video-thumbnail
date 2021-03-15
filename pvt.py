#!/usr/bin/env python3
# -*- coding: utf-8 -*-

helpDoc = """
Create thumbnail from a video (default 4x4).
usage:
    python pvt.py [video path]
require:
    pip install opencv-python
    Support Python3
Author:
    Huang Po-Hsuan (aben20807@gmail.com)
GitHub:
    https://github.com/aben20807/py-video-thumbnail
"""
print(helpDoc)

import os
import sys
import cv2
import time
import numpy as np


def concat_vh(list_2d):
    return cv2.vconcat([cv2.hconcat(list_h) for list_h in list_2d])


def video_to_frames(video_filename, num_of_frames):
    """Extract frames from video"""
    cap = cv2.VideoCapture(video_filename)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) * 0.94)
    frames = []
    if cap.isOpened() and total_frames > 0:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, image = cap.read()
        for i in range(1, num_of_frames + 1):
            cap.set(cv2.CAP_PROP_POS_FRAMES, round(total_frames * i / num_of_frames))
            success, image = cap.retrieve()
            if not success:
                break
            frames.append(image)
    return frames


def process(video_path, shape=(4, 4), img_format=".jpg", skip_exist=True):
    """Extract frames from the video and creates thumbnails for one of each"""
    output_path = os.path.splitext(video_path)[0] + img_format
    if os.path.isfile(output_path) and skip_exist:
        print(f"'{output_path}' exist, ignore")
        return

    print(f"Processing '{video_path}'")
    # Extract frames from video
    frames = video_to_frames(video_path, shape[0] * shape[1])
    thumbnail_shape = [shape, frames[0].shape]
    thumbnail_shape = [i for sub in thumbnail_shape for i in sub]
    frames = np.reshape(frames, thumbnail_shape)

    # Generate and save combined thumbnail
    thumbnail = concat_vh(frames)
    thumbnail_size = (frames[0][0].shape[1], frames[0][0].shape[0])
    thumbnail = cv2.resize(thumbnail, thumbnail_size, interpolation=cv2.INTER_AREA)
    cv2.imwrite(output_path, thumbnail)


if __name__ == "__main__":
    videos = sys.argv[1:]
    print(f"Total: {len(videos)} videos")
    for v in videos:
        process(v)