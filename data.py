import json

def load_quiz():
    with open("data/quiz.json", encoding="utf-8") as f:
        return json.load(f)

def load_jokes():
    with open("data/jokes.json", encoding="utf-8") as f:
        return json.load(f)