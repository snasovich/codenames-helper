import logging

from clue import Clue
from thresholds import Thresholds

stop_words = ['.', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

def word_similarities(word_vectors, clue, words):
    return sorted([(word, word_vectors.similarity(clue, word)) for word in words], key=lambda item: item[1], reverse=True)

def find_clues(word_vectors, board_words) -> list[Clue]:
    thresholds = Thresholds()
    potential_clues = {}

    # Combine all words to be excluded into a set for faster checking
    all_excluded_words = set(board_words["spymaster"] + board_words["opponent"] + board_words["neutral"] + board_words["assassin"] + stop_words)

    for word in board_words["spymaster"]:
        # Get enough similar words to include all matches up to requested threshold
        current_max = 100
        similar_words = word_vectors.similar_by_word(word, current_max)
        while (similar_words[-1][1] > thresholds.scoring_target_word_similarity):
            logging.debug(f"Last (of {current_max}) similar word's similarity {similar_words[-1][1]} is over threshold {thresholds.scoring_target_word_similarity}), requesting 10x")
            current_max *= 10
            similar_words = word_vectors.similar_by_word(word, current_max)

        # Iterate through matches and add to matches dict
        for similar_word, similarity in similar_words:
            if similarity < thresholds.scoring_target_word_similarity:
                # as soon as we hit first match lower than threshold it's safe to break as scores are ordered
                break

            if similar_word in all_excluded_words:
                continue

            potential_clues.setdefault(similar_word, []).append((word, similarity))
 
    # Build list of `Clue` objects from the initial dict
    clues_list = []
    for clue, similarities_list in potential_clues.items():
        # Sort similarities for better display
        if len(similarities_list) > 1:
            similarities_list.sort(key=lambda item: item[1], reverse=True)

        target_own_words = [word_pair[0] for word_pair in similarities_list]
        other_own_words = [own_word for own_word in board_words["spymaster"] if own_word not in target_own_words]

        clues_list.append(Clue(
            clue=clue,
            target_words_scores=similarities_list,
            other_own_words_scores=word_similarities(word_vectors, clue, other_own_words),
            assassin_scores=word_similarities(word_vectors, clue, board_words["assassin"]),
            opponent_scores=word_similarities(word_vectors, clue, board_words["opponent"]),
            neutral_scores=word_similarities(word_vectors, clue, board_words["neutral"]),
            thresholds=thresholds
        ))

    return clues_list