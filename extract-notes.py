import os

d = {}

def main():
    with open("My Clippings.txt") as f:
        s = f.read()

    annotations = s.split("\n==========\n")

    for a in annotations:
        add_to_dict(a)

def add_to_dict(annotation):
    lines = annotation.split('\n')

    if len(lines) >= 3:
        print(lines)
    

if __name__ == "__main__":
    main()