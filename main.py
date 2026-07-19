import json

from src.audio import get_audio_duration, get_media_files
from src.render import generate_video


def main():

    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    audio_file, image_file = get_media_files()

    duration = get_audio_duration(audio_file)

    config["audio"] = audio_file
    config["image"] = image_file
    config["duration"] = duration

    config["drop_time"] = config["drop_cs"] / 100

    generate_video(config)


if __name__ == "__main__":
    main()
