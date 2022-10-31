"""
Creation: 2022/10/31
Author: https://github.com/smv7
Description: Script to preprocess train data for bg3dppd models."""


from pathlib import Path

import srsly  # Serialization utilities of SpaCy's creators (https://github.com/explosion).
import spacy
from spacy.util import get_words_and_spaces  # To recover destructive tokenization that didn’t preserve whitespace info.
from spacy.tokens import Doc, DocBin


def main():
    # Initializing a blank spanish pipeline (multi-component model).
    nlp = spacy.blank("es")

    # Serializing the custom annotated data to be exported to a .spacy file.
    db = DocBin(attrs=['ENT_IOB', 'ENT_TYPE'])
    for sample in srsly.read_jsonl(Path(__file__).parent.joinpath('data/translated_01.jsonl')):
        # Reconstructing whitespace information from the tokens.
        tokens = [token['text'] for token in sample['tokens']]
        words, spaces = get_words_and_spaces(tokens, sample['text'])
        doc = Doc(nlp.vocab, words, spaces)

        # Packing the entity's information from the spans.
        doc.ents = [
            doc.char_span(span['start'], span['end'], span['label'])
            for span in sample['spans']]

        db.add(doc)  # Adding the doc to be serialized.

    # Saving the serialized samples to the .spacy file.
    db.to_disk(Path(__file__).parent.joinpath("data/train.spacy"))


if __name__ == '__main__':
    main()
