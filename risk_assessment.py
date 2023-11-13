from .clue import Clue

def calculate_risk_score(similarities, assassin_similarity, opponent_similarities, neutral_similarities, risk_factors):
    score = sum(similarity for _, similarity in similarities)
    print(f"Total score of target words: {score}")
    if assassin_similarity > risk_factors['min_similarity_assassin']:
        print(f"Subtracting assassin similarity ({assassin_similarity}) multiplied by weight ({risk_factors['assassin_weight']})")
        score -= risk_factors['assassin_weight'] * assassin_similarity
    else:
        print(f"Assassin similarity ({assassin_similarity}) is not over threshold ({risk_factors['min_similarity_assassin']}) - not reducing the score")

    opponent_words_adjustment = sum(risk_factors['opponent_weight'] * similarity for _, similarity in opponent_similarities if similarity > risk_factors['min_similarity_opponent'])
    print(f"Less opponent word similarity score - {opponent_words_adjustment} (counting scores over {risk_factors['min_similarity_opponent']} with {risk_factors['opponent_weight']}x) weight")
    score -= opponent_words_adjustment

    neutral_words_adjustment = sum(risk_factors['neutral_weight'] * similarity for _, similarity in neutral_similarities if similarity > risk_factors['min_similarity_neutral'])
    print(f"Less neutral word similarity score - {neutral_words_adjustment} (counting scores over {risk_factors['min_similarity_neutral']} with {risk_factors['neutral_weight']}x) weight")
    score -= neutral_words_adjustment

    return score