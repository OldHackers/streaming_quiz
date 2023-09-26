import os
import openai
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
from utils.preprocess import mp4_to_mp3, split_mp3


def extract_video_names(file_path):
    return {
        file.name.split("-")[0]
        for file in file_path.iterdir()
        if file.is_file() and file.name.endswith(".mp4")
    }


def process_videos(video_names, file_path):
    for i, video_name in enumerate(
        tqdm(video_names, desc="Processing mp4 -> mp3, split mp3")
    ):
        mp4_input_path = file_path / f"{video_name}"
        output_name_prefix = video_name[:-4]

        mp3_input_path = Path(f"./{output_name_prefix}.mp3")

        if not mp3_input_path.exists():
            print("mp4 -> mp3 start")
            mp4_to_mp3(str(mp4_input_path), output_name_prefix)

        result_path = Path(f"./result/{output_name_prefix}/{output_name_prefix}_0.mp3")
        if not result_path.exists():
            print("split mp3 start")
            split_mp3(str(mp3_input_path), 180 * 1000, output_name_prefix)


def transcribe_sequences(video_names):
    for video_name in tqdm(video_names, desc="Processing each mp3 seq -> txt"):
        video_name = video_name[:-4]
        sequence_path = Path(f"./result/{video_name}")
        sequences = sorted(
            file.name
            for file in sequence_path.iterdir()
            if file.is_file()
            and file.name.startswith(video_name)
            and file.name.endswith(".mp3")
        )

        for idx, sequence in enumerate(
            tqdm(sequences, desc=f"Processing files for {video_name}", leave=False)
        ):
            with open(sequence_path / sequence, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    "whisper-1", audio_file, language="ko"
                )

                output_dir = Path(f"./result/{video_name}")
                output_dir.mkdir(exist_ok=True)

                output_path = output_dir / f"{video_name}_{idx}.txt"
                with open(output_path, "w") as f:
                    f.write(str(transcript.text))


def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    file_path = Path("/Users/yoonjae/Desktop/23-1/Artificial-Intelligence/Lecture")
    video_names = extract_video_names(file_path)

    process_videos(video_names, file_path)
    transcribe_sequences(video_names)


if __name__ == "__main__":
    main()
