import pandas as pd


current_book = ""
current_chapter = ""
current_verse = ""
verses_list = []
line_stack = []

with open("bom.txt", "rt") as bom:
    bom_text = bom.readlines()

for line in bom_text:
    line = line.strip()

    if "Chapter 1" in line and line[-2:] == " 1":
        current_book = line.split("Chapter")[0]
        current_chapter = "1"

    elif "Chapter" in line:
        current_chapter = line.split(" ")[-1]

    elif len(line) > 0 and line[0].isnumeric() and len(line.split(":")) > 1:

        if len(line_stack) > 0:
            verses_list.append((current_book, current_chapter, current_verse, " ".join(line_stack).strip()))

        verse_num_and_text = line.split(":")[1].split(" ")
        current_verse = verse_num_and_text[0]
        line_stack = [" ".join(verse_num_and_text[1:])]

    elif len(line_stack) > 0:
        line_stack.append(line)


data = {
    'Book': [],
    'Chapter': [],
    'Verse': [],
    'Text': []
}

for book, chapter, verse, text in verses_list:
    data['Book'].append(book)
    data['Chapter'].append(chapter)
    data['Verse'].append(verse)
    data['Text'].append(text)

df = pd.DataFrame(data)

df.set_index(['Book', 'Chapter', 'Verse'], inplace=True)

print(df.head())
