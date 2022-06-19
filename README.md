<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# MoodCat 😼 (Sentence Mood Classifier for English)

This repository shows how to train a sentence [mood](https://en.wikipedia.org/wiki/Grammatical_mood) classifier using spaCy's new [SpanCategorizer](https://spacy.io/api/spancategorizer) component and the [Georgetown University Multilayer (GUM) Corpus](https://github.com/amir-zeldes/gum). The classifier uses a [custom span suggester](scripts/sent_suggester.py), which returns sentences for classification.

Please note that this repository is only for demonstration. The GUM corpus is too small for training a classifier from scratch and some labels are very rare. The classifier does a decent job with declaratives and interrogatives, but struggles with imperatives and rarer moods.

For information on classifier performance, see the file [`training/metrics.json`](training/metrics.json).

## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[spaCy projects documentation](https://spacy.io/usage/projects).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `convert` | Convert the CoNLL-U data to spaCy's binary format |
| `debug` | Debug the data for insights on the corpus |
| `train` | Train the model for sentence mood classification |
| `evaluate` | Evaluate the model and export metrics |
| `package` | Package the trained model as a pip package |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `convert` &rarr; `train` &rarr; `evaluate` &rarr; `package` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/gum` | Git | The Georgetown University Multilayer (GUM) Corpus |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->

### 🤔 How to run the demo?

1. Run the command `python setup.py install` in the directory `packages/en_moodcat-0.0.1` to install the pipeline
2. Run the file `moodcat_demo.py`