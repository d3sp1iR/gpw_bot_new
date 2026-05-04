import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_jokes():
    path = os.path.join(BASE_DIR, "data", "jokes.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def load_quiz():
    path = os.path.join(BASE_DIR, "data", "quiz.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)