from collections import defaultdict

def find_common_prefix_groups(productions):
    groups = defaultdict(list)
    for prod in productions:
        if not prod or prod == 'ε':
            prefix = 'ε'
        else:
            prefix = prod[0]
        groups[prefix].append(prod)
    return groups

def find_longest_common_prefix(strings):
    """查找一组字符串的最长公共前缀"""
    if not strings:
        return ""
    if len(strings) == 1:
        return strings[0]
    
    min_len = min(len(s) for s in strings)
    for i in range(min_len):
        if not all(s[i] == strings[0][i] for s in strings):
            return strings[0][:i]
    return strings[0][:min_len]

def extract_left_factoring(cfg):
    # 输入检查
    if not cfg or not cfg.strip():
        return {}
    
    grammar = defaultdict(list)
    for production in cfg.split('\n'):
        if not production.strip():
            continue
        try:
            lhs, rhs = production.split(' -> ')
            grammar[lhs.strip()].extend(r.strip() for r in rhs.split(' | '))
        except ValueError:
            continue

    result = defaultdict(list)

    def process_productions(symbol, productions):
        if not productions:
            return
        
        # 按前缀分组
        prefix_groups = find_common_prefix_groups(productions)
        
        for prefix, group in prefix_groups.items():
            if prefix == 'ε':
                result[symbol].append('ε')
                continue
                
            if len(group) == 1:
                result[symbol].append(group[0])
                continue
            
            # 找到最长公共前缀
            common_prefix = find_longest_common_prefix(group)
            if len(common_prefix) > 0:
                new_symbol = f"{symbol}'"
                while new_symbol in result:
                    new_symbol += "'"
                
                # 添加新的产生式规则
                result[symbol].append(f"{common_prefix}{new_symbol}")
                
                # 处理剩余部分
                remainders = []
                for prod in group:
                    remainder = prod[len(common_prefix):]
                    remainders.append(remainder if remainder else 'ε')
                
                # 递归处理剩余部分
                process_productions(new_symbol, remainders)
            else:
                result[symbol].extend(group)

    # 处理每个非终结符的产生式
    for lhs, rhs_list in grammar.items():
        process_productions(lhs, rhs_list)

    return result

# 测试代码
if __name__ == "__main__":
    cfg = """
    S -> apple | apply | application | ball | bat | bath | Xb
    X -> ab | ac | ad
    """

    new_cfg = extract_left_factoring(cfg)

    # 按字典序输出结果
    for lhs, rhs_list in sorted(new_cfg.items()):
        print(f"{lhs} -> {' | '.join(rhs_list)}")