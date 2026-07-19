import json

from src.audio import get_audio_duration, get_beats, get_media_files
from src.render import generate_video


def main():

    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    audio, image = get_media_files()

    config["audio"] = audio
    config["image"] = image
    config["duration"] = get_audio_duration(audio)
    config["beats"] = get_beats(audio)
    config["drop_time"] = config["drop_cs"] / 100

    generate_video(config)


if __name__ == "__main__":
    main()
