class NFA:
    def __init__(self, stari, alfabet, tranzitii, stare_initiala, stari_finale):
        if stare_initiala not in stari:
            raise ValueError("Starea intiala nu este in setul de stari.")
        if not stari_finale.issubset(stari):
            raise ValueError("starile finale nu sunt un subset al starilor.")
        
        self.stari = stari
        self.alfabet = alfabet
        self.tranzitii = tranzitii
        self.stare_initiala = stare_initiala
        self.stari_finale = stari_finale

    def _epsilon_closure(self, stari_curente):
        closure = set(stari_curente)
        stack = list(stari_curente) 
        while stack:
            stare = stack.pop()
            if (stare, None) in self.tranzitii:
                for next_state in self.tranzitii[(stare, None)]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def accepta(self, sir_intrare):
        stari_posibile = self._epsilon_closure({self.stare_initiala})

        for simbol in sir_intrare:
            if simbol not in self.alfabet:
                print(f"Simbol '{simbol}' nu este in alfabet")
                return False

            next_stari_temp = set()
            for stare_curenta in stari_posibile:
                if (stare_curenta, simbol) in self.tranzitii:
                    next_stari_temp.update(self.tranzitii[(stare_curenta, simbol)])

            stari_posibile = self._epsilon_closure(next_stari_temp)
            if not stari_posibile:
                return False

        return not stari_posibile.isdisjoint(self.stari_finale)

### Exemplu (NFA pentru `a*b|aba`)

#Sa definim un NFA care accepta sirul format din b urmat de un numar de a sau exact sirul 'aba'

#Stari: q0, q1, q2, q3, q4, q5
#Alfabet: a, b
#Stare inițială:** `q0`
# Stari finale: q2, q5
# Tranzitii:
#    (q0, a) -> q0 (pentru a)
#    (q0, b) -> q1 (pentru b din ab)
#    (q1, None) -> q2 (e-tranzitie la starea finala q2)
#    (q0, a) -> q3 (inceputul lui aba)
#    (q3, b) -> q4
#    (q4, a) -> q5 (stare finala q5)

stari = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5'}
alfabet = {'a', 'b'}
stare_initiala = 'q0'
stari_finale = {'q2', 'q5'}

tranzitii = {
    ('q0', 'a'): {'q0', 'q3'}, # Poate merge in q0 (a*) sau q3 (start aba)
    ('q0', 'b'): {'q1'},      # Pentru a*b
    ('q1', None): {'q2'},     # Epsilon transition la stare finala pentru a*b
    ('q3', 'b'): {'q4'},      # Pentru aba
    ('q4', 'a'): {'q5'},      # Pentru aba
}

nfa = NFA(stari, alfabet, tranzitii, stare_initiala, stari_finale)

print("--- Testare NFA ---")
print(f"sir 'a': {nfa.accepta('a')}") # False
print(f"sir 'b': {nfa.accepta('b')}") # True 
print(f"sir 'ab': {nfa.accepta('ab')}") # True
print(f"sir 'aab': {nfa.accepta('aab')}") # True
print(f"sir 'aba': {nfa.accepta('aba')}") # True
print(f"sir 'aaba': {nfa.accepta('aaba')}") # False
print(f"sir 'abc': {nfa.accepta('abc')}") # False 
print(f"sir '': {nfa.accepta('')}") # False 