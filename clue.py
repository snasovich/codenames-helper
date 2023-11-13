from typing import Optional
from thresholds import Thresholds

scoring_weights = {
    'target_words_weight': 3,        # How much weight to give to target own words
    'other_own_weight': 1,           # How much weight to give to other own words
    'assassin_weight': 7,            # How much weight to give to the assassin's similarity score
    'opponent_weight': 3,            # How much weight to give to each opponent word's similarity score
    'neutral_weight': 1,             # How much weight to give to each neutral word's similarity score
}

class Clue:
    def __init__(self, clue: str,
                 target_words_scores: list[tuple[str, float]],
                 other_own_words_scores: list[tuple[str, float]],
                 assassin_scores: list[tuple[str, float]],
                 opponent_scores: list[tuple[str, float]],
                 neutral_scores: list[tuple[str, float]],
                 thresholds: Thresholds):
        self.clue = clue  # The clue word
        self.target_words_scores = target_words_scores  # Scores of target words associated with this clue
        self.other_own_words_scores = other_own_words_scores # Scores of other own words associated with this clue
        self.assassin_scores = assassin_scores  # The similarity score to the assassin word
        self.opponent_scores = opponent_scores  # Scores of opponent words associated with this clue
        self.neutral_scores = neutral_scores  # Scores of neutral words associated with this clue
        self.thresholds = thresholds
        self.total_score = self.calculate_score(False)  # The final calculated score for the clue

    def calculate_score(self, print_calc_details: Optional[bool] = False):
        score = sum(similarity for _, similarity in self.target_words_scores) * scoring_weights['target_words_weight']
        initial_score = score

        other_own_words_adjustment = sum(scoring_weights['other_own_weight'] * similarity for _, similarity in self.other_own_words_scores if similarity > self.thresholds.scoring_other_own_word_positive_similarity)
        score += other_own_words_adjustment

        assasin_words_adjustment = sum(scoring_weights['assassin_weight'] * similarity for _, similarity in self.assassin_scores if similarity > self.thresholds.scoring_assassin_risk_similarity)
        score -= assasin_words_adjustment

        opponent_words_adjustment = sum(scoring_weights['opponent_weight'] * similarity for _, similarity in self.opponent_scores if similarity > self.thresholds.scoring_opponent_word_negative_similarity)
        score -= opponent_words_adjustment

        neutral_words_adjustment = sum(scoring_weights['neutral_weight'] * similarity for _, similarity in self.neutral_scores if similarity > self.thresholds.scoring_neutral_word_negative_similarity)
        score -= neutral_words_adjustment

        if print_calc_details:
            print(f"Score for clue: {self.clue} = {score}")
            print("\tCalculation steps:")
            print(f"\tScore of target words: {initial_score} (sum of all similarities with {scoring_weights['target_words_weight']}x weight)")
            print(f"\tPlus other own word similarity score - {other_own_words_adjustment} (counting scores over {self.thresholds.scoring_other_own_word_positive_similarity} with {scoring_weights['other_own_weight']}x) weight")
            print(f"\tLess assassin word similarity score - {assasin_words_adjustment} (counting scores over {self.thresholds.scoring_assassin_risk_similarity} with {scoring_weights['assassin_weight']}x) weight")
            print(f"\tLess opponent word similarity score - {opponent_words_adjustment} (counting scores over {self.thresholds.scoring_opponent_word_negative_similarity} with {scoring_weights['opponent_weight']}x) weight")
            print(f"\tLess neutral word similarity score - {neutral_words_adjustment} (counting scores over {self.thresholds.scoring_neutral_word_negative_similarity} with {scoring_weights['neutral_weight']}x) weight")

        return score

    def __repr__(self):
        return f"Clue({self.clue}, score={self.total_score})"