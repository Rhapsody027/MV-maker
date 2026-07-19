import os
import subprocess

import cv2
from tqdm import tqdm

from src.visual import render_frame


def open_file(path):

    if os.path.exists(path):
        os.startfile(os.path.abspath(path))


def generate_video(config):

    preview = config.get("preview", True)

    if preview:
        width, height = 540, 960
        bitrate = "1000k"
        preset = "veryfast"
    else:
        width, height = 1080, 1920
        bitrate = "6000k"
        preset = "slow"

    os.makedirs("output", exist_ok=True)

    silent = "output/.silent.mp4"
    output = "output/reel.mp4"

    img = cv2.imread(config["image"])

    writer = cv2.VideoWriter(
        silent, cv2.VideoWriter_fourcc(*"mp4v"), config["fps"], (width, height)
    )

    total = int(config["duration"] * config["fps"])

    for i in tqdm(range(total), desc="Rendering"):
        t = i / config["fps"]

        frame = render_frame(img, t, config, width, height, preview)

        writer.write(frame)

    writer.release()

    print("Encoding video...")

    result = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            silent,
            "-i",
            config["audio"],
            "-c:v",
            "libx264",
            "-preset",
            preset,
            "-b:v",
            bitrate,
            "-c:a",
            "aac",
            "-b:a",
            "320k",
            "-shortest",
            output,
        ],
        text=True,
    )

    if os.path.exists(silent):
        os.remove(silent)

    if result.returncode != 0:
        raise Exception("FFmpeg failed")

    if not os.path.exists(output):
        raise Exception("Output missing")

    print("DONE:", output)

    open_file(output)
