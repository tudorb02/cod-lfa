class TuringMachine:
    def __init__(self, tape_input, initial_state, final_states, blank_symbol='_', transitions=None):
        
        self.tape = list(tape_input) 
        self.head_position = 0      
        self.current_state = initial_state
        self.final_states = final_states
        self.blank_symbol = blank_symbol
        self.transitions = transitions if transitions is not None else {}
        
       
        self.tape_offset = 0 

    def _extend_tape(self):
        while self.head_position < 0: 
            self.tape.insert(0, self.blank_symbol)
            self.head_position += 1
            self.tape_offset += 1
        while self.head_position >= len(self.tape): 
            self.tape.append(self.blank_symbol)

    def _read_symbol(self):
        self._extend_tape()
        return self.tape[self.head_position]

    def _write_symbol(self, symbol):
        self._extend_tape()
        self.tape[self.head_position] = symbol

    def _move_head(self, direction):
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
        else:
            raise ValueError("Directie de miscare invalida. Foloseste 'R' sau 'L'.")
        self._extend_tape() 
        
    def _get_tape_string(self):
        first_char_idx = 0
        last_char_idx = len(self.tape) - 1

        while first_char_idx < len(self.tape) and self.tape[first_char_idx] == self.blank_symbol:
            first_char_idx += 1
        while last_char_idx >= 0 and self.tape[last_char_idx] == self.blank_symbol:
            last_char_idx -= 1

        if first_char_idx > last_char_idx: 
            return self.blank_symbol
        
        return "".join(self.tape[first_char_idx : last_char_idx + 1])

    def run(self, max_steps=1000):
        print(f"Incepe rularea. Stare initiala: {self.current_state}, Banda: {self._get_tape_string()}")
        print("-" * 30)

        for step in range(max_steps):
            if self.current_state in self.final_states:
                print(f"\nFinal: Stare finala '{self.current_state}' atinsa. Sir ACCEPTAT.")
                return True

            current_symbol = self._read_symbol()
            transition_key = (self.current_state, current_symbol)

            if transition_key not in self.transitions:
                print(f"\nFinal: Nu exista tranzitie pentru ({self.current_state}, {current_symbol}). Sir RESPINS.")
                return False

            next_state, symbol_to_write, direction = self.transitions[transition_key]

            self._write_symbol(symbol_to_write)
            self._move_head(direction)
            self.current_state = next_state

            tape_str = "".join(self.tape)
            head_indicator = ' ' * (self.head_position + self.tape_offset) + '^'
            print(f"Pas {step+1}: Stare: {self.current_state}, Banda: {tape_str}\n{head_indicator}")

        print(f"\nFinal: Numarul maxim de pasi ({max_steps}) atins. Sir RESPINS (posibil bucla infinita).")
        return False

# --- Exemplu de utilizare: Masina Turing pentru limbajul {0^n1^n | n >= 1} ---
# Aceasta masina marcheaza primul '0' cu 'X', primul '1' cu 'Y',
# se intoarce la stanga pentru urmatorul '0', si repeta.
# Daca gaseste '1' fara '0' sau '0' fara '1', respinge.

# Stari:
# q0: Starea initiala, cauta primul '0'.
# q1: A marcat '0', cauta primul '1'.
# q2: A marcat '1', cauta '0' nemarcat.
# q3: A marcat '0' si '1', a terminat de marcat '0'-uri. Verifica daca au mai ramas '1'-uri.
# qf: Stare finala de acceptare.

BLANK = '_'

# Tranzitiile (dict: (stare_curenta, simbol_citit): (stare_urmatoare, simbol_de_scris, directie))
transitions = {
    # Starea q0: Cauta un '0' nemarcat sau verifica acceptarea
    ('q0', '0'): ('q1', 'X', 'R'), # A gasit '0', il marcheaza cu 'X', merge dreapta
    ('q0', 'Y'): ('q3', 'Y', 'R'), # A terminat de marcat toate 0-urile si 1-urile, verifica sa nu mai fie 1-uri
    ('q0', BLANK): ('qf', BLANK, 'R'), # String gol ('') sau toate au fost marcate. Accepta.

    # Starea q1: A marcat un '0' cu 'X', cauta un '1'
    ('q1', '0'): ('q1', '0', 'R'), # Sarit peste 0-uri nemarcate
    ('q1', 'Y'): ('q1', 'Y', 'R'), # Sarit peste 1-uri marcate
    ('q1', '1'): ('q2', 'Y', 'L'), # A gasit '1', il marcheaza cu 'Y', merge stanga
    
    # Starea q2: A marcat un '1' cu 'Y', cauta un '0' nemarcat (se intoarce la stanga)
    ('q2', '0'): ('q2', '0', 'L'), # Sarit peste 0-uri nemarcate
    ('q2', 'X'): ('q0', 'X', 'R'), # A gasit 'X' (0 marcat), se intoarce la q0 pentru urmatorul ciclu
    ('q2', 'Y'): ('q2', 'Y', 'L'), # Sarit peste 1-uri marcate
    
    # Starea q3: A marcat toate 0-urile si 1-urile. Verifica sa nu mai fie 1-uri ramase
    ('q3', 'Y'): ('q3', 'Y', 'R'), # Sarit peste 1-uri marcate
    ('q3', BLANK): ('qf', BLANK, 'R'), # A ajuns la blank, toate 1-urile au fost marcate. Accepta.
}

# Crearea si rularea Masinii Turing

# Exemplu 1: Acceptat (0011)
print("\n=== Testare: 0011 ===")
tm1 = TuringMachine(tape_input="0011", initial_state='q0', final_states={'qf'}, blank_symbol=BLANK, transitions=transitions)
tm1.run()

# Exemplu 2: Acceptat (01)
print("\n=== Testare: 01 ===")
tm2 = TuringMachine(tape_input="01", initial_state='q0', final_states={'qf'}, blank_symbol=BLANK, transitions=transitions)
tm2.run()

# Exemplu 3: Acceptat (000111)
print("\n=== Testare: 000111 ===")
tm3 = TuringMachine(tape_input="000111", initial_state='q0', final_states={'qf'}, blank_symbol=BLANK, transitions=transitions)
tm3.run()

# Exemplu 4: Respins (001) - prea multe 0-uri
print("\n=== Testare: 001 ===")
tm4 = TuringMachine(tape_input="001", initial_state='q0', final_states={'qf'}, blank_symbol=BLANK, transitions=transitions)
tm4.run()

# Exemplu 5: Respins (011) - prea multe 1-uri
print("\n=== Testare: 011 ===")
tm5 = TuringMachine(tape_input="011", initial_state='q0', final_states={'qf'}, blank_symbol=BLANK, transitions=transitions)
tm5.run()

# Exemplu 6: Respins (10) - ordine gresita
print("\n=== Testare: 10 ===")
tm6 = TuringMachine(tape_input="10", initial_state='q0', final_states={'qf'}, blank_symbol=BLANK, transitions=transitions)
tm6.run()

# Exemplu 7: Acceptat (sir vid) - daca se accepta _ (blank) ca 0^01^0
print("\n=== Testare: '' (sir vid) ===")
tm7 = TuringMachine(tape_input="", initial_state='q0', final_states={'qf'}, blank_symbol=BLANK, transitions=transitions)
tm7.run() # Va fi acceptat, deoarece q0, blank -> qf.