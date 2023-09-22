import openai, os
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
from utils.preprocess import mp4_to_mp3, split_mp3


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


FILE_PATH = "/Users/yoonjae/Desktop/23-1/Artificial-Intelligence/Lecture"


file_path = Path(FILE_PATH)

"""
Extract all video names from the file path
"""
video_names = set()
video_names.update(
    file.name.split("-")[0]
    for file in file_path.iterdir()
    if file.is_file() and file.name.endswith(".mp4")
)

"""
1. mp4 -> mp3
2. split mp3 into 3m chunks
"""
for i, video_name in enumerate(
    tqdm(video_names, desc="Processing mp4 -> mp3, split mp3")
):
    mp4_input_path = FILE_PATH + "/" + video_name  # include .mp4
    output_name_prefix = f"{video_name[:-4]}"
    mp3_input_path = "./" + output_name_prefix + ".mp3"
    if not os.path.exists(mp3_input_path):
        print("mp4 -> mp3 start")
        mp4_to_mp3(mp4_input_path, output_name_prefix)
    if not os.path.exists(Path(f"./result/{output_name_prefix}_0.mp3")):
        print("split mp3 start")
        split_mp3(
            mp3_input_path,
            180 * 1000,
            output_name_prefix,
        )

"""
3. each mp3 seq -> text using whisper-1
4. save text
"""

for video_name in tqdm(video_names, desc="Processing each mp3 seq -> txt"):
    video_name = video_name[:-4]
    sequence_path = Path(f"./result/{video_name}")
    sequences = [
        file.name
        for file in sequence_path.iterdir()
        if file.is_file() and file.name.startswith(video_name)
    ]
    sequences.sort()

    for idx, sequence in enumerate(
        tqdm(sequences, desc=f"Processing files for {video_name}", leave=False)
    ):
        audio_file = open(
            os.path.join(sequence_path, sequence),
            "rb",
        )
        transcript = openai.Audio.transcribe("whisper-1", audio_file, language="ko")

        if not os.path.exists(f"./result/{video_name}"):
            os.mkdir(f"./result/{video_name}")

        output_path = f"./result/{video_name}/{video_name}_{idx}.txt"

        with open(output_path, "w") as f:
            f.write(str(transcript.text))
