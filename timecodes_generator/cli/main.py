import argparse

from timecodes_generator.core.generate_timecodes import generate_timecodes
from timecodes_generator.core.load import load_whisper_model


class CliError(Exception):
    pass


def main():
    parser = argparse.ArgumentParser(prog="Timecodes generator")
    parser.add_argument("file_path", help="Path to an audio file to process")

    args = parser.parse_args()

    print("Loading a model")
    model = load_whisper_model("small.en")

    print("Transcribing", "\n")
    timecodes = generate_timecodes(model, args.file_path)

    for timecode in timecodes:
        print(timecode)


if __name__ == "__main__":
    main()
