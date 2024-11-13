class CFG:
    def __init__(self, grammar, start_symbol):
        if isinstance(grammar, dict):
            # Grammar is passed as a dictionary, directly assign it to self.grammar
            self.grammar = grammar
        else:
            # Assuming grammar is an already defined Grammar object, we use it directly
            self.grammar = grammar

        self.start_symbol = start_symbol
        self.productions = self.grammar  # Since grammar is already a dictionary, no need for further processing
        self.non_terminals = {key for key in self.productions.keys()}
        self.first_sets = {nt: set() for nt in self.non_terminals}
        self.follow_sets = {nt: set() for nt in self.non_terminals}

    def calculate_first(self):
        # Calculate FIRST sets for all non-terminals
        for non_terminal in self.productions:
            self.first_sets[non_terminal] = self.get_first(non_terminal)
        return self.first_sets

    def get_first(self, non_terminal):
        """Recursively gets the FIRST set for a non-terminal."""
        if non_terminal in self.first_sets and self.first_sets[non_terminal]:
            return self.first_sets[non_terminal]

        first_set = set()

        # Process all productions for this non-terminal
        for production in self.productions[non_terminal]:
            for symbol in production:
                if not self.is_non_terminal(symbol):  # Terminal symbol
                    first_set.add(symbol)
                    break
                else:  # Non-terminal symbol
                    first_set.update(self.get_first(symbol) - {'ε'})
                    if 'ε' not in self.get_first(symbol):
                        break
                    # If 'ε' is in FIRST(symbol), continue with the next symbol

            # If the production could derive ε, add ε to the FIRST set
            if all(self.is_non_terminal(symbol) and 'ε' in self.get_first(symbol) for symbol in production):
                first_set.add('ε')

        self.first_sets[non_terminal] = first_set
        return first_set

    def calculate_follow(self):
        # The FOLLOW set for the start symbol must contain the end-of-input symbol $
        self.follow_sets[self.start_symbol].add('$')
        
        # Iteratively calculate FOLLOW sets for non-terminals
        changed = True
        while changed:
            changed = False
            for head, bodies in self.productions.items():
                for body in bodies:
                    follow_temp = set()
                    for i in range(len(body) - 1, -1, -1):  # Traverse the body from right to left
                        symbol = body[i]
                        if self.is_non_terminal(symbol):
                            follow_size_before = len(self.follow_sets[symbol])
                            # If it's the last symbol, propagate FOLLOW(head) to FOLLOW(symbol)
                            if i == len(body) - 1:
                                self.follow_sets[symbol].update(self.follow_sets[head])
                            else:
                                # Propagate FIRST(symbol[i+1]) to FOLLOW(symbol)
                                next_symbol_first = self.first_sets[body[i + 1]]
                                self.follow_sets[symbol].update(next_symbol_first - {'ε'})
                                # If the next symbol's FIRST contains ε, also add FOLLOW(head)
                                if 'ε' in next_symbol_first:
                                    self.follow_sets[symbol].update(self.follow_sets[head])
                            # If FOLLOW(symbol) has changed, set changed to True
                            if len(self.follow_sets[symbol]) > follow_size_before:
                                changed = True
                        else:
                            break  # If terminal symbol, stop

        return self.follow_sets

    def is_non_terminal(self, symbol):
        """Checks if a symbol is a non-terminal (typically uppercase)"""
        return symbol.isupper()

    def print_sets(self):
        # Sort the non-terminals in lexicographic order
        sorted_non_terminals = sorted(self.first_sets.keys())
        
        print("FIRST集：")
        for non_terminal in sorted_non_terminals:
            print(f"{non_terminal}: {sorted(self.first_sets[non_terminal])}")
        
        print("\nFOLLOW集：")
        for non_terminal in sorted_non_terminals:
            print(f"{non_terminal}: {sorted(self.follow_sets[non_terminal])}")

def main():
    # Test Case 1: Simple Grammar
    productions1 = {
        'S': ['AB'],
        'A': ['aA', 'ε'],
        'B': ['b'],
    }
    start_symbol1 = 'S'
    print("Test Case 1: Simple Grammar")
    cfg1 = CFG(productions1, start_symbol1)
    cfg1.calculate_first()
    cfg1.calculate_follow()
    cfg1.print_sets()
    print("\n" + "="*40 + "\n")

    # Test Case 2: No Recursion Grammar
    productions2 = {
        'S': ['aS', 'b'],
        'A': ['a', 'b'],
    }
    start_symbol2 = 'S'
    print("Test Case 2: No Recursion Grammar")
    cfg2 = CFG(productions2, start_symbol2)
    cfg2.calculate_first()
    cfg2.calculate_follow()
    cfg2.print_sets()
    print("\n" + "="*40 + "\n")

    # Test Case 3: Grammar with Multiple Productions
    productions3 = {
        'S': ['Aa', 'bB'],
        'A': ['a', 'ε'],
        'B': ['b'],
    }
    start_symbol3 = 'S'
    print("Test Case 3: Grammar with Multiple Productions")
    cfg3 = CFG(productions3, start_symbol3)
    cfg3.calculate_first()
    cfg3.calculate_follow()
    cfg3.print_sets()
    print("\n" + "="*40 + "\n")

    # Test Case 4: Grammar with Only Terminals
    productions4 = {
        'S': ['a', 'b'],
    }
    start_symbol4 = 'S'
    print("Test Case 4: Grammar with Only Terminals")
    cfg4 = CFG(productions4, start_symbol4)
    cfg4.calculate_first()
    cfg4.calculate_follow()
    cfg4.print_sets()
    print("\n" + "="*40 + "\n")

    # Test Case 5: Complex Grammar
    productions5 = {
        'S': ['AB'],
        'A': ['aA', 'ε'],
        'B': ['b'],
    }
    start_symbol5 = 'S'
    print("Test Case 5: Complex Grammar")
    cfg5 = CFG(productions5, start_symbol5)
    cfg5.calculate_first()
    cfg5.calculate_follow()
    cfg5.print_sets()
    print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    main()
