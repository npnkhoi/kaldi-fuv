import pandas as pd
from sklearn.metrics import confusion_matrix 
import seaborn as sns
import matplotlib.pyplot as plt

transcript_to_telex = pd.read_csv("TranscriptToName.csv")

def create_confusion_matrix(type):
    plt.figure(figsize = (11,10))
    with open(f"/home/cs398/kaldi/egs/kaldi-fuv/outputs/out_{type}.txt", "r") as f:
        results = f.readlines()
    prediction = []
    actual = []
    for result in results:
        try:
            act, pred = result.split()
        except:
            act = result.strip()
            pred = "sil"
        act = transcript_to_telex.loc[transcript_to_telex["filename"] == act.split("_")[3], "transcript"].iloc[0]
        actual.append(act)
        prediction.append(pred)
    cf_matrix = confusion_matrix(actual, prediction)

    ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues')

    ax.set_title(f'Confusion Matrix - {type.capitalize()} Model - {len(actual)} Words')
    ax.set_xlabel('Prediction')
    ax.set_ylabel('Actual')

    ## Ticket labels - List must be in alphabetical order
    tick_labels = transcript_to_telex.transcript.to_list()

    tick_labels.sort()
    ax.set_xticklabels(tick_labels, rotation=90)
    ax.set_yticklabels(tick_labels, rotation=90)


    ## Save the visualization of the Confusion Matrix.
    # plt.figure(figsize=(20,20))
    plt.savefig(f"confusion_matrix/{type}_confusion_matrix.png")
    plt.show()
    print(f"Save image at {type}_confusion_matrix.png")

# MONO
create_confusion_matrix("mono")
create_confusion_matrix("tri1")