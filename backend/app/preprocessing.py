import re

def preprocess_text(body: str, subject: str = None) -> str:
    """
    Cleans and preprocesses the input email text.
    Combines subject and body if subject is provided.
    
    Steps:
    - Combine subject and body
    - Lowercase text
    - Handle URLs
    - Remove special characters but keep some punctuation ($ ! ?)
    - Normalize whitespace
    """
    if not isinstance(body, str):
        body = ""
        
    text = body
    if subject and isinstance(subject, str):
        text = f"{subject} {body}"
        
    text = text.lower()
    
    # Replace URLs with the word 'http'
    text = re.sub(r'http\S+|www\S+|https\S+', ' ', text, flags=re.MULTILINE)
    
    # Keep some punctuation ($ ! ?), remove others
    text = re.sub(r'[^\w\s$!?]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
