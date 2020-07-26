import os
import re

d = {}
matcher = re.compile(r'^(.*) +\((.*)\)$')
# \\(([^\\(]*)\\)$
def main():
    with open("My Clippings.txt", encoding='utf-8-sig') as f:
        s = f.read()

    annotations = s.split("\n==========\n")

    for a in annotations:
        add_annotation(a)
    print(d)

def add_annotation(annotation):
    lines = annotation.split('\n')
    # print(lines)

    if len(lines) == 4:
        title_author = extract_title_author(lines[0])
        
        if title_author not in d:
            d[title_author] = [lines[3]]
        else:
            d[title_author].append(lines[3])
    elif len(lines) > 4:
        raise "ERROR: There should always be 4 lines"

def extract_title_author(first_line):
    """ Takes the first line of an annotation
        Returns formatted title and author (which is then used as filename) """

    # print(first_line)
    m = matcher.match(first_line)
    # author = author.group(1)

    title = m[1]
    author = m[2]

    return title + " - " + author

if __name__ == "__main__":
    main()