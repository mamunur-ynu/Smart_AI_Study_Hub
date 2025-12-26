from features.study_timer import start_study_timer
from features.text_to_speech import text_to_speech
from features.mcq_generator import mcq_generator
from features.vocab_builder import vocab_builder


def main():
    while True:
        print("\n=== Smart AI Study Hub ===")
        print("1. Study Timer (Pomodoro)")
        print("2. Text to Speech")
        print("3. MCQ Generator")
        print("4. Vocabulary Builder")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            start_study_timer()

        elif choice == "2":
            text_to_speech()

        elif choice == "3":
            mcq_generator()

        elif choice == "4":
            vocab_builder()

        elif choice == "5":
            print("👋 Goodbye! Keep studying smart.")
            break

        else:
            print("❌ Invalid choice. Please enter 1–5.")


if __name__ == "__main__":
    main()
