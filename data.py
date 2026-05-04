import json

def load_quiz():
    with open("data/quiz.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
def load_quest():
    with open("data/quest.json", "r", encoding="utf-8") as f:
        return json.load(f)