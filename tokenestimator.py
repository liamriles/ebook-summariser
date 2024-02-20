import os

# Set the instructions as a constant string
INSTRUCTIONS = """
You are a master of writing book chapter summaries. 

Your summaries should distill down the actionable advice in the books and structure your responses as if they were a handy cheat sheet to enable the reader to accelerate their learning process based on what has been outlined in the chapter of the book. 
If there are specific stories or examples, be sure to include a brief outline of them so that it can be linked to the actionable advice.
If the book has passages that are quotes from old texts in hard to read language, do not bring this into the summary. It should be in simple straightforward language that the reader can act on.
Try not to include obvious generic tropes of advice, instead focus on what you think is the unique and practical advice being given. What is the secret sauce of what is being written in the chapter?
Make sure each response has an appropriate title at the beginning, if possible, have this include the chapter name and/or number.
If it looks like the chapter is something like a table of contents, a foreword, an index or anything that really doesn't resemble a chapter of the book that could produce useful advice then do not attempt a summary, just say, "This isn't a proper chapter".

Here is the chapter of the book:
"""

# Prices per 1000 tokens
PRICE_PER_1000_TOKENS_INPUT = 0.01
PRICE_PER_1000_TOKENS_OUTPUT = 0.03

# Estimate the number of tokens in the instructions
instruction_tokens = len(INSTRUCTIONS) / 4  # Rough estimation of tokens

def estimate_file_tokens(file_path):
    """Estimate the number of tokens in a file, including the instructions."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Rough estimation of tokens in the file content
    file_tokens = len(content) / 4
    # Total tokens include both the file content and the instructions
    total_prompt_tokens = instruction_tokens + file_tokens
    return total_prompt_tokens

def estimate_cost(directory_path):
    total_input_tokens = 0
    total_output_tokens = 0  # Assuming one response per file
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            file_tokens = estimate_file_tokens(file_path)
            total_input_tokens += file_tokens
            total_output_tokens += 4095  # Fixed output token count per response
    total_cost_input = (total_input_tokens / 1000) * PRICE_PER_1000_TOKENS_INPUT
    total_cost_output = (total_output_tokens / 1000) * PRICE_PER_1000_TOKENS_OUTPUT
    return total_input_tokens, total_output_tokens, total_cost_input + total_cost_output

if __name__ == "__main__":
    directory_path = '.'  # Current directory
    total_input_tokens, total_output_tokens, total_cost = estimate_cost(directory_path)
    print(f"Estimated total input tokens: {total_input_tokens}")
    print(f"Estimated total output tokens: {total_output_tokens}")
    print(f"Estimated total cost: ${total_cost:.2f}")
