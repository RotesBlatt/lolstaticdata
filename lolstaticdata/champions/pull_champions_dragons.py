from thefuzz import fuzz
from functools import partial


def maximize(func, guesses):
    best = None, -float("inf")
    for params in guesses:
        value = func(params)
        if value > best[1]:
            best = params, value
    return best


def build_guess(
    champion_name,
    ability_name,
    ability_key,
    ability_index,
    include_champion_name,
    include_ability_name,
    include_ability_key,
    include_ability_index,
    use_underscores=True,
):
    ability_name = ability_name.replace("-", "").replace(" ", "").replace("_", "")
    guess = ""
    if include_champion_name:
        guess = guess + f"{champion_name}"
    if include_ability_name:
        if use_underscores and not guess.endswith("_"):
            guess = guess + "_"
        guess = guess + f"{ability_name}"
    if include_ability_key:
        if use_underscores and not guess.endswith("_"):
            guess = guess + "_"
        guess = guess + f"{ability_key}"
    if include_ability_index:
        if use_underscores and not guess.endswith("_"):
            guess = guess + "_"
        guess = guess + f"{ability_index}"
    guess = guess + ".png"
    return guess.lower()


def perform_guess(
    champion_name,
    ability_name,
    ability_key,
    ability_index,
    filenames,
    use_underscores=True,
):
    best_score = -float("inf")
    for include_champion_name in (True, False):
        for include_ability_name in (True, False):
            for include_ability_index in (True, False):
                for include_ability_key in (True, False):
                    if include_champion_name is True and not any(
                        [
                            include_ability_name,
                            include_ability_index,
                            include_ability_key,
                        ]
                    ):
                        continue
                    guess = build_guess(
                        champion_name,
                        ability_name,
                        ability_key,
                        ability_index,
                        include_champion_name,
                        include_ability_name,
                        include_ability_key,
                        include_ability_index,
                        use_underscores=use_underscores,
                    )
                    _fn, score = maximize(partial(fuzz.ratio, guess), filenames)
                    if score > best_score:
                        best_fn, best_score, best_guess = _fn, score, guess
    return best_fn, best_score, best_guess


