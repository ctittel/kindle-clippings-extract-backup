import os
import re

matcher = re.compile(r'^(.*) +\((.*)\)$')
annotations_dict = {}

class BookData:
    def __init__(self, title, authors):
        self.authors = tuple(authors) # list of authors
        self.title = title
    
    def __eq__(self, another):
        return ((self.authors == another.authors) and (self.title == another.title))

    def __hash__(self):
        return hash(self.title + " " + " ".join(self.authors))

def main():
    with open("My Clippings.txt", encoding='utf-8-sig') as f:
        s = f.read()

    annotations = s.split("\n==========\n")
    for a in annotations:
        add_annotation_to_dict(a)
    write_annotations_to_files()

def add_annotation_to_dict(annotation):
    """ Takes an annotation block (between the == in the My Clippings file)
        Add annotation to dict """
    lines = annotation.split('\n')
    
    if len(lines) == 4:
        m = matcher.match(lines[0])
        title = m[1]
        authors = m[2].split(';')
        text = lines[3]

        # Build a BookData object (used as key)
        fn = BookData(title, authors)

        if fn not in annotations_dict:
            annotations_dict[fn] = [text]
        else:
            annotations_dict[fn].append(text)
    elif len(lines) > 4:
        raise "ERROR: There should always be 4 lines"

def write_annotations_to_files():
    print(annotations_dict)
    for bd, annotations in annotations_dict.items():
        print("item")
        # Build filename of output files
        fn = bd.title + " - " + ", ".join(bd.authors) + ".md"

        with open(fn, 'w', encoding='utf-8') as f:
            content = ""

            # Write the book title in the first line
            content += "# " + bd.title + "\n\n"

            # After the title, just print all quotes with empty lines inbetween
            content += "\n\n".join(annotations)

            # last line is empty
            content += "\n"

            # Write the string to the file
            f.write(content)

if __name__ == "__main__":
    main()