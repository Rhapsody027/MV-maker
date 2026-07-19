import os

import librosa


def find_file(folder, extensions):

    for file in os.listdir(folder):
        if file.lower().endswith(extensions):
            return os.path.join(folder, file)

    raise Exception(f"No file found in {folder}")


def get_media_files():

    audio = find_file("assets/music", (".wav", ".mp3", ".flac"))

    image = find_file("assets/images", (".jpg", ".jpeg", ".png"))

    return audio, image


def get_audio_duration(path):

    duration = librosa.get_duration(path=path)

    return duration
