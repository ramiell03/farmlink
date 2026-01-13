from app.core.trie import Trie

crop_trie = Trie()

INITIAL_CROPS = [
    "maize",
    "cocoa",
    "coffee",
    "plantain"
]

for crop in INITIAL_CROPS:
    crop_trie.insert(crop)
    