import os
from pydub import AudioSegment


def mp4_to_mp3(input_path, output_name, output_format="mp3"):
    """
    Converts an MP4 audio file to MP3 format.

    :param input_path: str, Path to the input MP4 file.
    :param output_name: str, Name of the output MP3 file (without extension).
    :param output_format: str, Format of the output file.
    """
    audio = AudioSegment.from_file(input_path, format="mp4")
    output_file = f"{output_name}.{output_format}"
    audio.export(output_file, format=output_format)
    print(f"Exported {output_file}")


def construct_output_file_path(directory, output_name, index, extension="mp3"):
    """
    Constructs the output file path based on the provided parameters.

    :param directory: str, Target directory for the output file.
    :param output_name: str, Base name of the output file.
    :param index: int, Index of the chunk.
    :param extension: str, Extension of the output file.
    :return: str, Constructed output file path.
    """
    file_name = f"{output_name}_{index:02d}.{extension}"
    return os.path.join(directory, file_name)


def split_mp3(input_path, chunk_length, output_name, input_format="mp3"):
    """
    Splits an MP3 file into chunks of a specified length.

    :param input_path: str, Path to the input MP3 file.
    :param chunk_length: int, Length of each chunk in milliseconds.
    :param output_name: str, Base name of the output chunks.
    :param input_format: str, Format of the input file.
    """
    audio = AudioSegment.from_file(input_path, format=input_format)
    num_chunks = len(audio) // chunk_length + (1 if len(audio) % chunk_length else 0)
    target_directory_name = os.path.splitext(os.path.basename(input_path))[0]
    target_directory = os.path.join("./result", target_directory_name)
    os.makedirs(target_directory, exist_ok=True)

    for i in range(num_chunks):
        start_pos = i * chunk_length
        end_pos = min((i + 1) * chunk_length, len(audio))
        chunk = audio[start_pos:end_pos]
        output_file = construct_output_file_path(target_directory, output_name, i)
        chunk.export(output_file, format=input_format)
        print(f"Exported {output_file}")


# Example Usage:
# mp4_to_mp3("path_to_mp4_file", "output_name")
# split_mp3("path_to_mp3_file", 180000, "output_name")
