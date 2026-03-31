import pandas as pd 
import html
import re
import os
import fasttext #assume you have it installed already
import regex as re
import string
from collections import Counter
from collections import defaultdict
import csv

# Name the csv file with combined comments you have
df = pd.read_csv('YOUR_COMMENTS.csv')

# Take a look at the content
df.info()

df.describe(include="all") # count unique comments and authors

# see how many comments in each video
unique_counts = df.groupby("video_id")["comment"].nunique()
print(unique_counts)

# --- CLEANING FUNCTION ---
def clean_comment(text):
    text = html.unescape(str(text))
    text = re.sub(r'<[^>]+>', ' ', text)      # remove HTML tags
    text = re.sub(r'@\w+', '', text)          # remove @mentions
    text = re.sub(r'\s+', ' ', text).strip()  # normalize whitespace
    return text

# --- APPLY CLEANING ---
df["comment"] = df["comment"].astype(str).apply(clean_comment)

# --- DROP EMPTY ---
df = df[df["comment"].str.strip().astype(bool)]

# --- DROP DUPLICATES ---
df = df.drop_duplicates(subset=["comment"], keep="first").reset_index(drop=True)

df.head()

df.to_csv("ALL_COMMENTS_CLEAN.csv", index=False, encoding="utf-8")

# check again to see how many valid items are left after cleaning
df.info()

# see how many comments in each video again
unique_counts = df.groupby("video_id")["comment"].nunique()
print(unique_counts)

import os
import pandas as pd
import html
import re

# --- SETTINGS ---
csv_path = "ALL_COMMENTS_CLEAN_copy.csv"          # path to your CSV
output_folder = "ALL_COMMENTS_filtered_txt_copy"    # folder to store .txt files
comment_column = "comment"                     # column with comments
title_column = "video_title"                   # column with video titles

# --- FUNCTION TO CLEAN HTML entities ---
def clean_comment(text):
    # 1. Decode HTML entities (&amp; → &, etc.)
    text = html.unescape(text)

    # 2. Remove ALL HTML tags: <br>, <i>, <b>, <div>, etc.
    text = re.sub(r'<[^>]+>', ' ', text)

    # 3. Remove @usernames
    text = re.sub(r'@\w+', '', text)

    # 4. Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# --- LOAD CSV ---
df = pd.read_csv(csv_path)

# Clean comments, must clean again because the CSV will not apply to the txt settings 
df[comment_column] = df[comment_column].astype(str).apply(clean_comment)

# Remove empty after cleaning
df = df[df[comment_column].str.strip().astype(bool)]

# Remove duplicates
df = df.drop_duplicates(subset=[comment_column], keep="first").reset_index(drop=True)

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# --- SAFE FILENAME CLEANER ---
def clean_filename(name):
    # Remove illegal filename characters
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    # Trim length to avoid OS limits
    return name[:150].strip()

