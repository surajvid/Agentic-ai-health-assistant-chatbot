from pathlib import Path


def main():
    log_file = Path("logs/app.log")

    if not log_file.exists():
        print("No log file found.")
        return

    print("LAST 30 LOG LINES:\n")

    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines[-30:]:
        print(line.rstrip())


if __name__ == "__main__":
    main()