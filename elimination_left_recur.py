import sys
import re
from collections import defaultdict, OrderedDict

class Grammar:
    def __init__(self):
        self.productions = OrderedDict()  # 保持插入顺序
        self.nonterminals = []
        self.terminals = set()
    
    def add_production(self, nonterminal, productions):
        if nonterminal not in self.productions:
            self.productions[nonterminal] = []
            self.nonterminals.append(nonterminal)
        for prod in productions:
            symbols = self.parse_production(prod)
            self.productions[nonterminal].append(symbols)
    
    def parse_production(self, prod_str):
        # 分割产生式为符号列表
        # 这里假设符号之间没有空格，可以根据需要调整
        tokens = re.findall(r"[A-Za-z']+|[\(\)\+\*\|ε]", prod_str)
        return tokens
    
    def get_nonterminals_set(self):
        return set(self.nonterminals)
    
    def eliminate_left_recursion(self):
        new_productions = OrderedDict()
        nonterminals = self.nonterminals.copy()
        for i, Ai in enumerate(nonterminals):
            # 替换间接左递归
            for j in range(i):
                Aj = nonterminals[j]
                new_rules = []
                for production in self.productions[Ai]:
                    if production[0] == Aj:
                        # 替换 Aj 的产生式
                        for delta in new_productions[Aj]:
                            new_rule = delta + production[1:]
                            new_rules.append(new_rule)
                    else:
                        new_rules.append(production)
                self.productions[Ai] = new_rules
            # 消除直接左递归
            self.remove_direct_left_recursion(Ai, new_productions)
        self.productions = new_productions
    
    def remove_direct_left_recursion(self, Ai, new_productions):
        alpha = []  # 直接左递归的产生式
        beta = []   # 非左递归的产生式
        for production in self.productions[Ai]:
            if production[0] == Ai:
                alpha.append(production[1:])
            else:
                beta.append(production)
        if alpha:
            # 存在直接左递归
            Ai_prime = Ai + "'"
            while Ai_prime in self.productions or Ai_prime in new_productions:
                Ai_prime += "'"
            self.nonterminals.append(Ai_prime)
            new_productions[Ai] = []
            for b in beta:
                new_productions[Ai].append(b + [Ai_prime])
            new_productions[Ai_prime] = []
            for a in alpha:
                new_productions[Ai_prime].append(a + [Ai_prime])
            new_productions[Ai_prime].append(['ε'])
        else:
            new_productions[Ai] = self.productions[Ai]
    
    def get_all_terminals(self):
        nonterminals_set = self.get_nonterminals_set()
        terminals = set()
        for prods in self.productions.values():
            for prod in prods:
                for symbol in prod:
                    if symbol not in nonterminals_set and symbol != 'ε':
                        terminals.add(symbol)
        self.terminals = terminals
    
    def print_grammar(self):
        # 重新编号产生式
        production_list = []
        for lhs, prods in self.productions.items():
            for prod in prods:
                production_list.append((lhs, prod))
        # 打印编号
        for i in range(1, len(production_list) + 1):
            print(i)
        # 打印产生式
        prod_dict = defaultdict(list)
        for lhs, prod in production_list:
            rhs = ''.join(prod)
            prod_dict[lhs].append(rhs)
        for lhs in self.productions.keys():
            rhs = ' | '.join(prod_dict[lhs])
            print(f"{lhs} -> {rhs}")

def main():
    grammar = Grammar()
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            lines.append(line)
    # 假设生产规则从第四行开始（根据样例输入）
    # 找出所有产生式
    production_lines = []
    for line in lines:
        if '->' in line:
            production_lines.append(line)
    # 添加产生式到文法
    for prod_line in production_lines:
        lhs, rhs = prod_line.split('->')
        lhs = lhs.strip()
        rhs = rhs.strip()
        alternatives = [alt.strip() for alt in rhs.split('|')]
        grammar.add_production(lhs, alternatives)
    # 消除左递归
    grammar.eliminate_left_recursion()
    # 获取终结符
    grammar.get_all_terminals()
    # 打印消除左递归后的文法
    grammar.print_grammar()

if __name__ == "__main__":
    main()
