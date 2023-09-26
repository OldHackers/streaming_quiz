import os
import openai
from dotenv import load_dotenv
from prompt import PROMPT as BASE_PROMPT


load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


GPT_MODEL = "gpt-4"
LECTURE_DIR = "./result/Lecture13/"
INPUT_FILE = os.path.join(LECTURE_DIR, "lec4.txt")
OUTPUT_FILE = os.path.join(".", "result_5.txt")
PROMPT = BASE_PROMPT


class QuizGenerator:
    """
    A class used to generate quiz using OpenAI API.
    """

    def __init__(self, api_key, model=GPT_MODEL, prompt=PROMPT):
        """
        Initializes a new instance of the QuizGenerator class.

        :param api_key: str, OpenAI API key.
        :param model: str, Model to be used for generating quiz.
        :param prompt: str, Prompt to be used as a base for generating quiz.
        """
        openai.api_key = api_key
        self.model = model
        self.prompt = prompt

    def get_quiz(self, subtitle):
        """
        Generates a quiz based on the provided subtitle.

        :param subtitle: str, Subtitle to be used for generating a quiz.
        :return: str, Generated quiz.
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": subtitle},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error occurred: {e}")
            return ""


def read_file(file_path):
    """
    Reads the content of a file.

    :param file_path: str, Path to the file.
    :return: str, Content of the file.
    """
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return ""


def write_file(file_path, content):
    """
    Writes content to a file.

    :param file_path: str, Path to the file.
    :param content: str, Content to be written to the file.
    """
    try:
        with open(file_path, "w") as f:
            f.write(content)
    except Exception as e:
        print(f"Error occurred while writing to {file_path}: {e}")


def main():
    subtitle = read_file(INPUT_FILE)
    if subtitle:
        quiz_generator = QuizGenerator(api_key=API_KEY)
        response = quiz_generator.get_quiz(subtitle)
        if response:
            write_file(OUTPUT_FILE, response)


if __name__ == "__main__":
    main()
