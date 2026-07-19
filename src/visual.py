import random

import cv2
import numpy as np


def resize_cover(img, w, h):

    ih, iw, _ = img.shape

    scale = max(w / iw, h / ih)

    nw = int(iw * scale)
    nh = int(ih * scale)

    img = cv2.resize(img, (nw, nh))

    x = (nw - w) // 2
    y = (nh - h) // 2

    return img[y : y + h, x : x + w]


def apply_color_grade(frame, mode):

    img = frame.astype(np.float32) / 255

    if mode == "vocal":
        # 暗、冷、低飽和

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        hsv[:, :, 1] = hsv[:, :, 1] * 0.65
        hsv[:, :, 2] = hsv[:, :, 2] * 0.75

        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    else:
        # drop 高對比、高飽和

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.35, 0, 255)

        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.15, 0, 255)

        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        frame = cv2.convertScaleAbs(frame, alpha=1.15, beta=5)

    return frame


def apply_bloom(frame, strength=0.25):

    blur = cv2.GaussianBlur(frame, (0, 0), 25)

    result = cv2.addWeighted(frame, 1, blur, strength, 0)

    return result


def apply_grain(frame):

    noise = np.random.normal(0, 8, frame.shape)

    noisy = frame.astype(np.float32) + noise

    return np.clip(noisy, 0, 255).astype(np.uint8)


def camera_transform(frame, t, config):

    drop = config["drop_time"]

    if t < drop:
        # Vocal 慢慢推近

        progress = t / drop

        zoom = 1 + progress * 0.08

        offset_x = int(np.sin(t * 0.5) * 10)

    else:
        # Drop 更有侵略性

        progress = min((t - drop) / 2, 1)

        zoom = 1.1 + progress * 0.05

        offset_x = int(np.sin(t * 5) * 8)

    h, w, _ = frame.shape

    nw = int(w / zoom)
    nh = int(h / zoom)

    x = (w - nw) // 2 + offset_x
    y = (h - nh) // 2

    cropped = frame[y : y + nh, x : x + nw]

    return cv2.resize(cropped, (w, h))


def render_frame(img, t, config):

    w = 1080
    h = 1920

    frame = resize_cover(img, w, h)

    drop = config["drop_time"]

    if t < drop:
        mode = "vocal"

    else:
        mode = "drop"

    # camera

    frame = camera_transform(frame, t, config)

    # color

    frame = apply_color_grade(frame, mode)

    # bloom

    if mode == "drop":
        frame = apply_bloom(frame, 0.35)

    # flash transition

    if drop <= t <= drop + 0.15:
        frame = np.clip(frame.astype(float) * 1.8, 0, 255).astype(np.uint8)

    # grain

    frame = apply_grain(frame)

    # Hook

    if t < drop:
        cv2.putText(
            frame,
            config["hook"],
            (80, 300),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            3,
        )

    # Title

    cv2.putText(
        frame,
        config["title"],
        (80, 1700),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (255, 255, 255),
        2,
    )

    return frame
