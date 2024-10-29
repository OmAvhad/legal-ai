import tiktoken

def count_tokens(text, model="gpt-4"):
    # Load the tokenizer for the specified model
    encoding = tiktoken.encoding_for_model(model)
    
    # Encode the text and get the number of tokens
    tokens = encoding.encode(text)
    token_count = len(tokens)
    
    return token_count

# Example usage
text = "Your sample text goes here."
model = "gpt-4"  # Change this to your desired model

# Read text from output.txt
with open('op1.txt', 'r', encoding='utf-8') as file:
    text = file.read()

print(f"Token count for the given text: {count_tokens(text, model)}")