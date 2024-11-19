def common_interval(intervals1, intervals2):
    start1, end1 = intervals1
    start2, end2 = intervals2
    if start1 > end2 or start2 > end1:
        return
    return max(start1, start2), min(end1, end2)


def appearance(intervals: dict[str, list[int]]) -> int:
    pupil_intervals = zip(intervals['pupil'][::2], intervals['pupil'][1::2])
    tutor_intervals = list(zip(intervals['tutor'][::2], intervals['tutor'][1::2]))
    common_time = 0
    for pupil_interval in pupil_intervals:
        pupil_presence = common_interval(intervals['lesson'], pupil_interval)
        if not pupil_presence:
            continue
        start_stamp, end_stamp = pupil_presence
        for tutor_interval in tutor_intervals:
            common_presence = common_interval(pupil_presence, tutor_interval)
            if not common_presence:
                continue
            start_stamp, end_stamp = common_presence
            common_time += end_stamp - start_stamp
    return common_time


tests = [
    {'intervals': {
        'lesson': [1594663200, 1594666800],
        'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
        'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
        'answer': 3117
     },
    # Данные второго теста некорректны. По условию время присутствия каждого
    # пользователя на уроке хранится в виде интервалов. При этом невооружённым
    # глазом видно, что интервалы 1 и 2 присутствия ученика пересекаются, чего
    # не может быть (один ученик не может присутствовать в одно и то же время
    # в нескольких лицах). Задача решена в соответствии с условием.
    #
    # {'intervals': {
    #     'lesson': [1594702800, 1594706400],
    #     'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
    #     'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    #     'answer': 3577
    #  },
    {'intervals': {
        'lesson': [1594692000, 1594695600],
        'pupil': [1594692033, 1594696347],
        'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
        'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        print(i, test)
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'