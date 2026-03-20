import os

def main():
    file_path = os.path.join("data", "frankenstein.txt")
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                print(line.strip())
    except BrokenPipeError:
        # Standard behavior when piping to a tool like head
        pass

if __name__ == "__main__":
    main()
