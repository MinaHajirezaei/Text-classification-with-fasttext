import csv
import pandas as pd
import fasttext
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import json
# train_dataset_path = "Train_fastai_3labels.txt"
# test_dataset_path = "Test_fastai_3labels.txt"
# print(test_dataset_path)


fasttext_model = fasttext.load_model("sosial.ftz")
count=0
y_pred=[]
y_true=[]
with open ('social_test.txt', 'r') as f :
    # print(f)
    for line in f:
        # print(y_true[line])
        # print(line)
        label = line.split(' ', maxsplit=1)[0].strip()
        print(label)
        y_true.append(label)
        # print(y_true)
        sentence = line.split(' ', maxsplit=1)[1].strip()
        # print(sentence)
        start_time = datetime.now()

        outputs = fasttext_model.predict(sentence)
        print(outputs[0])
        y_pred.append(outputs[0])
        # print(y_pred)

#         if label!= outputs:
#             # print("ffffff")
#             count += 1
#             print(count)
#             with open('predict1.csv', 'a+') as f:
#                 writer = csv.writer(f)
#                 writer.writerow([sentence, label, outputs])
#
#
#
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

# #artmedia
# class_names = ['__label__35,', '__label__27,', '__label__25,', '__label__6,']
#sports
# class_names = ['__label__40,', '__label__24,', '__label__32,', '__label__13,', '__label__2,', '__label__14,', '__label__43,', '__label__39,']
#economy
# class_names = ['__label__8,', '__label__37,', '__label__41,', '__label__3,', '__label__10,', '__label__5,', '__label__28,', '__label__12,', '__label__1,', '__label__7,', '__label__23,']
#politics
# class_names = ['__label__30,', '__label__45,', '__label__0,', '__label__44,', '__label__16,', '__label__33,']
#culture
# class_names = ['__label__26,', '__label__18,', '__label__34,', '__label__29,', '__label__4,', '__label__38,', '__label__15,', '__label__17,']
#social
class_names = ['__label__54,', '__label__56,', '__label__47,', '__label__55,', '__label__50,', '__label__57,', '__label__53,', '__label__48,', '__label__51,', '__label__49,', '__label__52,']

# Plot non-normalized confusion matrix
plot_confusion_matrix(y_true, y_pred, classes=class_names,
                      title='Confusion matrix, without normalization social')

# Plot normalized confusion matrix
plot_confusion_matrix(y_true, y_pred, classes=class_names, normalize=True,
                      title='Normalized confusion matrix social')

plt.show()




# y_pred = list_pred
# print(len(list_pred))
# print(len(y_true))
# from sklearn.metrics import confusion_matrix
# y_pred = list_pred
# print(confusion_matrix(y_true, y_pred, labels=["__label__0,", "__label__1,", "__label__2,"]))













