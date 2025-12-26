import time

def start_study_timer():
    print("\n Study Time Started (25 minutes)")

    for i in range(25, 0, -1):
        print(f" {i} minutes remaining...", end="\r")
        time.sleep(60)

    print("\n Study session completed!")
    print(" Break Time (5 minutes)")

    for i in range(5, 0, -1):
        print(f" Break: {i} minutes remaining...", end="\r")
        time.sleep(60)

    print("\n Ready for next session!")
