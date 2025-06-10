import json

# JSON save/load/clean functions
history = [
    {"role": "human", "content": "Hello!"},
    {"role": "ai", "content": "Hi! How can I help you?"}
]
with open("history.json", "w") as f:
    json.dump(history, f, indent=2)

# Load history
with open("history.json") as f:
    loaded = json.load(f)