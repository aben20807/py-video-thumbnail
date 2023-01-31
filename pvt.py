#!/usr/bin/env python3
# -*- coding: utf-8 -*-

helpDoc = """
Create thumbnail from a video (default 4x4).
usage:
    python pvt.py -d '[video folder]' 2>/dev/null
    details can be accessed by: python pvt.py -h
example:
    python pvt.py -d 'videos/' 2>/dev/null
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
import argparse
import glob


def concat_vh(list_2d):
    return cv2.vconcat([cv2.hconcat(list_h) for list_h in list_2d])


def video_to_frames(video_filename, num_of_frames):
    """Extract frames from video"""
    cap = cv2.VideoCapture(video_filename)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) * 0.94)
    frames = []
    if cap.isOpened() and total_frames > 0:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, image = cap.retrieve()
        blank = np.zeros(
            (image.shape[0], image.shape[1], image.shape[2]), dtype="uint8"
        )
        for i in range(1, num_of_frames + 1):
            cap.set(cv2.CAP_PROP_POS_FRAMES, round(total_frames * i / num_of_frames))
            success, image = cap.retrieve()
            if not success:
                break
            frames.append(image)
    return frames


def process(
    video_path, shape=(4, 4), img_format=".jpg", skip_exist=True, verbose_level=2
):
    """Extract frames from the video and creates thumbnails for one of each"""
    output_path = os.path.splitext(video_path)[0] + img_format
    if os.path.isfile(output_path) and skip_exist:
        if verbose_level >= 2:
            print(f"'{output_path}' exist, ignore")
        return

    if not os.path.isfile(video_path) and verbose_level >= 1:
        if verbose_level >= 1:
            print(f"'{video_path}' is not a file, ignore")
        return

    if verbose_level >= 2:
        print(f"Processing '{video_path}'")
    # Extract frames from video
    frames = video_to_frames(video_path, shape[0] * shape[1])
    try:
        thumbnail_shape = [shape, frames[0].shape]
    except IndexError as e:
        print(video_path, str(e))
        return
    thumbnail_shape = [i for sub in thumbnail_shape for i in sub]
    frames = np.resize(frames, np.prod(thumbnail_shape))
    frames = np.reshape(frames, thumbnail_shape)

    # Generate and save combined thumbnail
    thumbnail = concat_vh(frames)
    thumbnail_size = (frames[0][0].shape[1], frames[0][0].shape[0])
    thumbnail = cv2.resize(thumbnail, thumbnail_size, interpolation=cv2.INTER_AREA)
    cv2.imwrite(output_path, thumbnail)


def get_parser():
    parser = argparse.ArgumentParser(
        description="Create thumbnail from a video",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-s", "--shape", type=int, default=4, help="use NxN grid")
    parser.add_argument("-k", "--exist", action="store_false", help="skip exist")
    parser.add_argument(
        "-v",
        "--verbose",
        type=int,
        default=2,
        choices=[0, 1, 2, 3],
        help="verbose level",
    )
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        default="mp4,avi,mkv,m4v,flv,wmv",
        help="extensions for video",
    )
    parser.add_argument("-i", "--input", type=str, default="", help="single input")
    parser.add_argument(
        "-d",
        "--input_dir",
        type=str,
        default="",
        help="folder for processing recursively",
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    print("Setting:")
    print(f"shape: {args.shape}x{args.shape}")
    print(f"skip_exist: {args.exist}")
    print(f"verbose: {args.verbose}")
    videos = []
    if args.input != "":
        videos.append(args.input)
    if args.input_dir != "":
        for ext in args.extension.split(","):
            videos.extend(
                glob.glob(os.path.join(args.input_dir, "**/*." + ext), recursive=True)
            )
    if args.verbose >= 3:
        print(f"videos: {videos}")
    print(
        f"Total: {len(videos)} videos{' (nothing to do...)' if len(videos) == 0 else ''}"
    )

    for v in videos:
        process(
            v,
            shape=(args.shape, args.shape),
            skip_exist=args.exist,
            verbose_level=args.verbose,
        )


if __name__ == "__main__":
    main()
