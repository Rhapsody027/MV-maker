import os
import subprocess

import cv2
from tqdm import tqdm

from src.visual import render_frame


def open_file(path):
    path = os.path.abspath(path)

    if os.path.exists(path):
        os.startfile(path)
    else:
        print("File not found:", path)


def generate_video(config):

    preview = config.get("preview", True)

    if preview:
        width, height = 540, 960
        bitrate = "800k"
    else:
        width, height = 1080, 1920
        bitrate = "5000k"

    os.makedirs("output", exist_ok=True)

    silent = os.path.abspath("output/silent.mp4")

    output = os.path.abspath("output/reel.mp4")

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
            "medium",
            "-b:v",
            bitrate,
            "-c:a",
            "aac",
            "-b:a",
            "320k",
            "-shortest",
            output,
        ],
        capture_output=True,
        text=True,
    )

    if os.path.exists(silent):
        os.remove(silent)

    if result.returncode != 0:
        print(result.stderr)

        raise Exception("FFmpeg failed")

    if not os.path.exists(output):
        raise Exception("Video was not created: " + output)

    print("DONE:", output)

    open_file(output)
