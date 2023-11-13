from typing import Optional
from colorama import Fore, Back, Style

from clue import Clue
from thresholds import Thresholds

positive_color_modifiers = [
    (0.6, Fore.GREEN+Style.BRIGHT),
    (0.5, Fore.GREEN+Style.NORMAL),
    (0.33, Fore.GREEN+Style.DIM),
    (0.2, Fore.YELLOW)
]

def get_color_modifiers(negative: Optional[bool] = False):
    thresholds = Thresholds()
    if negative:
        return [
            (thresholds.display_great_similarity, Fore.RED+Style.BRIGHT),
            (thresholds.display_good_similarity, Fore.RED+Style.NORMAL),
            (thresholds.display_ok_similarity, Fore.RED+Style.DIM),
            (thresholds.display_meh_similarity, Fore.YELLOW+Style.DIM)
        ]
    
    return [
        (thresholds.display_great_similarity, Fore.GREEN+Style.BRIGHT),
        (thresholds.display_good_similarity, Fore.GREEN+Style.NORMAL),
        (thresholds.display_ok_similarity, Fore.GREEN+Style.DIM),
        (thresholds.display_meh_similarity, Fore.YELLOW)
    ]

def colorize_score(score: float, negative: Optional[bool] = False) -> str:
    result = ""
    for threshold, style in get_color_modifiers(negative):
        if score > threshold:
            result += style
            break

    result += f"{score:.3f}"
    result += Style.RESET_ALL

    return result

def colorize_assassin_score(score: float) -> str:
    thresholds = Thresholds()
    result = ""
    if score < thresholds.display_assassin_safe_similarity:
        result += Fore.GREEN
    if score > thresholds.display_assassin_danger_similarity:
        result += Fore.RED

    result += f"{score:.3f}"
    result += Style.RESET_ALL

    return result

def colorize_word_scores(scores: list[tuple[str, float]], negative: Optional[bool] = False) -> str:
    result = "["
    first = True
    for word, score in scores:
        if not first:
            result += ", "
        result += "('"
        result += word
        result += "', "
        result += colorize_score(score, negative)
        result += ")"
        first = False
    result += "]"
    return result

def print_clue_details(clue: Clue):
    print(f"--- {Fore.BLUE+Back.WHITE}{clue.clue}{Style.RESET_ALL} ({len(clue.target_words_scores)}) ---")
    
    print(f"\tTarget own words scores: {colorize_word_scores(clue.target_words_scores)}")
    print(f"\tOther own words scored: {colorize_word_scores(clue.other_own_words_scores)}")
    print("\t-------------")
    print(f"\tASSASSIN ({clue.assassin_scores[0][0]}) Score: {colorize_assassin_score(clue.assassin_scores[0][1])}")
    print(f"\tOpponent words scored: {colorize_word_scores(clue.opponent_scores, True)}")
    print(f"\tNeutral words scored: {colorize_word_scores(clue.neutral_scores, True)}")

    score_style = Fore.GREEN
    if clue.total_score < 0:
        score_style = Fore.RED
    if abs(clue.total_score) > 3:
        score_style += Style.BRIGHT
    print(f"\t\tTotal Score: {score_style}{clue.total_score}{Style.RESET_ALL}")
