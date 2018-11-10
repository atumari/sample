def get_score(past_answers, correct):
    string = ''
    score = 0
    for ch in correct:
        if ch in past_answers:
            string += ch
            score += 1
        else:
            string += '-'
    return string, score


def draw_hangman(status):
    raw1 = '______________'
    raw2 = '│     │      \ '
    raw3 = '│ 　　〇'
    raw4 = '│ ---─┼─---'
    raw5 = '│     │　'
    raw6 = '│　 　/\　'
    raw7 = '│  　/  \ '
    raw8 = '│'
    raw9 = '┴-------------'

    raw3_1 = '│'
    raw4_3 = '│'
    raw5_1 = '│'
    raw6_2 = '│'
    raw7_2 = '│ '

    raw4_1 = '│     ┼─---'
    raw4_2 = '│     │'

    raw6_1 = '│　 　 \　'
    raw7_1 = '│  　   \ '

    raws = [[raw3, raw3_1], [raw4, raw4_1, raw4_2, raw4_3], [raw5, raw5_1],
            [raw6, raw6_1, raw6_2], [raw7, raw7_1, raw7_2]]

    res = raw1 + '\n' + raw2 + '\n'
    for i in range(5):
        j = get_raw_num(i, status)
        res += raws[i][j] + '\n'
    res += raw8 + '\n' + raw9
    return res


def get_raw_num(i, status):
    if i == 0:
        return status == 0
    elif i == 1:
        return max(0, min(3, 4-status))
    elif i == 2:
        return status <= 1
    else:
        return max(0, min(2, 6-status))