# GENERAL TERMS
PASSED = "bestanden"
GRADE = "Note"
ECTS = "ECTS"
THESIS = "Thesis"
TOTAL_GRADE = "Gesamtnote"

# SECTIONS
CC = "Pflichtbereich"
CE = "Wahlpflichtbereich"
KS = "Schlüsselqualifikationsbereich"
TH = "Abschlussbereich"

# PATTERNS
# module structure: "• <module_name> [<module_info>] <grade> <ECTS>"
p_module = r"•\s([^•]*)\s\[.*\]\s?(\d,\d|bestanden)\d?\s(2|3|5|10)"

# ECTS targets
ects_targets = {
    CC: 100,
    CE: 50,
    KS: 20,
    TH: 10
}

# ASQ list
# todo: needs to be completed
asq_list = ["Ringvorlesung: Digitale Innovationen"]
