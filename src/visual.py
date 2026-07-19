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


def render_frame(img, t, config):

    w = 1080
    h = 1920

    frame = resize_cover(img, w, h)

    drop = config["drop_time"]

    # camera movement

    if t < drop:
        progress = t / config["duration"]

        zoom = 1 + progress * 0.08

    else:
        zoom = 1.12

    frame = cv2.resize(frame, None, fx=zoom, fy=zoom)

    fh, fw, _ = frame.shape

    x = (fw - w) // 2
    y = (fh - h) // 2

    frame = frame[y : y + h, x : x + w]

    # drop flash

    if drop <= t <= drop + 0.2:
        frame = np.clip(frame.astype(float) * 1.8, 0, 255).astype(np.uint8)

    # hook

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

    # title

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
