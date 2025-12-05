import sys

from annotator import main as annotator_main
from cvat import main as cvat_main
from train import main as train_main


def main():
    """
    Main entry point to combine annotator and cvat scripts.
    Dispatches to the appropriate main function based on the first argument.
    """
    if len(sys.argv) < 2:
        print("Usage: python src/main.py [annotate|cvat|train] [args...]")
        print("Available commands: annotate, cvat, train")
        sys.exit(1)

    command = sys.argv[1]
    main_functions = {"annotate": annotator_main, "cvat": cvat_main, "train": train_main}

    if command not in main_functions:
        print(f"Unknown command: {command}")
        print(f"Available commands: {', '.join(main_functions.keys())}")
        sys.exit(1)

    sys.argv = [f"{sys.argv[0]} {command}"] + sys.argv[2:]
    main_functions[command]()


if __name__ == "__main__":
    main()
