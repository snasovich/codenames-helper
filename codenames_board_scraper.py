import logging

from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def load_board_from_chrome(own_words_red: bool, debugger_address: Optional[str] = "127.0.0.1:9222") -> dict[str, list[str]]:
    board_words = {
        "spymaster": [],
        "opponent": [],
        "neutral": [],
        "assassin": []
    }

    card_class_type_mapping = {
        "gray": "neutral",
        "black": "assassin"
    }
    if own_words_red:
        card_class_type_mapping["red"] = "spymaster"
        card_class_type_mapping["blue"] = "opponent"
    else:
        card_class_type_mapping["blue"] = "spymaster"
        card_class_type_mapping["red"] = "opponent"

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)

    driver_service = Service()

    driver = webdriver.Chrome(service=driver_service, options=chrome_options)

    # most cards have `card` and `text-black` CSS classes except assassin card that has `card` and `text-white`
    cards = driver.find_elements(By.CSS_SELECTOR, ".card.text-black")
    cards.extend(driver.find_elements(By.CSS_SELECTOR, ".card.text-white"))

    for card in cards:
        text = card.text.lower().strip()
        
        # This is a bit hacky but fine at least for now
        parent_element = card.find_element(By.XPATH, "./..")
        if "revealed" in parent_element.get_attribute("aria-label").split(" "):
            logging.debug(f"Card '{text}' has already been revealed. IGNORED. Moving on!")
            continue
            
        classes = card.get_attribute("class").split(" ")
        for card_class, card_type in card_class_type_mapping.items():
            is_found = False
            if card_class in classes:
                if is_found:
                    logging.debug(f"Card '{text}' has class '{card_class}' but was already categorized due to having another class! This can't be!")
                    exit
                is_found = True
                logging.debug(f"Card '{text}' has class '{card_class}' and is thus categorized as '{card_type}'")
                board_words[card_type].append(text)

    return board_words