# --- PROCESS EACH COMMENT ---
for idx, row in df.iterrows():
    cleaned_comment = row[comment_column]
    raw_title = str(row[title_column])

    # Clean title for safe filename
    safe_title = clean_filename(raw_title)

    # If multiple comments come from same video, avoid overwriting
    file_path = os.path.join(output_folder, f"{safe_title}_{idx+1}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(cleaned_comment)

print(f"Done! Saved {len(df)} cleaned, unique comments to: {output_folder}")

!pip install fasttext

# Load fastText model
model = fasttext.load_model("lid.176.bin")

# -----------------------------
# Script detection patterns
# -----------------------------
SCRIPTS = {
    "Cyrillic": r"\p{Cyrillic}",
    "Arabic": r"\p{Arabic}",
    "Han": r"\p{Han}",
    "Devanagari": r"\p{Devanagari}",
    "Hebrew": r"\p{Hebrew}",
    "Hangul": r"\p{Hangul}",
    "Thai": r"\p{Thai}",
}

def detect_script(text):
    for script, pattern in SCRIPTS.items():
        if re.search(pattern, text):
            return script
    return "Latin"

# -----------------------------
# Utility functions
# -----------------------------

def ascii_ratio(text):
    letters = sum(c in string.ascii_letters for c in text)
    return letters / max(len(text), 1)

def is_emoji_or_symbol(text):
    # No alphabetic characters at all
    return not re.search(r"[A-Za-z]", text)

def fasttext_predict(text):
    label, prob = model.predict(text)
    return label[0].replace("__label__", ""), prob[0]

# -----------------------------
# Language counting logic
# -----------------------------

def detect_language_clean(text):
    text = text.strip()
    if not text:
        return None

    # 1. Emoji-only or symbol-only → ignore
    if is_emoji_or_symbol(text):
        return None

    # 2. Very short lines (<6 chars) → treat as English
    if len(text) < 6:
        return "en"

    # 3. All ASCII and all-caps → English
    if text.isupper() and all(ord(c) < 128 for c in text):
        return "en"

    # 4. Script detection: non-Latin → use script as language
    script = detect_script(text)
    if script != "Latin":
        return script  # e.g., "Cyrillic", "Arabic", etc.

    # 5. fastText prediction
    lang, prob = fasttext_predict(text)

    # 6. Strong English threshold
    if lang == "en" and prob > 0.75:
        return "en"

    # 7. If fastText is confident it's non-English
    if lang != "en" and prob > 0.40:
        return lang

    # 8. ASCII-heavy fallback → English
    if ascii_ratio(text) > 0.75:
        return "en"

    # 9. Otherwise return fastText guess
    return lang

# -----------------------------
# Scan folder and count languages
# -----------------------------

folder = "ALL_COMMENTS_filtered_txt"
lang_counts = Counter()

for filename in os.listdir(folder):
    if filename.endswith(".txt"):
        with open(os.path.join(folder, filename), "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                lang = detect_language_clean(line)
                if lang:
                    lang_counts[lang] += 1

# -----------------------------
# Print results
# -----------------------------

print("Language counts (cleaned):")
for lang, count in lang_counts.most_common():
    print(f"{lang}: {count}")

# Get which texts are labeled as non-English

from collections import defaultdict

# Load fastText model
model = fasttext.load_model("lid.176.bin")
# -----------------------------
# Script detection patterns
# -----------------------------
SCRIPTS = {
    "Cyrillic": r"\p{Cyrillic}",
    "Arabic": r"\p{Arabic}",
    "Han": r"\p{Han}",
    "Devanagari": r"\p{Devanagari}",
    "Hebrew": r"\p{Hebrew}",
    "Hangul": r"\p{Hangul}",
    "Thai": r"\p{Thai}",
}

def detect_script(text):
    for script, pattern in SCRIPTS.items():
        if re.search(pattern, text):
            return script
    return "Latin"


# -----------------------------
# Utility functions
# -----------------------------

def ascii_ratio(text):
    letters = sum(c in string.ascii_letters for c in text)
    return letters / max(len(text), 1)

def is_emoji_or_symbol(text):
    return not re.search(r"[A-Za-z]", text)

def fasttext_predict(text):
    label, prob = model.predict(text)
    return label[0].replace("__label__", ""), prob[0]

# -----------------------------
# Clean language detection
# -----------------------------

def detect_language_clean(text):
    text = text.strip()
    if not text:
        return None

    # Emoji-only or symbol-only → ignore
    if is_emoji_or_symbol(text):
        return None

    # Very short lines (<6 chars) → English
    if len(text) < 6:
        return "en"

    # All ASCII and all-caps → English
    if text.isupper() and all(ord(c) < 128 for c in text):
        return "en"

    # Script detection
    script = detect_script(text)
    if script != "Latin":
        return script

    # fastText prediction
    lang, prob = fasttext_predict(text)

    # Strong English threshold
    if lang == "en" and prob > 0.75:
        return "en"

    # Confident non-English
    if lang != "en" and prob > 0.40:
        return lang

    # ASCII-heavy fallback
    if ascii_ratio(text) > 0.75:
        return "en"

    return lang

# -----------------------------
# Scan folder and map files → languages
# -----------------------------

folder = "ALL_COMMENTS_filtered_txt"

file_languages = defaultdict(set)

for filename in os.listdir(folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                lang = detect_language_clean(line)
                if lang and lang != "en":
                    file_languages[filename].add(lang)

# -----------------------------
# Print results
# -----------------------------

print("Files containing non-English content:\n")
for filename, langs in file_languages.items():
    print(f"{filename}")


import re

# Your pasted filenames according to the output above
raw_text = """



"""

# Split into lines, strip whitespace, keep only non-empty lines
files = [line.strip() for line in raw_text.split("\n") if line.strip()]

# Print Python-ready list
print("video_comment_files = [")
for f in files:
    print(f'    "{f}",')
print("]")


# copy-paste the new output below and manually check the auto-detected non-English comments in a csv file

# 🔧 Set your folder path here
folder = "ALL_COMMENTS_filtered_txt"

# 🔧 List of non-English files you identified, remove the last comma
non_english_files = [



  
]

# 🔧 Output CSV file
output_csv = "AUTO_DETECTED_NON-ENG_COMMENTS_copy.csv"

rows = []

for fname in non_english_files:
    fpath = os.path.join(folder, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().strip()
            rows.append([fname, text])
    else:
        rows.append([fname, "(file not found)"])

# Write to CSV
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["filename", "content"])
    writer.writerows(rows)

print(f"CSV created: {output_csv}")

# assume you know which txt files are wrongly detected after checking, now put them here to be deleted from the corpus

# 🔧 Put your folder path here
folder = "ALL_COMMENTS_filtered_txt"

# 🔥 Files you want to delete
files_to_delete = [
    "Title2.txt",
    "Tittle2.txt",
  "..."
]


for fname in files_to_delete:
    fpath = os.path.join(folder, fname)
    if os.path.exists(fpath):
        os.remove(fpath)
        print(f"Deleted: {fname}")
    else:
        print(f"Not found (skipped): {fname}")

print("\nDone.")

# check how many files remain

print("TXT files:", len(os.listdir("ALL_COMMENTS_filtered_txt")))
