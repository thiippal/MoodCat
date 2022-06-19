import spacy

from functools import partial
from pathlib import Path
from typing import Iterable, Optional, Callable, cast
from spacy.util import registry
from spacy.tokens import Doc, DocBin, Span
from spacy.training import Example
from spacy.compat import Protocol, runtime_checkable

from thinc.api import get_current_ops, Ops
from thinc.types import Ragged, Ints1d


@runtime_checkable
class Suggester(Protocol):
    def __call__(self, docs: Iterable[Doc], *, ops: Optional[Ops] = None) -> Ragged:

        ...


@registry.misc("spacy.sent.suggester.v1")
def build_sent_suggester():

    def sent_suggester(docs: Iterable[Doc], *, ops: Optional[Ops] = None) -> Ragged:

        if ops is None:
            ops = get_current_ops()

        sents = []
        lengths = []

        for doc in docs:

            starts = []
            ends = []

            for sent in doc.sents:

                starts.append(sent.start)
                ends.append(sent.end)

            starts = ops.xp.array(starts, dtype="i").reshape((-1, 1))
            ends = ops.xp.array(ends, dtype="i").reshape((-1, 1))

            sents.append(ops.xp.hstack((starts, ends)))

            lengths.append(sents[-1].shape[0])

        lengths_array = cast(Ints1d, ops.asarray(lengths, dtype="i"))

        if len(sents) > 0:

            output = Ragged(ops.xp.vstack(sents), lengths_array)

        else:

            output = Ragged(ops.xp.zeros((0, 0), dtype="i"), lengths_array)

        assert output.dataXd.ndim == 2

        return output

    return sent_suggester


@spacy.registry.readers("SentenceMoodCorpus.v1")
def create_reader(file: Path) -> Callable[["Language"], Iterable[Example]]:

    return partial(read_files, file)


def read_files(file: Path, nlp: "Language") -> Iterable[Example]:

    doc_bin = DocBin().from_disk(file)
    docs = doc_bin.get_docs(nlp.vocab)

    for gold in docs:

        pred = Doc(
            nlp.vocab,
            words=[t.text for t in gold],
            spaces=[t.whitespace_ for t in gold],
            sent_starts=[t.is_sent_start for t in gold]
            )

        pred.spans['mood'] = [Span(gold, gspan.start, gspan.end, label=nlp.vocab[gspan.label].text)
                              for gspan in gold.spans['mood']]

        yield Example(pred, gold)
