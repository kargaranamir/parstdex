
def test():
    for i in range(1,21):
        with open(f"./in/input{i}.txt", 'r') as infile:
            s = infile.read()
            print(s)


test()