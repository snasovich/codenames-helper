from board_scraper import load_board_from_chrome

_board_word_samples = [
    {
        "spymaster": ["shadow", "ice", "trip", "scale", "ground", "snowman", "bermuda", "paste", "bed"],
        "opponent": ["moscow", "saturn", "row", "disease", "face", "crane", "van", "buffalo"],
        "neutral": ["hole", "sound", "duck", "board", "press", "part", "rome"],
        "assassin": ["kid"]
    },
    {
        'spymaster': ['platypus', 'green', 'crash', 'sub', 'ray', 'plane', 'row', 'jupiter', 'mint'],
        'opponent': ['block', 'india', 'embassy', 'sock', 'scale', 'round', 'phoenix', 'night'],
        'neutral': ['canada', 'whale', 'pool', 'jam', 'center', 'undertaker', 'ninja'],
        'assassin': ['rose']
    },
    {
        'spymaster': ['platypus', 'green', 'sub', 'ray', 'row', 'jupiter', 'mint'],
        'opponent': ['block', 'india', 'embassy', 'sock', 'scale', 'round', 'phoenix', 'night'],
        'neutral': ['canada', 'whale', 'pool', 'jam', 'center', 'undertaker', 'ninja'],
        'assassin': ['rose']
    }
]

def _select_board_word_sample() -> dict[str, list[str]]:
    while True:
        print("\nSelect the sample board state:")
        print("0. Go back!")
        for i, value in enumerate(_board_word_samples):
            print(f"{i+1}. {value}")
        try:
            choice = int(input("Enter your choice: "))
            if choice == 0:
                return None
            elif choice <= len(_board_word_samples):
                return _board_word_samples[choice-1]
            else:
                print("Choice is not in range of allowed option. Please try again.")
                continue
        except ValueError:
            print("Please enter a valid (number) input. Please try again.")

def select_board_words() -> dict[str, list[str]]:
    while True:
        print("\nSelect the board state source:")
        print(f"\t1. Use built-in samples (have {len(_board_word_samples)} sets)")
        print("\t2. Load from running 'codenames.game' Chrome window")
        print("\t3. Go back!")
    
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                board_words = _select_board_word_sample()
                if board_words == None:
                    print("No built-in sample was selected.  Please try again.")
                    continue
                return board_words
            elif choice == 2:
                # TODO: Render some instructions how to start Chrome properly
                # TODO: This is temporary, need to ask whether current team is red or blue
                return load_board_from_chrome(True)
            elif choice == 3:
                return None
            else:
                print("Choice is not in range of allowed option. Please try again.")
                continue
        
        except ValueError:
            print("Please enter a valid (number) input. Please try again.")
