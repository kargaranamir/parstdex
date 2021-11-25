from timeMarkerExtractor import time_marker_extractor


def main():
    for i in range(1, 21):
        with open(f"./test/in/input{i}.txt", 'r', encoding="utf8") as infile:
            s = infile.read()
            print("Original Sentence:")
            print(s)
            time_marker_extractor(s)
            print("=" * 50)


if __name__ == '__main__':
    main()
