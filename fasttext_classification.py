from __future__ import unicode_literals
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from hazm import *
import fasttext
import string
import emoji
import hazm
import json
import os
import re
#
normalizer = Normalizer()

def remove_extra_chars(text):
    eng_alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',\
                     'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    eng_pattern = r'(?:{})'.format('|'.join([r"{}".format(ch) for ch in eng_alphabets]))

    with open("words_with_2_duplicate_letters.txt", encoding="utf-8") as text_file:
        certain_words = [line.strip() for line in text_file.readlines()]

    text = text.lower()
    # if url exists in the text
    url_pattern = r"(?:(?:https?):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"
    if re.findall(url_pattern, text, re.IGNORECASE):
        text = re.sub(url_pattern,"",text)


    if re.findall(r"@(\w+[.]*\b)", text):
        text = re.sub(r"@(\w+[.]*\b)","",text)

    # if number length is more than 3 numbers
    text = re.sub(r'\d{3,}', '', text)

    # remove english characters
    text = re.sub(eng_pattern, '', text)

    # if text contains @
    # text = re.sub(r'\s@\s', '', text)

    # if text contains extra character
    # remove all punctuation in fasttext or glove in ai_model
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    text = regex.sub(' ', text)

    text = unifing_alphabets(text)

    duplicate_letter_pattern = re.compile(r"(.)\1{2,}")
    text_with_pattern2 = duplicate_letter_pattern.sub(r"\1\1", text)
    differences2 = [word for word in text_with_pattern2.split(" ") if word not in text.split(" ")]
    if differences2:
        curse_pattern = r'\b(?:{})\b'.format('|'.join(certain_words))
        if re.findall(curse_pattern, " ".join(differences2)):
            text = text_with_pattern2
        else:
            text = duplicate_letter_pattern.sub(r"\1", text)


    text = (" ").join([word.strip() for word in text.split()])
    return text


def emoji_space(text):
    regex = re.compile(r'\d+(.*?)(?:\u263a|\U0001f645)')
    all_emoji = regex.findall(text)

    edited_text = []
    for c in text:
        if c in emoji.UNICODE_EMOJI:
            edited_text.append(" "+c+" ")
        else:
            edited_text.append(c)

    edited_text = ("").join(edited_text)
    return(edited_text)


def unifing_alphabets(text):
    text = re.sub(r'اَ|اِ|اُ|اٌ|اٍ|اً|أ|إ', 'ا', text)
    text = re.sub(r'بَ|بِ|بُ|بّ', 'ب', text)
    text = re.sub(r'پَ|پِ|پُ', 'پ', text)
    text = re.sub(r'تَ|تِ|تُ|تّ', 'ت', text)
    text = re.sub(r'ثَ|ثِ|ثُ', 'ث', text)
    text = re.sub(r'جَ|جِ|جُ|جّ', 'ج', text)
    text = re.sub(r'چَ|چِ|چُ|چّ', 'چ', text)
    text = re.sub(r'حَ|حِ|حُ', 'ح', text)
    text = re.sub(r'خَ|خِ|خُ', 'خ', text)
    text = re.sub(r'دَ|دِ|دُ|دّ', 'د', text)
    text = re.sub(r'ذَ|‌ذِ|ذُ', 'ذ', text)
    text = re.sub(r'رَ|رِ|رُ|رّ', 'ر', text)
    text = re.sub(r'زَ|زِ|زُ|زّ', 'ز', text)
    text = re.sub(r'ژَ|ژِ|ژُ', 'ژ', text)
    text = re.sub(r'سَ|سِ|سُ|سّ', 'س', text)
    text = re.sub(r'شَ|شِ|شُ', 'ش', text)
    text = re.sub(r'صَ|صِ|صُ', 'ص', text)
    text = re.sub(r'ضَ|ضِ|ضُ', 'ض', text)
    text = re.sub(r'طَ|طِ|طُ', 'ط', text)
    text = re.sub(r'ظَ|ظِ|ظُ', 'ظ', text)
    text = re.sub(r'عَ|عِ|عُ', 'ع', text)
    text = re.sub(r'غَ|غِ|غُ', 'غ', text)
    text = re.sub(r'فَ|فِ|فُ|فّ', 'ف', text)
    text = re.sub(r'قَ|قِ|قُ|قّ', 'ق', text)
    text = re.sub(r'کَ|کِ|کُ|ك|كَ|كِ|كُ|کّ|كّ', 'ک', text)
    text = re.sub(r'گَ|گِ|گُ', 'گ', text)
    text = re.sub(r'لَ|لِ|لُ|لّ', 'ل', text)
    text = re.sub(r'مَ|مِ|مُ', 'م', text)
    text = re.sub(r'نَ|نِ|نُ|نّ', 'ن', text)
    text = re.sub(r'وَ|وِ|وُ|ؤ|ؤَ|ؤُ|ؤِ|وّ|ؤّ', 'و', text)
    text = re.sub(r'هَ|هِ|هُ|ة', 'ه', text)
    text = re.sub(r'یَ|یِ|یُ|ي|يَ|يِ|يُ|يّ|یّ', 'ی', text)
    text = re.sub(r'ئَ|ئِ|ئُ|ئّ', 'ئ', text)
    return text



train_dataset_path ="social_train.txt"
test_dataset_path= "social_test.txt"


model = fasttext.train_supervised(train_dataset_path,
                                 dim=100,
                                 lr=0.9, #[0.1 - 1.0]
                                 loss="hs",
                                 wordNgrams=7, #[1 - 5]
                                 ws=3,
                                 epoch=100, #[5 - 50]
                                 minn=3,#3
                                 maxn=6,#6
                                 lrUpdateRate=10,
                                 neg=10,
                                 t=0.0001
                                 )


model.quantize(input=train_dataset_path,
               qnorm=True,
               retrain=True,
               epoch=1,
               cutoff=100000
               )


quantized_model_path = "social.ftz"
model.save_model(quantized_model_path)

print("test: ", model.test(test_dataset_path))

#number label
labels = set()
with open("social_test.txt", 'r') as f:
    for line in f:
        # print(line)
        labels.add(line.split(' ')[0])

print(labels,"test")


labels = set()
with open("social_train.txt", 'r') as f:
    for line in f:
        # print(line)
        labels.add(line.split(' ')[0])

print(labels,"train")


fasttext_model = fasttext.load_model("social.ftz")
count=0
y_pred=[]
y_true=[]
with open ('social_test.txt', 'r') as f :
    # print(f)
    for line in f:
        # print(y_true[line])
        # print(line)
        label = line.split(' ', maxsplit=1)[0].strip()

        y_true.append(label)

        sentence = line.split(' ', maxsplit=1)[1].strip()

        outputs = fasttext_model.predict(sentence)
      
        y_pred.append(outputs[0])




def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    #     classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


class_names = ['__label__47,', '__label__48,', '__label__49,', '__label__50,', '__label__51,', '__label__52,', '__label__53,', '__label__54,','__label__55,','__label__56,','__label__57,']

# Plot non-normalized confusion matrix
plot_confusion_matrix(y_true, y_pred, classes=class_names,
                      title='Confusion matrix, without normalization')

# Plot normalized confusion matrix
plot_confusion_matrix(y_true, y_pred, classes=class_names, normalize=True,
                      title='Normalized confusion matrix')

plt.show()
