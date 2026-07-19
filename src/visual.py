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


def apply_color(frame, mode):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)

    if mode == "vocal":
        hsv[:, :, 1] *= 0.65
        hsv[:, :, 2] *= 0.75
    else:
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.35, 0, 255)

        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.15, 0, 255)

    hsv = np.clip(hsv, 0, 255).astype(np.uint8)

    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def bloom(frame):
    blur = cv2.GaussianBlur(frame, (0, 0), 25)

    return cv2.addWeighted(frame, 1, blur, 0.3, 0)


def beat_punch(frame, t, config):
    hit = False

    for beat in config.get("beats", []):
        if abs(t - beat) < 0.04:
            hit = True
            break

    if not hit:
        return frame

    h, w, _ = frame.shape

    scale = 1.03

    nw = int(w / scale)
    nh = int(h / scale)

    x = (w - nw) // 2
    y = (h - nh) // 2

    crop = frame[y : y + nh, x : x + nw]

    return cv2.resize(crop, (w, h))


def render_frame(img, t, config, w, h, preview=False):

    frame = resize_cover(img, w, h)

    drop = config["drop_time"]

    mode = "vocal" if t < drop else "drop"

    if t < drop:
        zoom = 1 + (t / max(drop, 0.01)) * 0.08
    else:
        zoom = 1.12

    frame = cv2.resize(frame, None, fx=zoom, fy=zoom)

    fh, fw, _ = frame.shape

    x = (fw - w) // 2
    y = (fh - h) // 2

    frame = frame[y : y + h, x : x + w]

    frame = apply_color(frame, mode)

    if mode == "drop" and not preview:
        frame = bloom(frame)

    if drop <= t <= drop + 0.15:
        frame = np.clip(frame.astype(float) * 1.8, 0, 255).astype(np.uint8)

    frame = beat_punch(frame, t, config)

    if not preview:
        noise = np.random.normal(0, 8, frame.shape)

        frame = np.clip(frame.astype(float) + noise, 0, 255).astype(np.uint8)

    if t < drop:
        cv2.putText(
            frame,
            config["hook"],
            (50, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (255, 255, 255),
            2,
        )

    cv2.putText(
        frame,
        config["title"],
        (50, h - 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (255, 255, 255),
        2,
    )

    return frame
