def mcq_generator():
    print("\n=== MCQ Generator ===")

    question = input("Enter a question: ")

    options = []
    for i in range(1, 5):
        opt = input(f"Option {i}: ")
        options.append(opt)

    while True:
        correct = input("Correct option number (1-4): ")

        if correct in ("1", "2", "3", "4"):
            correct = int(correct)
            break
        else:
            print(" Invalid input. Please enter a number between 1 and 4.")

    print("\n--- Generated MCQ ---")
    print("Q:", question)

    for i, opt in enumerate(options, start=1):
        print(f"{i}. {opt}")

    print(f"\n Correct Answer: {correct}. {options[correct-1]}")
