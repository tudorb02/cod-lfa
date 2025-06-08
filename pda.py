import collections

class PDA:
    def __init__(self, states, input_alphabet, stack_alphabet, transitions,
                 initial_state, initial_stack_symbol, final_states):
        self.states = states
        self.input_alphabet = input_alphabet
        self.stack_alphabet = stack_alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.initial_stack_symbol = initial_stack_symbol
        self.final_states = final_states

    def accepta(self, input_string):
        q = collections.deque()
        
        initial_stack = [self.initial_stack_symbol] 
        q.append((self.initial_state, 0, initial_stack))

        visited_configs = set() 

        print(f"Rulare PDA pentru '{input_string}'")

        while q:
            current_state, input_idx, current_stack = q.popleft()

            config_tuple = (current_state, input_idx, tuple(current_stack)) 
            if config_tuple in visited_configs:
                continue 
            visited_configs.add(config_tuple)

            if input_idx == len(input_string) and current_state in self.final_states and len(current_stack) == 1 and current_stack[0] == self.initial_stack_symbol:
                print(f"Sir '{input_string}' ACCEPTAT (stare finala si stiva goala).")
                return True
            
            top_stack_symbol = current_stack[-1] if current_stack else None 

            epsilon_transitions = self.transitions.get((current_state, None, top_stack_symbol), [])
            for next_state_eps, push_string_eps in epsilon_transitions:
                new_stack_eps = list(current_stack) 
                if push_string_eps == '': 
                    if new_stack_eps:
                        new_stack_eps.pop()
                    else: 
                        continue 
                else:
                    if new_stack_eps: 
                        new_stack_eps.pop()
                    new_stack_eps.extend(list(push_string_eps)) 

                q.append((next_state_eps, input_idx, new_stack_eps))

            if input_idx < len(input_string):
                current_input_symbol = input_string[input_idx]
                
                transitions_for_symbol = self.transitions.get((current_state, current_input_symbol, top_stack_symbol), [])

                for next_state_sym, push_string_sym in transitions_for_symbol:
                    new_stack_sym = list(current_stack) 
                    if push_string_sym == '': 
                        if new_stack_sym:
                            new_stack_sym.pop()
                        else: 
                            continue
                    else:
                        if new_stack_sym: 
                            new_stack_sym.pop()
                        new_stack_sym.extend(list(push_string_sym)) 

                    
                    q.append((next_state_sym, input_idx + 1, new_stack_sym))
        
        print(f"Sir '{input_string}' RESPINS ")
        return False

#Exemplu de utilizare: PDA pentru limbajul {a^n b^n | n >= 0}
# Accepta prin stare finala si stiva goala (doar Z0 ramâne)

# Stari:
# q0: Citim 'a', push 'A'
# q1: Citim 'b', pop 'A'
# q2: Stare finala de acceptare (dupa ce s-au potrivit 'a' si 'b' si stiva e goala)

# Alfabet de intrare: {'a', 'b'}
# Alfabet de stiva: {'A', 'Z0'} - 'Z0' e simbolul de baza al stivei

states = {'q0', 'q1', 'q2'}
input_alphabet = {'a', 'b'}
stack_alphabet = {'A', 'Z0'}
initial_state = 'q0'
initial_stack_symbol = 'Z0'
final_states = {'q2'}

transitions = {
    # Starea q0: Proceseaza 'a'
    # (q0, a, Z0) -> (q0, AZ0) : Daca e 'a' si Z0 e pe stiva, impinge A peste Z0
    ('q0', 'a', 'Z0'): [('q0', 'AZ0')], 
    # (q0, a, A) -> (q0, AA) : Daca e 'a' si A e pe stiva, impinge alt A peste
    ('q0', 'a', 'A'): [('q0', 'AA')], 
    
    # Starea q0 sau q1: Trecere la starea q1 când întâlnesti primul 'b' (poate fi si epsilon)
    # (q0, b, A) -> (q1, '') : Daca e 'b' si A e pe stiva, treci la q1 si scoate A (pop)
    ('q0', 'b', 'A'): [('q1', '')], 
    
    # Starea q1: Proceseaza 'b'
    # (q1, b, A) -> (q1, '') : Daca e 'b' si A e pe stiva, scoate A (pop)
    ('q1', 'b', 'A'): [('q1', '')], 

    # Starea q1: Trecere la starea finala q2 (epsilon tranziție)
    # Când ai terminat de citit 'b' si stiva conține doar Z0
    # (q1, None, Z0) -> (q2, Z0) : Daca ai terminat inputul (None) si stiva e Z0, treci la q2, lasa Z0 pe stiva
    ('q1', None, 'Z0'): [('q2', 'Z0')] 
}

pda = PDA(states, input_alphabet, stack_alphabet, transitions,
          initial_state, initial_stack_symbol, final_states)

print("\n=== Testare: a^n b^n ===")
print(f"Sir 'aabb': {pda.accepta('aabb')}") # True
print(f"Sir 'aaabbb': {pda.accepta('aaabbb')}") # True
print(f"Sir 'ab': {pda.accepta('ab')}") #  True
print(f"Sir '': {pda.accepta('')}") # True
print(f"Sir 'a': {pda.accepta('a')}") # False
print(f"Sir 'b': {pda.accepta('b')}") # False
print(f"Sir 'aaab': {pda.accepta('aaab')}") # False
print(f"Sir 'aabbb': {pda.accepta('aabbb')}") # False
print(f"Sir 'aba': {pda.accepta('aba')}") # False