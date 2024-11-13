from collections import defaultdict

class CFG:
    def __init__(self, grammar, start_symbol):
        self.grammar = grammar
        self.start_symbol = start_symbol
        self.productions = grammar
        self.first_sets = defaultdict(set)
        self.follow_sets = defaultdict(set)
    
    def calculate_first(self):
        for non_terminal in self.productions:
            self.first_sets[non_terminal] = self.get_first(non_terminal)
    
    def get_first(self, non_terminal):
        if non_terminal in self.first_sets and self.first_sets[non_terminal]:
            return self.first_sets[non_terminal]
        
        first_set = set()
        for production in self.productions[non_terminal]:
            for symbol in production:
                if not self.is_non_terminal(symbol):  # Terminal symbol
                    first_set.add(symbol)
                    break
                else:  # Non-terminal symbol
                    first_set.update(self.get_first(symbol) - {'ε'})
                    if 'ε' not in self.get_first(symbol):
                        break
            if all(self.is_non_terminal(symbol) and 'ε' in self.get_first(symbol) for symbol in production):
                first_set.add('ε')
        
        self.first_sets[non_terminal] = first_set
        return first_set

    def calculate_follow(self):
        self.follow_sets[self.start_symbol].add('$')
        changed = True
        while changed:
            changed = False
            for head, bodies in self.productions.items():
                for body in bodies:
                    for i in range(len(body) - 1, -1, -1):
                        symbol = body[i]
                        if self.is_non_terminal(symbol):
                            follow_size_before = len(self.follow_sets[symbol])
                            if i == len(body) - 1:
                                self.follow_sets[symbol].update(self.follow_sets[head])
                            else:
                                next_symbol_first = self.first_sets[body[i + 1]]
                                self.follow_sets[symbol].update(next_symbol_first - {'ε'})
                                if 'ε' in next_symbol_first:
                                    self.follow_sets[symbol].update(self.follow_sets[head])
                            if len(self.follow_sets[symbol]) > follow_size_before:
                                changed = True
        return self.follow_sets
    
    def is_non_terminal(self, symbol):
        return symbol.isupper()

    def build_parsing_table(self):
        table = defaultdict(lambda: defaultdict(str))
        for non_terminal, productions in self.productions.items():
            for production in productions:
                first_prod = self.get_first_of_production(production)
                for terminal in first_prod:
                    if terminal != 'ε':
                        table[non_terminal][terminal] = production
                if 'ε' in first_prod:
                    for terminal in self.follow_sets[non_terminal]:
                        if terminal != '$':
                            table[non_terminal][terminal] = production
                    if '$' in self.follow_sets[non_terminal]:
                        table[non_terminal]['$'] = production
        return table

    def get_first_of_production(self, production):
        first_prod = set()
        for symbol in production:
            if not self.is_non_terminal(symbol):  # Terminal
                first_prod.add(symbol)
                break
            else:
                first_prod.update(self.first_sets[symbol] - {'ε'})
                if 'ε' not in self.first_sets[symbol]:
                    break
        if all(self.is_non_terminal(symbol) and 'ε' in self.first_sets[symbol] for symbol in production):
            first_prod.add('ε')
        return first_prod

    def print_sets(self):
        # Print the FIRST sets
        print("FIRST sets:")
        for non_terminal in sorted(self.first_sets):
            print(f"{non_terminal}: {sorted(self.first_sets[non_terminal])}")
        
        # Print the FOLLOW sets
        print("\nFOLLOW sets:")
        for non_terminal in sorted(self.follow_sets):
            print(f"{non_terminal}: {sorted(self.follow_sets[non_terminal])}")
    
    def print_parsing_table(self):
        table = self.build_parsing_table()
        print("\nPredictive Parsing Table:")
        terminals = sorted(set(t for rules in table.values() for t in rules.keys()))
        non_terminals = sorted(self.productions.keys())
        print(f"       {'    '.join(terminals)}")
        for non_terminal in non_terminals:
            row = [non_terminal] + [table[non_terminal].get(t, '') for t in terminals]
            print(f"{row[0]:<10} {'  '.join(row[1:])}")

    def parse(self, input_string):
        stack = [self.start_symbol]
        input_list = list(input_string) + ['$']  # Add the end-of-input symbol
        print(f"Parsing input: {input_string}")
        
        while stack:
            top = stack.pop()
            current_input = input_list[0]
            
            print(f"Stack: {stack}")
            print(f"Input: {input_list}")
            
            if top == current_input:  # Terminal symbol matches input
                print(f"Match: {top}")
                input_list.pop(0)  # Move to the next input symbol
            elif self.is_non_terminal(top):  # Non-terminal symbol
                table = self.build_parsing_table()
                if current_input in table[top]:
                    production = table[top][current_input]
                    print(f"Expanding: {top} -> {production}")
                    # Push the right-hand side of the production to the stack in reverse order
                    for symbol in reversed(production):
                        if symbol != 'ε':  # Don't push epsilon
                            stack.append(symbol)
                else:
                    print("Error: No matching production found")
                    return False
            else:
                print("Error: Stack and input symbol mismatch")
                return False
        
        if not input_list:
            print("Parsing successful")
            return True
        else:
            print("Error: Input not fully consumed")
            return False

def main():
    # Define the grammar
    productions = {
        'S': ['AB'],
        'A': ['aA', 'ε'],
        'B': ['b'],
    }
    start_symbol = 'S'
    cfg = CFG(productions, start_symbol)
    
    # Calculate FIRST and FOLLOW sets
    cfg.calculate_first()
    cfg.calculate_follow()

    # Print FIRST and FOLLOW sets
    cfg.print_sets()

    # Build the predictive parsing table
    cfg.print_parsing_table()

    # Parse the input string
    input_string = "ab"
    cfg.parse(input_string)

if __name__ == "__main__":
    main()
