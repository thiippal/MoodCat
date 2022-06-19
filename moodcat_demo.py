import spacy
import en_moodcat

nlp = spacy.load("en_moodcat")

doc = nlp("Does this work? I'm not sure.")

for sent in list(doc.spans['mood']):

    print(sent, sent.label_)