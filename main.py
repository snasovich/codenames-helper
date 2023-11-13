import print_utils
import logging

from gensim.downloader import load

from clue import Clue
from clue_finder import find_clues
from thresholds import Thresholds

model_name = "glove-wiki-gigaword-50"
# model_name = "glove-wiki-gigaword-300"

board_words = {
    "spymaster": ["shadow", "ice", "trip", "scale", "ground", "snowman", "bermuda", "paste", "bed"],
    "opponent": ["moscow", "saturn", "row", "disease", "face", "crane", "van", "buffalo"],
    "neutral": ["hole", "sound", "duck", "board", "press", "part", "rome"],
    "assassin": ["kid"]
}
# board_words = {
#     'spymaster': ['platypus', 'green', 'crash', 'sub', 'ray', 'plane', 'row', 'jupiter', 'mint'],
#     'opponent': ['block', 'india', 'embassy', 'sock', 'scale', 'round', 'phoenix', 'night'],
#     'neutral': ['canada', 'whale', 'pool', 'jam', 'center', 'undertaker', 'ninja'],
#     'assassin': ['rose']
# }

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', mode='w'),  # File handler for DEBUG level
        logging.StreamHandler()  # Stream handler for console output
    ]
)
# Set the level for the console handler to WARN
logging.getLogger().handlers[1].setLevel(logging.INFO)

thresholds = Thresholds()
thresholds.initialize_thresholds(model_name)

#load model
logging.info(f"Loading model '{model_name}'")
word_vectors = load(model_name)
logging.info("Model loaded!")

logging.info("Finding clues for specified board words...")
clues = find_clues(word_vectors, board_words)
logging.info(f"Clues found (total: {len(clues)})")

page_size = 10
# clues.sort(key=lambda item: (len(item.target_words_scores), sum([e[1] for e in item.target_words_scores]) / len(item.target_words_scores)), reverse=True)
clues.sort(key=lambda item: item.total_score, reverse=True)
print(f"Top {page_size} clues (ordered by total score)")
for clue in clues[:10]:
    print_utils.print_clue_details(clue)