"""Educational 1D offside prototype using a custom 50% threshold.

Distances use the same pitch-axis units, increasing from left to right.
Defender positions are their goal-nearest eligible body parts, goalkeeper included.
This does not analyse camera footage and is not an official offside tool.
"""

from math import isfinite

NO_OFFSIDE_RESTARTS = ("goal_kick", "throw_in", "corner_kick")
DIRECTIONS = ("left", "right")


def _number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    return value


def _direction(value):
    if value not in DIRECTIONS:
        raise ValueError("attacking_direction must be 'left' or 'right'")


def get_second_last_defender(defender_positions, attacking_direction):
    """Return the goal-nearest eligible point of the second-last opponent."""
    _direction(attacking_direction)
    positions = list(defender_positions)
    if len(positions) < 2:
        raise ValueError("At least two opponent positions are required")
    for x in positions:
        _number(x, "defender position")
    return sorted(positions)[-2 if attacking_direction == "right" else 1]


def analyse_position(center_x, body_width, defender_positions, ball_x,
                     attacking_direction, halfway_x=50):
    """Analyse the position at the teammate's pass/touch; does not decide involvement.

    50% means the proportion of a 1D eligible body segment beyond the defender
    line. Exactly 50% qualifies, per the original code. Halfway and ball are
    checked using the player's goal-nearest eligible point. Ball_x is the
    goal-nearest point of the ball. Equality with the ball/halfway is onside.
    """
    _direction(attacking_direction)
    for name, value in (("center_x", center_x), ("body_width", body_width),
                        ("ball_x", ball_x), ("halfway_x", halfway_x)):
        _number(value, name)
    if body_width <= 0:
        raise ValueError("body_width must be greater than zero")
    defender_x = get_second_last_defender(defender_positions, attacking_direction)
    # Multiply by -1 when attacking left so 'ahead' always means larger.
    sign = 1 if attacking_direction == "right" else -1
    center = sign * center_x
    defender = sign * defender_x
    front = center + body_width / 2
    back = center - body_width / 2
    fraction = max(0.0, min(1.0, (front - defender) / body_width))
    in_opponent_half = front > sign * halfway_x
    ahead_of_ball = front > sign * ball_x
    position = fraction >= 0.5 and in_opponent_half and ahead_of_ball
    return {
        "second_last_defender": defender_x,
        "fraction_beyond_defender": fraction,
        "in_opponent_half": in_opponent_half,
        "ahead_of_ball": ahead_of_ball,
        "in_offside_position": position,
    }


def check_offside(player_center_x, body_width, defender_positions, ball_x, attacking_direction):
    """Original-style position test, without the halfway-line condition."""
    result = analyse_position(player_center_x, body_width, defender_positions,
                              ball_x, attacking_direction)
    return result["fraction_beyond_defender"] >= 0.5 and result["ahead_of_ball"]


def is_in_opponent_half(center_x, halfway_x, attacking_direction, body_width=0):
    """Check whether any eligible part is in the opponents' half."""
    _direction(attacking_direction)
    for name, value in (("center_x", center_x), ("halfway_x", halfway_x), ("body_width", body_width)):
        _number(value, name)
    if body_width < 0:
        raise ValueError("body_width cannot be negative")
    sign = 1 if attacking_direction == "right" else -1
    return sign * center_x + body_width / 2 > sign * halfway_x


def check_offside_offence(center_x, body_width, defender_positions, ball_x,
                          attacking_direction, halfway_x=50, restart_type=None,
                          touched_ball=False, interfered_with_opponent=False,
                          gained_advantage=False):
    """Return a simplified offence result using manually supplied involvement.

    restart_type refers ONLY to the direct receipt of that restart. These
    booleans are referee inputs, not automated determinations. Other complex
    Law 11 events such as deliberate opponent play are not modelled.
    """
    if restart_type not in (None, *NO_OFFSIDE_RESTARTS):
        raise ValueError("Unknown restart_type")
    position = analyse_position(center_x, body_width, defender_positions, ball_x,
                                attacking_direction, halfway_x)["in_offside_position"]
    involved = touched_ball or interfered_with_opponent or gained_advantage
    return bool(position and involved and restart_type not in NO_OFFSIDE_RESTARTS)


def check_all_attackers(attackers, body_width, defender_positions, ball_x,
                        attacking_direction, halfway_x=50, restart_type=None,
                        involved_players=()):
    """Return a name-to-offence mapping for a dictionary of attacker centres."""
    return {name: check_offside_offence(
        x, body_width, defender_positions, ball_x, attacking_direction,
        halfway_x=halfway_x, restart_type=restart_type,
        touched_ball=name in involved_players,
    ) for name, x in attackers.items()}