def _try_champion_specific_patterns(champion_key, ability_key, ability_index, filenames):
    """
    Attempts to find icon filenames for champions with special naming patterns.
    
    Returns the matched filename if found, None otherwise.
    """
    champion_lower = champion_key.lower()
    
    # Generate champion-specific patterns to try
    specific_patterns = []
    
    # Hwei pattern: "hweiee.png", "hweieq.png", "hweiew.png" (no separators, concatenated)
    if champion_lower == "hwei":
        # Try different combinations of ability key repetitions
        specific_patterns.extend([
            f"{champion_lower}{ability_key.lower()}q.png",  
            f"{champion_lower}{ability_key.lower()}w.png",  
            f"{champion_lower}{ability_key.lower()}e.png",  
            f"{champion_lower}{ability_key.lower()}{ability_key.lower()}{ability_index}.png",
        ])
    
    # Heimerdinger pattern: "heimerdinger_q1.png", "heimerdinger_q2.png"
    elif champion_lower == "heimerdinger":
        specific_patterns.extend([
            f"{champion_lower}_{ability_key.lower()}{ability_index}.png",
            f"{champion_lower}_{ability_key.lower()}_{ability_index}.png",
        ])
    
    # Gnar pattern: "gnar_e.png" and "gnarbig_e.png"
    elif champion_lower == "gnar":
        specific_patterns.extend([
            f"{champion_lower}_{ability_key.lower()}.png",
            f"{champion_lower}big_{ability_key.lower()}.png",
            f"{champion_lower}_{ability_key.lower()}{ability_index}.png",
            f"{champion_lower}big_{ability_key.lower()}{ability_index}.png",
        ])
    
    # Elise pattern: "elisehumanq" and "elisespiderq"
    elif champion_lower == "elise":
        specific_patterns.extend([
            f"{champion_lower}human{ability_key.lower()}.png",
            f"{champion_lower}spider{ability_key.lower()}.png",
            f"{champion_lower}human{ability_key.lower()}{ability_index}.png",
            f"{champion_lower}spider{ability_key.lower()}{ability_index}.png",
        ])
    
    # Aurelion Sol pattern: "aurelionsolr1" and "aurelionsolr2" (R only)
    elif champion_lower == "aurelionsol" and ability_key.upper() == "R":
        specific_patterns.extend([
            f"{champion_lower}{ability_key.lower()}{ability_index}.png",
            f"{champion_lower}{ability_key.lower()}_{ability_index}.png",
        ])
    
    # Khazix pattern: "khazix_e" and "khazix_e_red"
    elif champion_lower == "khazix":
        specific_patterns.extend([
            f"{champion_lower}_{ability_key.lower()}.png",
            f"{champion_lower}_{ability_key.lower()}_red.png",
            f"{champion_lower}_{ability_key.lower()}{ability_index}.png",
            f"{champion_lower}_{ability_key.lower()}_red{ability_index}.png",
        ])
    
    # Rell pattern: "rellw" and "rellmount" (W only)
    elif champion_lower == "rell" and ability_key.upper() == "W":
        specific_patterns.extend([
            f"{champion_lower}{ability_key.lower()}.png",
            f"{champion_lower}mount.png",
            f"{champion_lower}{ability_key.lower()}{ability_index}.png",
            f"{champion_lower}mount{ability_index}.png",
        ])
    
    # Riven pattern: "rivenbladeoftheexile" and "rivenwindscar" (R only)
    elif champion_lower == "riven" and ability_key.upper() == "R":
        specific_patterns.extend([
            f"{champion_lower}bladeoftheexile.png",
            f"{champion_lower}windscar.png",
        ])
    
    # Tahm Kench pattern: "tahmkenchwrapper" and "tahmkenchr2" (R only)
    elif champion_lower == "tahmkench" and ability_key.upper() == "R":
        specific_patterns.extend([
            f"{champion_lower}wrapper.png",
            f"{champion_lower}{ability_key.lower()}{ability_index}.png",
            f"{champion_lower}{ability_key.lower()}2.png",
        ])
    
    # Yorick pattern: "yorick_q" and "yorick_q2" (Q only)
    elif champion_lower == "yorick" and ability_key.upper() == "Q":
        specific_patterns.extend([
            f"{champion_lower}_{ability_key.lower()}.png",
            f"{champion_lower}_{ability_key.lower()}{ability_index}.png",
            f"{champion_lower}_{ability_key.lower()}2.png",
        ])
    
    # Try champion-specific patterns with exact matching
    for pattern in specific_patterns:
        for filename in filenames:
            filename_clean = filename.split('/')[-1] if '/' in filename else filename
            if filename_clean.lower() == pattern.lower():
                return filename_clean
    
    return None


def get_ability_url(key, ability_key, ability_index, ability_name, latest_version, ddragon_champion, filenames):
    champion_lower = key.lower()
    
    # Try champion-specific patterns first
    specific_filename = _try_champion_specific_patterns(key, ability_key, ability_index, filenames)
    if specific_filename:
        return f"https://raw.communitydragon.org/latest/game/assets/characters/{champion_lower}/hud/icons2d/{specific_filename}"
    
    # Use fuzzy matching to find the best icon filename for this specific ability
    best_fn, best_score, best_guess = perform_guess(
        champion_name=key,
        ability_name=ability_name,
        ability_key=ability_key,
        ability_index=ability_index,
        filenames=filenames,
    )
    
    # If we found a good match (score > 50), use the matched filename
    if best_fn and best_score > 50:
        # Remove any leading path components and ensure proper format
        filename = best_fn.split('/')[-1] if '/' in best_fn else best_fn
        return f"https://raw.communitydragon.org/latest/game/assets/characters/{champion_lower}/hud/icons2d/{filename}"
    
    # Fallback to the generic pattern if no good match found
    return f"https://cdn.communitydragon.org/latest/champion/{key}/ability-icon/{ability_key[0]}"
