import openai
import pytesseract
from PIL import Image
import torch
from sentence_transformers import SentenceTransformer, util

openai.api_key = "your-api-key"

def extract_email(email_text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Extract the sender's email address"},
                  {"role": "user", "content": email_text}]
    )
    return response["choices"][0]["message"]["content"].strip()

def extract_credit_card(image_path):
    image = Image.open(image_path)
    card_text = pytesseract.image_to_string(image)
    return "".join(filter(str.isdigit, card_text))

def find_similar_comments():

    with open("./data/comments.txt", "r") as f:
        comments = [line.strip() for line in f.readlines()]

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(comments, convert_to_tensor=True)

    scores = util.cos_sim(embeddings, embeddings)  # Ensure proper matrix form
    scores.fill_diagonal_(-1)  # Ignore self-similarity

    idx = torch.argmax(scores).item()
    row, col = divmod(idx, scores.shape[1])

    similar_comments = [comments[row], comments[col]]

    with open("./data/comments-similar.txt", "w") as f:
        f.write("\n".join(similar_comments))

    return "Similar comments found."
