import math
import statistics
from utils.config import *


def get_ects_sec(data, sec):
    ects_sum = 0
    for _, module_name in data[sec].items():
        ects_sum += module_name[ECTS]
    return ects_sum


def get_grade_sec(data, sec, target):
    if get_ects_sec(data, sec) > target:
        # get 10 best grades
        # todo: 10 should be a variable
        all_grades_sec = []
        for _, module_name in data[sec].items():
            if module_name[GRADE] != PASSED:
                all_grades_sec.append(module_name[GRADE])
        best_grades_sec = sorted(all_grades_sec)[:10]

        grade_sum = 0
        ects_sum = 0
        for _, module_name in data[sec].items():
            if module_name[GRADE] != PASSED and module_name[GRADE] in best_grades_sec:
                grade_sum += module_name[GRADE] * module_name[ECTS]
                ects_sum += module_name[ECTS]
    else:
        grade_sum = 0
        ects_sum = 0
        for _, module_name in data[sec].items():
            if module_name[GRADE] != PASSED:
                grade_sum += module_name[GRADE] * module_name[ECTS]
                ects_sum += module_name[ECTS]
    grade_sec = grade_sum / ects_sum
    return float(f"{grade_sec:.3f}")


def get_ects_total(data, secs, thesis_grade):
    ects_sum = 0
    for sec in secs:
        ects_sum += get_ects_sec(data, sec)
    if thesis_grade:
        ects_sum += ects_targets[TH]
    return min(ects_sum, 180) # to make sure value is max 180


def get_grade_total(data, secs, thesis_grade):
    grade_sum = 0
    ects_sum = 0
    for sec in secs:
        ects_sec = get_ects_sec(data, sec)
        ects_sum += ects_sec
        grade_sec = math.floor(get_grade_sec(data, sec, ects_targets[sec]) * 10) / 10
        grade_sum += grade_sec * ects_sec
    if thesis_grade:
        ects_sum += ects_targets[TH]
        grade_sum += thesis_grade * ects_targets[TH]
    grade_total = grade_sum / ects_sum
    return float(f"{grade_total:.3f}")


def get_modal_info(data):
    all_grades = get_all_grades_rec(data)
    all_grades = [x for x in all_grades if x != PASSED]
    mode = statistics.mode(all_grades)
    if isinstance(mode, list):
        mode = mode[0] # to make sure it's only one value
    per_share = get_per_share(mode, all_grades)
    return [mode, per_share]


def get_all_grades_rec(data):
    all_grades = []
    for key, value in data.items():
        if isinstance(value, dict):
            all_grades.extend(get_all_grades_rec(value))
        elif key == GRADE:
            all_grades.append(value)
    return all_grades


def get_per_share(mode, all_grades):
    count = all_grades.count(mode)
    share = count / len(all_grades) if len(all_grades) > 0 else 0
    return round(share * 100, 1)
