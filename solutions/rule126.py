def hex_str_to_binary(string):
    return bin(int(string, base=16))[2:]

rules = {
        '111': '0',
        '110': '1',
        '101': '1',
        '100': '1',
        '011': '1',
        '010': '1',
        '001': '1',
        '000': '0'
        }

reverse_rules = {
        '0': ['000', '111'],
        '1': ['001', '010', '011', '100', '101', '110']
        }

def rule_126(step):
    output = ''
    for index, cell in enumerate(step):
        rule = step[index-1] + cell + step[(index+1) % len(step)]
        output += rules[rule]

    return output

def binary_to_hex(string):
    return hex(int(string, base=2))[2:]

def forward_step(string):
    return binary_to_hex(rule_126(hex_str_to_binary(string)))

def reverse_step(string):
    return binary_to_hex(reverse_rule_126(hex_str_to_binary(string)))

def reverse_rule_126(step):
    attempts = [0 for x in range(len(step))]
    output = [None for x in range(len(step))]

    finished = False
    i = 0

    while not finished:
        current = step[i]
        # import pdb; pdb.set_trace()
        potential = reverse_rules[current][attempts[i]]
        print(output)
        if output[i - 1]:
            if output[i-1] == potential[0]:
                if output[i] == potential[1]:
                    if output[(i+1)%len(step)] == potential[2]:
                        finished = True
                        break
                    elif output[(i+1)%len(step)]:
                        if attempts[i] < len(reverse_rules[current]) - 1:
                            attempts[i] += 1
                            continue
                        else:
                            attempts[0] = (attempts[0] + 1)%len(reverse_rules[current])
                            i = 0
                    else:
                        i += 1
                        output[(i+1)%len(step)] = potential[2]
                        continue
                else:
                    if attempts[i] < len(reverse_rules[current]) - 1:
                        attempts[i] += 1
                        continue
                    else:
                        attempts[i] = 0
                        output[i] = None
                        i -= 1
                        attempts[i] = (attempts[i] + 1)%len(reverse_rules[current])
                        if i == 0: output = [None for x in range(len(step))]
                        output[i] = None
                        continue
            else:
                if attempts[i] < len(reverse_rules[current]) - 1:
                    attempts[i] += 1
                    continue
                else:
                    attempts[i] = 0
                    output[i] = None
                    i -= 1
                    attempts[i] = (attempts[i] + 1)%len(reverse_rules[current])
                    if i == 0: output = [None for x in range(len(step))]
                    output[i] = None
                    continue
        else:
            output[i-1] = potential[0]
            output[i] = potential[1]
            output[(i+1)%len(step)] = potential[2]
            i += 1

        if i >= len(step):
            finished = True
