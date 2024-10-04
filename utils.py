import math
import statistics


def get_area_ects(data, area):
    ects_sum = 0
    for _, module in data[area].items():
        ects_sum += module["ECTS"]
    return ects_sum


def get_area_grade(data, area, targets):
    if get_area_ects(data, area) > targets[area]:
        # get 10 best grades
        all_grades = []
        for _, module in data[area].items():
            if module["Note"] != "bestanden":
                all_grades.append(module["Note"])
        best_grades = sorted(all_grades)[:10]

        grade_sum = 0
        ects_sum = 0
        for _, module in data[area].items():
            if module["Note"] != "bestanden" and module["Note"] in best_grades:
                grade_sum += module["Note"] * module["ECTS"]
                ects_sum += module["ECTS"]
        return float('%.3f' % (grade_sum / ects_sum))
    else:
        grade_sum = 0
        ects_sum = 0
        for _, module in data[area].items():
            if module["Note"] != "bestanden":
                grade_sum += module["Note"] * module["ECTS"]
                ects_sum += module["ECTS"]
        return float('%.3f' % (grade_sum / ects_sum))


def get_total_ects(data, areas, thesis_grade):
    ects_sum = 0
    for area in areas:
        ects_sum += get_area_ects(data, area)
    if thesis_grade:
        ects_sum += 10
    if ects_sum > 180:
        ects_sum = 180
    return ects_sum


def get_total_grade(data, areas, thesis_grade, targets):
    grade_sum = 0
    ects_sum = 0
    for area in areas:
        grade = math.floor(get_area_grade(data, area, targets) * 10) / 10
        ects = get_area_ects(data, area)
        grade_sum += grade * ects
        ects_sum += ects
    if thesis_grade:
        grade_sum += thesis_grade * 10
        ects_sum += 10
    return float('%.3f' % (grade_sum / ects_sum))


def get_modal_grade(data):
    all_grades = get_all_grades_rec(data)
    all_grades = [x for x in all_grades if x != "bestanden"]
    modalwert = statistics.mode(all_grades)
    if isinstance(modalwert, list):
        modalwert = modalwert[0]
    anteil = share_of_modal_grade(modalwert, all_grades)
    return [modalwert, anteil]


def share_of_modal_grade(modalwert, all_grades):
    count = all_grades.count(modalwert)
    ratio = count / len(all_grades) if len(all_grades) > 0 else 0
    return round(ratio * 100, 1)


def get_all_grades_rec(data):
    all_grades = []  # Liste zur Speicherung aller Noten
    for key, value in data.items():
        if isinstance(value, dict):  # Überprüfe, ob der Wert ein Dictionary ist
            all_grades.extend(get_all_grades_rec(value))  # Rekursiver Aufruf und Noten hinzufügen
        elif key == "Note":  # Wenn der Schlüssel "Note" ist
            all_grades.append(value)  # Note zur Liste hinzufügen
    return all_grades  # Rückgabe der gesammelten Noten
