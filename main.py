from timeMarkerExtractor import time_marker_extractor


def test():
    for i in range(1, 21):
        with open(f"./test/in/input{i}.txt", 'r', encoding="utf8") as infile:
            s = infile.read()
            print(s)
            print(time_marker_extractor(s))


test()
