

# Define functions for interpreting the rules from an input:

# START OF CODE FROM
# https://scipython.com/blog/langtons-ant-on-a-hexagonal-plane/
def parse_rules_string(s):

    # Each 'character' corresponds to a change in direction
    move_dict = {'N': 0, 'L2': -120, 'L1': -60, 'R1': 60, 'R2': 120, 'U': 180}
    rules = []
    i = 0

    # Takes a string such as "L2NNL1L2L1" and turns it into a list such as
    # [L2, N, N, L1, L2, L1]
    while i < len(s):
        t = s[i]
        if t in 'LR' and i != len(s) - 1:
            i += 1
            t += s[i]
        try:
            rules.append(move_dict[t])
        except KeyError:
            raise ValueError('Unidentified move {} in rules {}'
                             .format(t, s))
        i += 1
    return rules
# END OF CODE FROM scipython.com


# Takes a square grid movement pattern such as "LRRL" and turns
# it into a list such as [L, R, R, L]
def square_rule_maker(movement_pattern):

    # Split the string into a list of letters
    movement_pattern_split = [letter for letter in movement_pattern]

    return movement_pattern_split
