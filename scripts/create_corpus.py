"""Convert CoNNL-U annotations into .spacy format"""
import conllu
import typer
import numpy as np
from pathlib import Path

import spacy
from spacy.tokens import Span, Doc, DocBin

np.random.seed(32)

nlp = spacy.load('en_core_web_sm')


def create_corpus(in_path: Path):

    annotations = [conllu.parse(f.read_text(encoding='utf-8')) for f in in_path.glob('*.conllu')]

    docs = []

    for ann in annotations:

        moods = []
        words = []
        spaces = []
        sent_starts = []

        for sent in ann:

            is_start = True

            moods.append(sent.metadata['s_type'])

            for token in sent:

                words.append(token['form'])

                sent_starts.append(True if is_start else False)
                is_start = False

                if token['misc'] is not None and 'SpaceAfter' in token['misc']:

                    if token['misc']['SpaceAfter'] == 'No':
                        spaces.append(False)

                else:

                    spaces.append(True)

        doc = Doc(vocab=nlp.vocab,
                  words=words,
                  spaces=spaces,
                  sent_starts=sent_starts)

        sentences = []

        for sent, mood in zip(doc.sents, moods):
            sent = Span(doc, sent.start, sent.end, label=mood)

            sentences.append(sent)

        doc.spans['mood'] = sentences

        docs.append(doc)

    dev = np.random.choice(len(docs), 10, replace=False)
    dev = [docs[x] for x in dev]

    train = [x for x in docs if x not in dev]

    train = DocBin(docs=train, store_user_data=True)
    dev = DocBin(docs=dev, store_user_data=True)

    train.to_disk('corpus/train.spacy')
    dev.to_disk('corpus/dev.spacy')


if __name__ == "__main__":
    typer.run(create_corpus)
