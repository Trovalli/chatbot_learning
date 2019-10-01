import numpy as np
import re
import time

"""
Important notes from Matt:

Welcome to my chatbot. This is a preliminary testing ground for learning NLP.
I have no idea what I'm doing, so if you're reading this chances are the code is wrong.

My notes:

.split() returns a list with the split for each item, determined by split character

"""


lines = open('movie_lines.txt', encoding='utf-8', errors='ignore').read().split('\n')
keys = open('movie_conversations.txt', encoding='utf-8', errors='ignore').read().split('\n')

# Dictionary  to map each line to its ID
mapping = {}
for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line) == 5:
        mapping[_line[0]] = _line[4]


"""
Here's what's happening with the code below:
    First, iterating (for key in keys) takes each line the list (keys) and breaks it into a string
    For every key in our keys file, minus the last line (because it's empty), it's splitting the lines into a list.
    It then takes the last item ([-1]), a list which is keys for the dialogue, the only thing we need.
    Then it takes that list and pulls out the text raw text, and then replaces unnecessary characters.
    Finally, we then take _key and append it to our key_ids list, splitting by the , character
"""
key_ids = []
for key in keys[:-1]:
    _key = key.split(' +++$+++ ')[-1][1:-1].replace("'", "").replace(" ", "")
    key_ids.append(_key.split(','))

"""
We then need to separate the list of keys into questions, and answers.
So we take each item in key_ids, and iterate over our master list (keys). We subtract 1, because we start with key in key_ids (line 50).
On each iteration over the list, we create two lists. the first, is a question, the second, is an answer. Answer always follows question, so i + 1.
"""

questions = []
answers = []
for key in key_ids:
    for i in range(len(key) - 1):
        questions.append(mapping[key[i]])
        answers.append(mapping[key[i + 1]])

# We now have two lists. questions[x] aligns with answers[x]

print(questions[123])
print(answers[123])


