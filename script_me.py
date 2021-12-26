def absorb_left(left, right):
    return left[:len(left) - 1] + right + left[-1:]


def absorb_right(left, right):
    return right[0] + left + right[1:]


def combine(left, right):
    return left + right


def get_level(s):
    level = 0
    m = 1
    for i in s:
        if i == '(':
            level += 1
        else:
            level -= 1
        m = max(m, level)
    return m


def solve(left, right):
    l_level = get_level(left)
    r_level = get_level(right)
    if r_level > l_level:
        return absorb_right(left, right)
    if r_level < l_level:
        return absorb_left(left, right)
    return combine(left, right)


while True:
    problem = input().split(" + ")

    current = solve(problem[0], problem[1])

    for i in problem[2:]:
        current = solve(current, i)

    print(current)
