import pandas as pd
from tqdm import tqdm
import spacy

tqdm.pandas(desc="Processing")
nlp = spacy.load('en_core_web_sm')


def extract_features(text):
    doc = nlp(text)
    keywords = [chunk.text for chunk in doc.noun_chunks]
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return keywords, entities


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
        current_book = line.split("Chapter")[0].strip()
        current_chapter = "1"

    elif "Chapter" in line:
        if len(line_stack) > 0:
            verses_list.append((current_book, current_chapter, current_verse, " ".join(line_stack).strip()))

        current_chapter = line.split(" ")[-1].strip()
        line_stack = []

    elif len(line) > 0 and line[0].isnumeric() and len(line.split(":")) > 1:

        if len(line_stack) > 0:
            verses_list.append((current_book, current_chapter, current_verse, " ".join(line_stack).strip()))

        verse_num_and_text = line.split(":")[1].split(" ")
        current_verse = verse_num_and_text[0].strip()
        line_stack = [" ".join(verse_num_and_text[1:]).strip()]

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
df.sort_index(inplace=True)


df['Keywords'], df['Entities'] = zip(*df['Text'].progress_apply(extract_features))
df = df.reset_index()
df.set_index(['Book', 'Chapter', 'Verse', 'Keywords', 'Entities'], inplace=True)
df.sort_index(inplace=True)


print(df.loc[('1 Nephi', '1')])
