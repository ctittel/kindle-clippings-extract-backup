import os
import re
import json
from pathlib import Path

matcher = re.compile(r'^(.*) +\((.*)\)$')
annotations_dict = {}

json_files_dir = Path("./json")
notes_files_dir = Path("./output")

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

    # create used directories if they don't exist
    json_files_dir.mkdir(exist_ok=True)
    notes_files_dir.mkdir(exist_ok=True)

    annotations = s.split("\n==========\n")
    for a in annotations:
        add_annotation_to_dict(a)

    update_json_files()
    write_notes_files()

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

def make_json_file_path(bd: BookData):
    return Path(json_files_dir, bd.title + " - " + ", ".join(bd.authors) + ".json")

def make_note_file_path(bd: BookData):
    return Path(notes_files_dir, bd.title + " - " + ", ".join(bd.authors) + ".md")

def update_json_files():
    """ Create json files for each book if it not exists.
        Otherwise merge the new stuff into the existing json file"""

    for bd in annotations_dict:
        fp = make_json_file_path(bd)
        notes = []
        if fp.exists():
            with fp.open(mode="r") as f:
                notes = json.loads(f.read())['notes']
        notes_set = set(notes)
        for nn in annotations_dict[bd]:
            if nn not in notes_set:
                notes.append(nn)
        annotations_dict[bd] = notes
        with fp.open(mode="w+") as f:
            f.write(json.dumps({'notes':notes}))

def write_notes_files():
    for bd, annotations in annotations_dict.items():
        with open(make_note_file_path(bd), 'w', encoding='utf-8') as f:
            content = ""

            # Write the book title in the first line
            content += "# " + bd.title

            # Write author in the second line
            content += "\n*by " + ' and '.join(bd.authors) + "*" + "\n\n"

            # After the title, just print all quotes with empty lines inbetween
            content += "\n\n".join(annotations)

            # last line is empty
            content += "\n"

            # Write the string to the file
            f.write(content)

if __name__ == "__main__":
    main()