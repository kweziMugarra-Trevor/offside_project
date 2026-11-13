"""Run a sample scenario or enter your own measurements."""
from offside import analyse_position, check_offside_offence


def show_result(name, center, width, defenders, ball, direction, halfway,
                restart, touched, interfered, advantage):
    data = analyse_position(center, width, defenders, ball, direction, halfway)
    offence = check_offside_offence(center, width, defenders, ball, direction,
                                    halfway, restart, touched, interfered, advantage)
    print(f"\n--- {name} ---")
    print(f"Second-last opponent line: {data['second_last_defender']:.2f}")
    print(f"Body beyond defender: {data['fraction_beyond_defender'] * 100:.1f}%")
    print(f"Any eligible body part in opponents' half: {data['in_opponent_half']}")
    print(f"Any eligible body part ahead of ball: {data['ahead_of_ball']}")
    print(f"Custom 50% offside position: {data['in_offside_position']}")
    print(f"Simplified offside offence: {offence}")
    print("Decision support prototype only, not an official decision.")


def yes_no(question):
    while True:
        answer = input(question + " (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")


def main():
    print("50% Offside Prototype | Educational demonstration")
    print("1. Run an example\n2. Enter a scenario")
    choice = input("Choose 1 or 2: ").strip()
    if choice == "1":
        show_result("Amir", 60, 2, [30, 45, 48, 52], 40, "right", 50,
                    None, True, False, False)
    elif choice == "2":
        try:
            print("Use the same units for all positions. Include the goalkeeper.")
            name = input("Player name: ").strip() or "Player"
            direction = input("Attacking direction (left/right): ").strip().lower()
            center = float(input("Player's body centre on pitch axis: "))
            width = float(input("Eligible body extent along pitch axis: "))
            defenders = [float(x.strip()) for x in input(
                "Opponent goal-nearest points, separated by commas: ").split(",")]
            ball = float(input("Ball's goal-nearest point: "))
            halfway = float(input("Halfway line position (e.g. 50): "))
            restart = input("Direct restart (goal_kick/throw_in/corner_kick/none): ").strip().lower()
            if restart == "none" or restart == "":
                restart = None
            touched = yes_no("Did the player touch the ball?")
            interfered = yes_no("Did the player interfere with an opponent?")
            advantage = yes_no("Did the player gain an advantage under Law 11?")
            show_result(name, center, width, defenders, ball, direction, halfway,
                        restart, touched, interfered, advantage)
        except ValueError as exc:
            print(f"Invalid input: {exc}. Please run the program again.")
    else:
        print("Please run again and choose 1 or 2.")


if __name__ == "__main__":
    main()
