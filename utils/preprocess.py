import os
from pydub import AudioSegment


def mp4_to_mp3(input_path, output_name):
    audio = AudioSegment.from_file(input_path, format="mp4")

    # Define the output file path
    output_file = f"{output_name}.mp3"

    # Export as MP3
    audio.export(output_file, format="mp3")
    print(f"Exported {output_file}")


def split_mp3(input_path, chunk_length, output_name):
    audio = AudioSegment.from_file(input_path, format="mp3")

    # Define the length of each chunk (in milliseconds)
    # chunk_length = 180 * 1000  # e.g., 180 seconds

    # Calculate the number of chunks
    num_chunks = len(audio) // chunk_length + (1 if len(audio) % chunk_length else 0)

    # Split the audio and export each chunk
    for i in range(num_chunks):
        start_pos = i * chunk_length
        end_pos = (i + 1) * chunk_length if i < num_chunks - 1 else len(audio)
        chunk = audio[start_pos:end_pos]

        # Construct the output file path
        target_file_name = input_path.split("/")[-1][: -len(".mp3")]
        os.makedirs(f"./result/{target_file_name}", exist_ok=True)
        output_file = f"./result/{target_file_name}/{output_name}_{i}.mp3"
        chunk.export(output_file, format="mp3")
        print(f"Exported {output_file}")
