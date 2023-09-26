import os
import openai
import logging
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
from utils.preprocess import mp4_to_mp3, split_mp3

logging.basicConfig(level=logging.INFO)

MP4_EXTENSION = ".mp4"
MP3_EXTENSION = ".mp3"
TXT_EXTENSION = ".txt"
RESULT_DIR = "./result"
FILE_PATH = Path("/Users/yoonjae/Desktop/23-1/Artificial-Intelligence/Lecture")


def extract_video_names(file_path: Path) -> set[str]:
    return {
        file.stem.split("-")[0]
        for file in file_path.iterdir()
        if file.is_file() and file.suffix == MP4_EXTENSION
    }


def process_videos(video_names: set[str], file_path: Path) -> None:
    for video_name in tqdm(video_names, desc="Processing mp4 -> mp3, split mp3"):
        mp4_input_path = file_path / f"{video_name}{MP4_EXTENSION}"
        output_name_prefix = video_name

        mp3_input_path = Path(f"./{output_name_prefix}{MP3_EXTENSION}")

        if not mp3_input_path.exists():
            logging.info("mp4 -> mp3 start")
            mp4_to_mp3(str(mp4_input_path), output_name_prefix)

        result_path = Path(
            f"{RESULT_DIR}/{output_name_prefix}/{output_name_prefix}_0{MP3_EXTENSION}"
        )
        if not result_path.exists():
            logging.info("split mp3 start")
            split_mp3(str(mp3_input_path), 180 * 1000, output_name_prefix)


def transcribe_sequence(
    sequence_path: Path, sequence: str, idx: int, video_name: str
) -> None:
    with open(sequence_path / f"{sequence}{MP3_EXTENSION}", "rb") as audio_file:
        try:
            transcript = openai.Audio.transcribe("whisper-1", audio_file, language="ko")
        except Exception as e:
            logging.error(f"Error transcribing audio: {e}")
            return

    output_path = sequence_path / f"{video_name}_{idx}{TXT_EXTENSION}"
    with open(output_path, "w") as f:
        f.write(str(transcript.text))


def transcribe_sequences(video_names: set[str]) -> None:
    for video_name in tqdm(video_names, desc="Processing each mp3 seq -> txt"):
        sequence_path = Path(f"{RESULT_DIR}/{video_name}")
        sequences = sorted(
            file.stem
            for file in sequence_path.iterdir()
            if file.is_file()
            and file.name.startswith(video_name)
            and file.suffix == MP3_EXTENSION
        )

        for idx, sequence in enumerate(
            tqdm(sequences, desc=f"Processing files for {video_name}", leave=False)
        ):
            transcribe_sequence(sequence_path, sequence, idx, video_name)


def main() -> None:
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    video_names = extract_video_names(FILE_PATH)
    process_videos(video_names, FILE_PATH)
    transcribe_sequences(video_names)


if __name__ == "__main__":
    main()
