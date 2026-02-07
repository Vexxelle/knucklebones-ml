import main as kb

players = [kb.Pupser, kb.Aggressive_Player, kb.Random_Player, kb.Sequential_Player, kb.Smart_Player, kb.Combo_Player, kb.Stupip_Player]

matches_per_player = 10000

def gather_statistics(p1: kb.Player, p2: kb.Player, num_matches: int) -> dict:
    match_outcomes = []
    for _ in range(num_matches):
        result = kb.play_knucklebones(p1, p2)
        match_outcomes.append(result)

    # Evaluate Outcomes
    stats = {}
    stats["p1_wins"] = sum([1 for match in match_outcomes if match[0] > match[1]])
    stats["p1_losses"] = sum([1 for match in match_outcomes if match[0] < match[1]])
    stats["ties"] = sum([1 for match in match_outcomes if match[0] == match[1]])
    try: stats["winrate"] = stats["p1_wins"]/(num_matches-stats["ties"])
    except ZeroDivisionError: stats["winrate"] = 0.5 

    return stats



for p_1 in players:
    for p_2 in players:
        print("\n"*4)
        print(p_1.__name__ + " vs " + p_2.__name__)
        print(gather_statistics(p_1("1"),p_2("2"),matches_per_player))
        