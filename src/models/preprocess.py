"""
Creation: 2022/10/31
Author: https://github.com/smv7
Description: Script to preprocess train data for bg3dppd models."""


import argparse
import sys

from pathlib import Path

import srsly  # Serialization utilities of SpaCy's creators (https://github.com/explosion).
import spacy
from spacy.util import get_words_and_spaces  # To recover destructive tokenization that didn’t preserve whitespace info.
from spacy.tokens import Doc, DocBin


def main() -> None:
    # Configuring the CLI.
    parser = argparse.ArgumentParser(description="Build .spacy train data from format's compatible annotated data.")
    parser.add_argument('file2serialize', help='Annotated data to be serialized to .spacy file.')
    parser.add_argument('destination', default=Path(__file__).parent.joinpath('train.spacy'),
                        help='.spacy file destination.')
    parser.add_argument('-o', '--override', action='store_true', help='Override .spacy file if destination exists.')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    # Checking if the in/out files are founded and meet overriding constraints before proceed building the .spacy file.
    infile_exist = Path(args.file2serialize).is_file()
    outfile_exist = Path(args.destination).is_file()
    if infile_exist and (outfile_exist and args.override) or\
       infile_exist and not outfile_exist:
        # Initializing a blank spanish pipeline (multi-component model).
        nlp = spacy.blank("es")

        # Serializing the custom annotated data to be exported to a .spacy file.
        db = DocBin(attrs=['ENT_IOB', 'ENT_TYPE'])
        for sample in srsly.read_jsonl(Path(__file__).parent.joinpath(args.file2serialize)):
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
        db.to_disk(Path(__file__).parent.joinpath(args.destination))
    else:
        print(f"Path {args.file2serialize} must be a file to be serialized.") 
        sys.exit(1)

    return None


if __name__ == '__main__':
    main()
