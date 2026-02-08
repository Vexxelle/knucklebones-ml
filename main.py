import knucklebones

def main():
    knucklebones.game.interface = knucklebones.ui.Test_UI()
    p_0, p_1 = knucklebones.game.interface.choose_players()
    knucklebones.play(p_0, p_1)


if __name__ == "__main__":
    main()