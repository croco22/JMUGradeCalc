"""
Coding project by Philipp Landeck.
Calculate your grade and ... by analyzing your Transcript of Records.

Abbreviations for grading areas:
* CC = compulsory courses
* CE = compulsory electives
* KS = key skill area
"""
from PyPDF2 import PdfReader
import re
import json
from utils import *
import math


# grading areas
CC = "Pflichtbereich"
CE = "Wahlpflichtbereich"
KS = "Schlüsselqualifikationsbereich"
AREAS = [CC, CE, KS]

# ECTS targets
targets = {
    CC: 100,
    CE: 50,
    KS: 20
}

# module structure: "• <module_name> [<module_info>] <grade> <ECTS>"
pattern_module = r"•\s([^•]*)\s\[.*\]\s?(\d,\d|bestanden)\d?\s(2|3|5|10)"

reader = PdfReader("ToRs/Modulbescheinigung180.pdf")
text = ""

for page in reader.pages:
    text = text + page.extract_text()

data = {
    CC: {},
    CE: {},
    KS: {},
    "Thesis": {}
}

for area in AREAS:
    pattern_area = rf"{area}(.*)Gesamt\s{area}"
    modules = re.search(pattern_area, text, flags=re.DOTALL).group(1)
    for match in re.findall(pattern_module, modules):
        name = match[0].strip()
        grade = match[1] if match[1] == "bestanden" else float(match[1].replace(",", "."))
        if name == "Ringvorlesung: Digitale Innovationen": # Ausnahme: ASQ mit Note
            grade = "bestanden"
        data[area][name] = {
            "Note": grade,
            "ECTS": int(match[2])
        }


# Ausnahme: Thesis
pattern_area = r"Abschlussbereich(.*)Gesamt\sAbschlussbereich"
modules = re.search(pattern_area, text, flags=re.DOTALL).group(1)
if modules:
    match = re.search(r"(\d,\d)", modules)
    if match:
        thesis_grade = float(match.group().replace(",", "."))
    else:
        thesis_grade = 0
    data["Thesis"] = {
        "Note": thesis_grade,
        "ECTS": 10
    }
else:
    thesis_grade = None


with open("data.json", 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=4)

print("### DEINE NOTEN ###")
for area in AREAS:
    area_ects = get_area_ects(data, area)
    if area_ects > targets[area]:
        area_ects = targets[area]
    print(f"{area} ({area_ects} ECTS): {get_area_grade(data, area, targets)}\t\t[gewertet als {math.floor(get_area_grade(data, area, targets) * 10) / 10}]")
if thesis_grade:
    print(f"Thesis (10 ECTS): {thesis_grade}")
print(f"Gesamtnote ({get_total_ects(data, AREAS, thesis_grade)} ECTS): {get_total_grade(data, AREAS, thesis_grade, targets)}\t\t[also {math.floor(get_total_grade(data, AREAS, thesis_grade, targets) * 10) / 10}]")
print()
modal_info = get_modal_grade(data)
print(f"Deine häufigste Note im Studium war eine {modal_info[0]} ({modal_info[1]} %)")
