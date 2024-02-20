import os
import openai
from pathlib import Path

# Set your OpenAI API key here
openai.api_key = 'insert your OpenAI api key here'

# Set the directory path where your txt files are located
directory_path = '.'

# Instructions to prepend to each file content
instructions = """
You are a master of writing book chapter summaries.  

Your summaries should distill down the actionable advice in the books and structure your responses as if they were a handy cheat sheet to enable the reader to accelerate their learning process based on what has been outlined in the chapter of the book. 
If there are specific stories or examples in the chapter, be sure to explain exactly what happened and how the outcome was achieved so that it can be linked to the actionable advice.
If the book has passages that are quotes from old texts in hard to read language, do not bring this into the summary. It should be in simple straightforward language that the reader can act on.
Try not to include obvious generic tropes of advice, instead focus on what you think is the unique and practical advice being given. What is the secret sauce of what is being written in the chapter?
Make sure each response has an appropriate title at the beginning, if possible, have this include the chapter name and/or number.
If it looks like the chapter is something like a table of contents, a foreword, an index or anything that really doesn't resemble a chapter of the book that could produce useful advice then do not attempt a summary, just say, "This isn't a proper chapter".
Here is the chapter of the book:
"""

# Output Markdown file
output_file = 'book_summary.md'

# Function to count words in a file
def word_count(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return len(text.split())

# Function to generate prompt and get response from OpenAI API, along with token usage
def generate_response(file_path, instructions):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    prompt = f"{instructions}{content}"  # Include instructions in the prompt
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4095
    )
    
    if response.choices:
        content = response.choices[-1].message['content'].strip()
        token_usage = response['usage']['total_tokens']  # Extract token usage
        return content, token_usage
    else:
        return "No response generated.", 0

# Main function to process files and generate markdown
def process_files(directory_path, instructions, output_file):
    files_processed = 0
    total_token_usage = 0  # Initialize total token usage
    with open(output_file, 'w', encoding='utf-8') as md_file:
        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                if word_count(file_path) < 150:
                    print(f"Skipping {filename}: less than 150 words")
                    continue
                print(f"Processing {filename}...")
                response, token_usage = generate_response(file_path, instructions)
                md_file.write(f"## Response for {filename}\n\n")
                md_file.write(f"{response}\n\n")
                files_processed += 1
                total_token_usage += token_usage  # Accumulate token usage
                print(f"Saved response for {filename} into {output_file}")
        # Write total token usage at the end of the Markdown file
        md_file.write(f"Total token usage for processing {files_processed} files: {total_token_usage} tokens\n")
    print(f"Processed {files_processed} files with total token usage of {total_token_usage} tokens.")

# Run the script
if __name__ == "__main__":
    process_files(directory_path, instructions, output_file)
