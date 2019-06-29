import pdb
import subprocess
import sys

import rule126

def attempt(key):
    hex_key = hex(int(key, 2))[2:]
    cmd1 = f'echo "{hex_key}" > /tmp/plain.key; xxd -r -p /tmp/plain.key > /tmp/enc.key'
    cmd2 = 'echo "U2FsdGVkX1/andRK+WVfKqJILMVdx/69xjAzW4KUqsjr98GqzFR793lfNHrw1Blc8UZHWOBrRhtLx3SM38R1MpRegLTHgHzf0EAa3oUeWcQ=" | openssl enc -d -aes-256-cbc -pbkdf2 -md sha1 -base64 --pass file:/tmp/enc.key'
    subprocess.call(cmd1, shell=True)
    return subprocess.call(cmd2, shell=True)

FORM = list("xooooooooooxxoooooxxooooooooooxxxxxooooooxxxxxxxoooxxxxxooooxxx")

# takes a number between 0 and 63
def populate_zeros(variant):
    population = [int(x) for x in bin(variant)[2:].zfill(6)]

    last = "x"
    group = 0
    group_count = 0
    output = FORM[::]
    for index, current in enumerate(FORM):
        if current == "o":
            output[index] = population[group]
            if (group == 0 and group_count >= 4 and group_count <= 6) or (group == 2 and group_count >= 7):
                output[index] = 1 - output[index]
            group_count += 1
        else:
            if last == "o":
                group += 1
                group_count = 0
        last = current

    return output

def fill_certain_ones(step):
    output = step[::]
    for i, x in enumerate(step):
        if x == 'x':
            if (not isinstance(step[i-1], str)) and (step[i-2] == step[i-1] or step[i-1] == step[(i+1)%63]):
                output[i] = 1 - step[i-1]
            elif (not isinstance(step[(i+1)%63], str)) and step[(i+1)%63] == step[(i+2)%63]:
                output[i] = 1 - step[(i+1)%63]
    return output

# number between 0 and 8192
def populate_ones(variant, step):
    population = [int(x) for x in bin(variant)[2:].zfill(13)]
    output = step
    group = 0
    for i, x in enumerate(step):
        if x == 'x':
            output[i] = population[group]
            group += 1
    return output

desired = '110011011011110001111000001101111111000011111111101111111001111'

def matching_digits(key):
    count = 0
    for a, b in zip(key, desired):
        if a == b:
            count += 1
        else:
            break
    return count

def main():
    answers = []
    for i in range(0,64):
        most = fill_certain_ones(populate_zeros(i))
        for j in range(8192):
            key = ''.join(str(x) for x in populate_ones(j, fill_certain_ones(most)))
            hexkey = hex(int(key, 2))[2:]
            forward = rule126.rule_126(key)
            forward_hex = rule126.binary_to_hex(forward)
            if forward_hex == '66de3c1bf87fdfcf':
                print(hexkey)
                if attempt(key) == 0:
                    answers.append(hexkey)
                    print("Key: ", hexkey, "variants:", i, j)
    return answers

if __name__ == "__main__":
    x = main()
    print(x)

# 3c73e7f12fcd767a
