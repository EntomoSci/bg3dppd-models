"""
Creation: 2022/10/19
Author: https://github.com/smv7
Description: Tools to build annotated train sets for bg3dppd models."""


import os
from pathlib import Path
from typing import NewType
import json

import spacy
from spacy.tokens import DocBin


TRAINSET_SAMPLES_PATH = Path(__file__).parent.joinpath('samples.json')
TRAINSET_PATH = Path(__file__).parent.joinpath('train.spacy')
CATEGORIES = ('TYPE', 'PRICE', 'MATERIAL', 'BOARDGAME')

WordIndexPair = NewType('WordIndexPair', tuple[int, int])
Annotation = NewType('Annotation', tuple[int, int, str])
AnnotatedEntry = NewType('AnnotatedEntry', tuple[str, list[Annotation]])


def load_raw_samples() -> list[str]:
    """
    Return 49 samples of Instagram's post descriptions about 3D printed boardgame products."""

    with Path(__file__).parents[2].joinpath('data/text_samples.txt').open('rt', encoding='utf-8') as f:
        return f.readlines()


def get_word_indices(text: str, words: str | list[str]) -> WordIndexPair | list[WordIndexPair]:
    """
    Return start/end char index of `words` in `text`."""

    indx_pairs: list[WordIndexPair] = []

    if isinstance(words, str):
        st = text.index(words)
        end = st + len(words)
        return st, end
        # match_ = re.search(words, text)
        # if match_ is not None:
        #     indx_pair: WordIndexPair = match_.span()
        #     return match_.span()
    elif isinstance(words, list):
        for word in words:
            st = text.index(word)
            end = st + len(word)
            indx_pairs.append((st, end))

            # match_ = re.search(word, text)
            # if match_ is not None:
            #     indx_pair: WordIndexPair = match_.span()
            #     indx_pairs.append(indx_pair)

    return indx_pairs


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

    return None


def get_training_data_interactively() -> list[AnnotatedEntry]:
    """
    Return interactively annotated training data."""

    clear()

    # Loading the text samples to begin building the annotated training set.
    samples: list[str] = load_raw_samples()
    training_data: list[AnnotatedEntry] = []
    for i, sample in enumerate(samples):

        # Prompting the user to identify the categories of the current sample.
        print(f'#{i+1} sample: {sample}')
        type: str = input('Type: ')
        price: str = input('Price: ')
        material: str = input('Material: ')
        boardgame: str = input('Boardgame: ')

        # Calculating the indices of the categories passed by the user founded in the current sample and saving the
        # sample and its category indices as a entry for the annotated training data.
        annotations: list[Annotation] = []
        for category, label in zip((type, price, material, boardgame), CATEGORIES):
            if category != '':
                annotation: Annotation = (*get_word_indices(sample, category), label)
                annotations.append(annotation)

        entry: AnnotatedEntry = (sample, annotations)
        training_data.append(entry)

        # Cleaning the terminal and going to the next sample.
        clear()

    return training_data


def build_annotated_trainset() -> None:
    """
    Build annotated training set using a set of samples."""

    with TRAINSET_SAMPLES_PATH.open('rt') as f:
        samples: dict[AnnotatedEntry] = json.load(f)
        
    return None


def save_training_data(training_data: list[AnnotatedEntry]) -> None:
    """
    Store `training_data` using the spaCy recommended mechanisms."""

    # Setting the required spaCy objects.
    nlp = spacy.blank('es')

    # The DocBin will store the example documents.
    db = DocBin()

    # Converting the training data objects into spaCy entities and saving it to .spacy file.
    for text, annotations in training_data:
        doc = nlp(text)
        ents = []
        for start, end, label in annotations:
            span = doc.char_span(start, end, label=label)
            ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(TRAINSET_PATH)

    return None


def main() -> None:
    training_data: list[AnnotatedEntry] = get_training_data_interactively()
    save_training_data(training_data)

    return None


if __name__ == '__main__':
    main()

    # with TRAINSET_PATH.open('rt') as f:
    #     data = json.load(f)
    #     print(type(data), data)

    # text: str = 'This orange is delicious like programming in python!'
    # words: list[str] = ['orange', 'python', 'letuse', 'programming']
    # indxs: list[WordIndexPair] = get_word_indices(text, words)
    # print(text, words, sep='\n')
    # for st, end in indxs:
    #     print(f'{st}-{end}: "{text[st:end]}"')