import pandas as pd
from sklearn.metrics import confusion_matrix 
import seaborn as sns
import matplotlib.pyplot as plt

transcript_to_telex = pd.read_csv("TranscriptToName.csv")

def create_confusion_matrix(type):
    with open(f"/home/cs398/kaldi/egs/kaldi-fuv/outputs/out_{type}.txt", "r") as f:
        results = f.readlines()
    prediction = []
    actual = []
    for result in results:
        try:
            act, pred = result.split()
        except:
            act = result.strip()
            pred = ""
        act = transcript_to_telex.loc[transcript_to_telex["filename"] == act.split("_")[2], "transcript"].iloc[0]
        actual.append(act)
        prediction.append(pred)

    cf_matrix = confusion_matrix(actual, prediction)

    ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues')

    ax.set_title(f'{type.capitalize()} Confusion Matrix')
    ax.set_xlabel('Prediction')
    ax.set_ylabel('Actual')

    ## Ticket labels - List must be in alphabetical order
    tick_labels = transcript_to_telex.transcript.to_list()
    tick_labels.sort()
    ax.set_xticklabels(tick_labels, rotation=90)
    ax.set_yticklabels(tick_labels, rotation=90)

    ## Save the visualization of the Confusion Matrix.
    # plt.figure(figsize=(20,20))
    plt.savefig(f"{type}_confusion_matrix.png")
    print("Save image")

# MONO
create_confusion_matrix("mono")
create_confusion_matrix("tri1")