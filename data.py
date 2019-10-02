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
So we take each item in key_ids, and iterate over our master list (keys). 
We subtract 1, because we start with key in key_ids (line 50).
On each iteration over the list, we create two lists. the first, is a question, the second, is an answer. 
Answer always follows question, so i + 1.
"""

questions = []
answers = []
for key in key_ids:
    for i in range(len(key) - 1):
        questions.append(mapping[key[i]])
        answers.append(mapping[key[i + 1]])

"""
We now have two lists. questions[x] aligns with answers[x].
The next step is to clean the data, removing apostrophes, changing words and making everything lowercase.
"""

# Heck of a function, but all it does is re.sub() all of the text to make it more simple for the bot to learn from.
def clean(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"wouldn't", "would not", text)
    text = re.sub(r"shouldn't", "should not", text)
    text = re.sub(r"couldn't", "could not", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"isn't", "is not", text)
    text = re.sub(r"didn't", "did not", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"[-()\"@#/:;<>{}+=~|.?,]", "", text)
    text = re.sub(r"  ", " ", text)
    return text


# Clean the questions
clean_questions = []
for question in questions:
    clean_questions.append(clean(question))

# Clean the answers
clean_answers = []
for answer in answers:
    clean_answers.append(clean(answer))

"""
Next, we will remove the non-important words
Note: I will come back and play with this. May be worth it in the long run to not do this.
We do this to optimize training, but what if I had forever to train? Or a super powerful PC? 
Would it make the bot smarter?

Regardless, we will choose a dictionary to do this, called word_count.

For each question in our now cleaned list, we split each word into a list. If that word appears in word_count, 
we add 1 to it. if not, we set it equal to 1.
"""
word_count = {}
for question in clean_questions:
    for word in question.split(' '):
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1

for answer in clean_answers:
    for word in answer.split(' '):
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1

"""
Next:
Tokenization and filtering the non frequent words. Both are key in NLP.
Threshold is a hyperparameter
"""

threshold = 20
questions_words_ints = {}
word_number = 0
for word, count in word_count.items():
    if count >= threshold:
        questions_words_ints[word] = word_number
        word_number += 1

answers_words_ints = {}
word_number = 0
for word, count in word_count.items():
    if count >= threshold:
        answers_words_ints[word] = word_number
        word_number += 1


# Adding the last tokens to these two dictionaries
tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']
for token in tokens:
    questions_words_ints[token] = len(questions_words_ints) + 1
for token in tokens:
    answers_words_ints[token] = len(answers_words_ints) + 1

# Create the inverse dictionary of answers_words_ints
answersint2word = {w_i: w for w, w_i in answers_words_ints.items()}
for i in range(len(clean_answers)):
    clean_answers[i] += " <EOS>"

# Translate all questions and answers into integers
# and replace all words filtered out with <OUT>

questions_to_int = []
answers_to_int = []
for question in clean_questions:
    ints = []
    for word in question.split():
        if word not in questions_words_ints:
            ints.append(questions_words_ints['<OUT>'])
        else:
            ints.append(questions_words_ints[word])
    questions_to_int.append(ints)

for answer in clean_answers:
    ints = []
    for word in answer.split():
        if word not in answers_words_ints:
            ints.append(answers_words_ints['<OUT>'])
        else:
            ints.append(answers_words_ints[word])
    answers_to_int.append(ints)

# Sort the questions and answers by length of question to help the training
sorted_clean_questions = []
sorted_clean_answers = []

for length in range(1, 25 + 1):
    for i in enumerate(questions_to_int):
        if len(i[1]) == length:
            sorted_clean_questions.append(questions_to_int[i[0]])
            sorted_clean_answers.append(answers_to_int[i[0]])

### END DATA PRE PROCESSING ###
