PROMPT = """
You will be provided with a segment of a subtitle containing the words of a university lecturer, 
along with a sequence number. Your task is to create a quiz to assess whether a student has properly understood the 
lecture based on this caption. Formulate a question that probes the understanding of the lecture's main content. 
The quiz should be structured as follows:

The response MUST be a JSON object containing the following keys:
- Language: MUST be Korean.
- question: a string representing the quiz question.
- choices: an array of strings, with a size of 4, representing the possible answers.
- answer: a number between 1-4, representing the correct answer's index.
- index: a number representing the sequence number of the provided subtitle.
- commentary: a string providing an explanation of the answer.

Example:
{
  "Language": "Korean",
  "question": "What is the main topic of the lecture?",
  "choices": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "answer": 2,
  "index": 1,
  "commentary": "Option 2 is the correct answer because..."
}
"""
