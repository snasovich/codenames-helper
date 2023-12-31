import print_utils
import logging
import user_interactions

from gensim.downloader import load

from clue import Clue
from clue_finder import find_clues
from thresholds import Thresholds


model_name = "glove-wiki-gigaword-50"
# model_name = "glove-wiki-gigaword-300"

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

board_words = user_interactions.select_board_words()
if board_words == None:
    print("No board words specified, exiting!")
    exit()

logging.info(f"Finding clues for specified board words: {board_words}")
clues = find_clues(word_vectors, board_words)
logging.info(f"Clues found (total: {len(clues)})")

page_size = 10
# clues.sort(key=lambda item: (len(item.target_words_scores), sum([e[1] for e in item.target_words_scores]) / len(item.target_words_scores)), reverse=True)
clues.sort(key=lambda item: item.total_score, reverse=True)
print(f"Top {page_size} clues (ordered by total score)")
for clue in clues[:10]:
    print_utils.print_clue_details(clue)