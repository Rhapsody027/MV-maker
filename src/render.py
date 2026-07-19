import os
import subprocess

import cv2

from src.visual import render_frame


def generate_video(config):

    img = cv2.imread(config["image"])

    fps = config["fps"]

    width = 1080
    height = 1920

    output = "output/reel.mp4"

    silent = "output/silent.mp4"

    writer = cv2.VideoWriter(
        silent, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )

    total_frames = int(config["duration"] * fps)

    for i in range(total_frames):
        t = i / fps

        frame = render_frame(img, t, config)

        writer.write(frame)

    writer.release()

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i",
        silent,
        "-i",
        config["audio"],
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "320k",
        "-shortest",
        output,
    ])

    os.remove(silent)

    print("DONE:", output)
