import json
import os
import re

import librosa


def find_file(folder, extensions):
    for file in os.listdir(folder):
        if file.lower().endswith(extensions):
            return os.path.join(folder, file)

    raise Exception(f"File not found: {folder}")


def get_media_files():
    audio = find_file("assets/music", (".wav", ".mp3", ".flac"))

    image = find_file("assets/images", (".jpg", ".jpeg", ".png"))

    return audio, image


def get_audio_duration(path):
    return librosa.get_duration(path=path)


def get_cache_name(path):

    os.makedirs("cache", exist_ok=True)

    name = os.path.splitext(os.path.basename(path))[0]

    name = re.sub(r"[^a-zA-Z0-9_-]", "_", name)

    return f"cache/{name}_beats.json"


def get_beats(path):

    cache = get_cache_name(path)

    if os.path.exists(cache):
        with open(cache, "r", encoding="utf-8") as f:
            return json.load(f)

    print("Analyzing beats...")

    y, sr = librosa.load(path, sr=None)

    _, beats = librosa.beat.beat_track(y=y, sr=sr)

    times = librosa.frames_to_time(beats, sr=sr)

    beats = times.tolist()

    with open(cache, "w", encoding="utf-8") as f:
        json.dump(beats, f)

    return beats
