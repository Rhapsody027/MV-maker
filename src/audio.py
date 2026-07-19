import hashlib
import json
import os

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
    name = hashlib.md5(path.encode()).hexdigest()

    return f"output/{name}_beats.json"


def get_beats(path):

    cache = get_cache_name(path)

    if os.path.exists(cache):
        with open(cache, "r") as f:
            return json.load(f)

    print("Analyzing beats...")

    y, sr = librosa.load(path, sr=None)

    _, beats = librosa.beat.beat_track(y=y, sr=sr)

    times = librosa.frames_to_time(beats, sr=sr)

    beats = times.tolist()

    os.makedirs("output", exist_ok=True)

    with open(cache, "w") as f:
        json.dump(beats, f)

    return beats
