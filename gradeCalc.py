"""
Calculates your exact grade via your Transcript of Records (ToR).
No files will be uploaded, only local storage of personal information.

Abbreviations for the four main sections based on the ToR:
* CC = compulsory courses
* CE = compulsory electives
* KS = key skill area
* TH = thesis

Made with ❤ by croco22.
"""
import json
import re
from PyPDF2 import PdfReader
from utils.utils import *

sections = [CC, CE, KS]  # special case for TH

reader = PdfReader("ToRs/Modulbescheinigung180.pdf")
text = ""

for page in reader.pages:
    text = text + page.extract_text()

data = {
    CC: {},
    CE: {},
    KS: {},
    THESIS: {}
}

# store grades in data dict
for section in sections:
    p_section = rf"{section}(.*)Gesamt\s{section}"
    module_text = re.search(p_section, text, flags=re.DOTALL).group(1)
    for match in re.findall(p_module, module_text):
        module_name = match[0].strip()
        module_grade = match[1] if match[1] == PASSED else float(match[1].replace(",", "."))
        if module_name in asq_list:
            module_grade = PASSED # grade of ASQs can be ignored
        data[section][module_name] = {
            GRADE: module_grade,
            ECTS: int(match[2])
        }

# thesis uses a different type of text field
p_section = rf"{TH}(.*)Gesamt\s{TH}"
module_text = re.search(p_section, text, flags=re.DOTALL).group(1)
if module_text:
    match = re.search(r"(\d,\d)", module_text)
    if match:
        thesis_grade = float(match.group().replace(",", "."))
    else:
        thesis_grade = None
    data[THESIS] = {
        GRADE: thesis_grade,
        ECTS: ects_targets[TH]
    }
else:
    thesis_grade = None

# store dict in a local file
with open("data.json", 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=4)

# print output to console
print("### DEINE NOTEN ###")
for section in sections:
    ects_section = get_ects_sec(data, section)
    if ects_section > ects_targets[section]:
        ects_section = ects_targets[section]
    grade_section = get_grade_sec(data, section, ects_targets[section])
    f_grade_section = math.floor(grade_section * 10) / 10
    print(f"{section} ({ects_section} {ECTS}): {grade_section}\t\t[gewertet als {f_grade_section}]")
if thesis_grade:
    print(f"{THESIS} ({ects_targets[TH]} {ECTS}): {thesis_grade}")

ects_total = get_ects_total(data, sections, thesis_grade)
grade_total = get_grade_total(data, sections, thesis_grade)
f_grade_total = math.floor(grade_total * 10) / 10
print(f"{TOTAL_GRADE} ({ects_total} {ECTS}): {grade_total}\t\t[also {f_grade_total}]")

modal_info = get_modal_info(data)
print(f"Deine häufigste Note im Studium war eine {modal_info[0]} ({modal_info[1]} %)")
