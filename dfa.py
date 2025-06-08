import re
from pprint import pprint

def citeste_dfa_si_intrare(fisier):
    """
    Citeste un DFA si secventa de intrare dintr-un fisier.
    """
    with open(fisier, 'r') as f:
        text = f.read()

    linii = [
        linie.split('#')[0].strip()  
        for linie in text.strip().split('\n') 
        if linie.strip() and not linie.strip().startswith('#')
    ]
    
    dfa = {
        'alfabet': set(),
        'stari': set(),
        'stare_initiala': None,
        'tranzitii': {},
        'stari_finale': set(),
        'intrare': []
    }

    regex_alfabet = r"^alfabet\s*:\s*([\w,\s]+);$"
    regex_stari = r"^stari\s*:\s*([\w,\s]+);$"
    regex_initiala = r"^stare initiala\s*:\s*(\w+);$"
    regex_tranzitii = r"^reguli\s*:\s*(.*);$"
    regex_finale = r"^stari finale\s*:\s*([\w,\s]+);$"
    regex_intrare = r"^intrare\s*:\s*([\w,\s]+);$"
    regex_tranzitie = r"(\w+)\((\w)\)(\w+)"

    for linie in linii:
        if match := re.match(regex_alfabet, linie):
            dfa['alfabet'] = set(x.strip() for x in match.group(1).split(','))

        elif match := re.match(regex_stari, linie):
            dfa['stari'] = set(x.strip() for x in match.group(1).split(','))

        elif match := re.match(regex_initiala, linie):
            dfa['stare_initiala'] = match.group(1)

        elif match := re.match(regex_finale, linie):
            dfa['stari_finale'] = set(x.strip() for x in match.group(1).split(','))

        elif match := re.match(regex_tranzitii, linie):
            reguli = match.group(1)
            tranzitii = re.findall(regex_tranzitie, reguli)
            for stare_curenta, simbol, stare_urmatoare in tranzitii:
                dfa['tranzitii'][(stare_curenta, simbol)] = stare_urmatoare

        elif match := re.match(regex_intrare, linie):
            dfa['intrare'] = [x.strip() for x in match.group(1).split(',')]

    return dfa

def ruleaza_dfa(dfa):
    stare_curenta = dfa['stare_initiala']

    print(f"Stare initiala: {stare_curenta}")

    for simbol in dfa['intrare']:
        print(f"Tranzitie: ({stare_curenta}, {simbol}) -> ", end="")
        if (stare_curenta, simbol) in dfa['tranzitii']:
            stare_curenta = dfa['tranzitii'][(stare_curenta, simbol)]
            print(f"{stare_curenta}")
        else:
            print("Tranzitie invalida!")
            return False

    print(f"\nStare finala atinsa: {stare_curenta}")

    if stare_curenta in dfa['stari_finale']:
        print("Secventa este ACCEPTATA!")
        return True
    else:
        print("Secventa este RESPINSA!")
        return False

dfa = citeste_dfa_si_intrare("intrare.txt")
pprint(dfa)

ruleaza_dfa(dfa)