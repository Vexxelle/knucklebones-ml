import knucklebones

def main():
    knucklebones.interface = knucklebones.ui.CLI()
    p_0, p_1 = knucklebones.interface.choose_players()
    knucklebones.play(p_0, p_1)


if __name__ == "__main__":
    main()