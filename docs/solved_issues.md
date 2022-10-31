# Project's Solved Issues

Creation: 2022/10/31\
Author: https://github.com/smv7

Problem:\
`ValueError: [E1010] Unable to set entity information for token n which is included in more than one span in entities,
blocked, missing or outside. error.`

Solution:\
Remove token's labeling overlapping (same token with different labels) from the annotated data user to build
the `.spacy` file.

---

