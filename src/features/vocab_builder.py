import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "vocab_data.json")

def load_data():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(words):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

def add_word(words):
    word = input("Word: ").strip()
    meaning = input("Meaning: ").strip()
    example = input("Example sentence: ").strip()

    if not word:
        print("❌ Word cannot be empty")
        return

    words.append({"word": word, "meaning": meaning, "example": example})
    save_data(words)
    print("✅ Saved!")

def list_words(words):
    if not words:
        print("⚠️ No words saved yet.")
        return
    print("\n=== Your Vocabulary ===")
    for i, w in enumerate(words, start=1):
        print(f"{i}. {w['word']} - {w['meaning']}")
        if w.get("example"):
            print(f"   Example: {w['example']}")
    print()

def search_word(words):
    key = input("Search word: ").strip().lower()
    found = [w for w in words if key in w["word"].lower()]
    if not found:
        print("❌ Not found")
        return
    for w in found:
        print(f"✅ {w['word']} - {w['meaning']}")
        if w.get("example"):
            print(f"   Example: {w['example']}")

def vocab_builder():
    words = load_data()

    while True:
        print("\n=== Vocabulary Builder ===")
        print("1. Add new word")
        print("2. Show all words")
        print("3. Search word")
        print("4. Back to main menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_word(words)
            words = load_data()
        elif choice == "2":
            list_words(words)
        elif choice == "3":
            search_word(words)
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice. Try 1-4.")
