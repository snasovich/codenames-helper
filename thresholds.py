import logging

class Thresholds:
    _instance = None

    _model_thresholds_mapping = {
        "glove-wiki-gigaword-50": {
            "scoring_target_word_similarity": 0.5,
            "scoring_other_own_word_positive_similarity": 0.33,
            "scoring_opponent_word_negative_similarity": 0.33,
            "scoring_neutral_word_negative_similarity": 0.33,
            "scoring_assassin_risk_similarity": 0.15,

            "display_great_similarity": 0.6,
            "display_good_similarity": 0.5,
            "display_ok_similarity": 0.33,
            "display_meh_similarity": 0.2,
            "display_assassin_safe_similarity": 0.1,
            "display_assassin_danger_similarity": 0.25
        },
       "glove-wiki-gigaword-300": {
            "scoring_target_word_similarity": 0.4,
            "scoring_other_own_word_positive_similarity": 0.25,
            "scoring_opponent_word_negative_similarity": 0.25,
            "scoring_neutral_word_negative_similarity": 0.25,
            "scoring_assassin_risk_similarity": 0.1,

            "display_great_similarity": 0.5,
            "display_good_similarity": 0.4,
            "display_ok_similarity": 0.3,
            "display_meh_similarity": 0.2,
            "display_assassin_safe_similarity": 0.08,
            "display_assassin_danger_similarity": 0.2
        }
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Thresholds, cls).__new__(cls)
        return cls._instance

    def initialize_thresholds(self, model_name: str):
        config = self._model_thresholds_mapping[model_name]

        if config is not None:
            self.scoring_target_word_similarity = config["scoring_target_word_similarity"]
            self.scoring_other_own_word_positive_similarity = config["scoring_other_own_word_positive_similarity"]
            self.scoring_opponent_word_negative_similarity = config["scoring_opponent_word_negative_similarity"]
            self.scoring_neutral_word_negative_similarity = config["scoring_neutral_word_negative_similarity"]
            self.scoring_assassin_risk_similarity = config["scoring_assassin_risk_similarity"]
            
            self.display_great_similarity = config["display_great_similarity"]
            self.display_good_similarity = config["display_good_similarity"]
            self.display_ok_similarity = config["display_ok_similarity"]
            self.display_meh_similarity = config["display_meh_similarity"]
            self.display_assassin_safe_similarity = config["display_assassin_safe_similarity"]
            self.display_assassin_danger_similarity = config["display_assassin_danger_similarity"]
        else:
            logging.warn(f"No model-specific thresholds defined for model '{model_name}', using defaults")

            self.scoring_target_word_similarity = 0.5
            self.scoring_other_own_word_positive_similarity = 0.33
            self.scoring_opponent_word_negative_similarity = 0.33
            self.scoring_neutral_word_negative_similarity = 0.33
            self.scoring_assassin_risk_similarity = 0.15
            
            self.display_great_similarity = 0.6
            self.display_good_similarity = 0.5
            self.display_ok_similarity = 0.33
            self.display_meh_similarity = 0.2
            self.display_assassin_safe_similarity = 0.1
            self.display_assassin_danger_similarity = 0.25