import knucklebones

def main():
    print("Hello from knucklebones-ml!")
    p_0 = knucklebones.Human_Player(input("Player 1 Name: "))
    if bool(input("Play against a bot? (y/n): ").lower() == 'y'):
        p_1 = knucklebones.ai_players.Random_Player("Bot")
    else:
        p_1 = knucklebones.Human_Player(input("Player 2 Name: "))
    knucklebones.play(p_0, p_1, ui=True)


if __name__ == "__main__":
    main()
