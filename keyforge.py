#!/usr/bin/env python3
"""
KeyForge - Smart Personal Wordlist Generator
Advanced CUPP alternative. For ethical/authorized use only.

Usage:
    python keyforge.py
"""

import os
import sys
import itertools

# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────
LEET_MAP = {
    'a': ['a', '4', '@'], 'b': ['b', '8'], 'e': ['e', '3'],
    'g': ['g', '9', '6'], 'i': ['i', '1', '!'], 'l': ['l', '1', '|'],
    'o': ['o', '0'], 's': ['s', '5', '$'], 't': ['t', '7'],
    'z': ['z', '2'], 'c': ['c', '('], 'd': ['d', '|)'],
}

COMMON_NUMBERS = [
    '', '1', '12', '123', '1234', '12345', '123456', '1234567',
    '007', '69', '99', '111', '000', '786', '143', '420',
    '2020', '2021', '2022', '2023', '2024', '2025', '2026',
]

COMMON_SPECIALS = ['', '!', '@', '#', '$', '.', '_', '-', '?', '*', '+']

SOUTH_ASIAN_PATTERNS = [
    '786', '143', '420', '007', '000',
    'allah', 'ali', 'hussain', 'raza', 'haider',
    'khan', 'malik', 'butt', 'chaudhry', 'sheikh',
    'gujjar', 'rajput', 'memon', 'ansari', 'qureshi',
]


def ask(prompt, example="", default=""):
    if example:
        print(f"    \u2514\u2500 Example: {example}")
    val = input(prompt).strip()
    if val.lower() in ('skip', 's', 'none', 'na', 'n/a', 'unknown'):
        return default
    return val if val else default


def ask_yes_no(prompt, default=False):
    marker = 'y' if default else 'n'
    val = input(f"{prompt} (y/n) [{marker}]: ").strip().lower()
    if not val:
        return default
    return val in ('y', 'yes', '1', 'true')


def case_variations(word):
    if not word:
        return []
    return [word.lower(), word.capitalize(), word.upper(), word[::-1]]


def leet_variations(word, max_variants=15):
    word = word.lower()
    choices = [LEET_MAP.get(ch, [ch]) for ch in word]
    variants = set()
    for combo in itertools.product(*choices):
        variants.add(''.join(combo))
        if len(variants) >= max_variants:
            break
    return list(variants)


def ask_questions():
    print("\n" + "=" * 65)
    print("   K E Y F O R G E   -   Wordlist Generator")
    print("=" * 65)
    print("\u26a0\ufe0f  For ethical/authorized use only (own accounts / pentest).")
    print("\U0001f4a1 Leave any field empty to SKIP it \u2014 you'll get a confirmation.\n")

    info = {}

    print("\u2500\u2500 BASIC INFO \u2500\u2500")
    info['first_name'] = ask("[?] First name              : ", "ali, ahmed, john")
    info['last_name']  = ask("[?] Last name / Surname     : ", "khan, smith, malik")
    info['nickname']   = ask("[?] Nickname                : ", "alu, sunny, jr")
    info['username']   = ask("[?] Username / Handle       : ", "alikhan92, cool_dev")

    print("\n\u2500\u2500 DATE OF BIRTH \u2500\u2500")
    print("    Formats: DDMMYYYY (15081998) | DDMMYY (150898) | YYYY (1998)")
    dob = ask("[?] Date of birth           : ", "15081998 or 150898 or 1998")
    if dob:
        clean = ''.join(c for c in dob if c.isdigit())
        if len(clean) in (4, 6, 8):
            info['dob'] = clean
        else:
            print(f"    [!] Invalid ({len(clean)} digits) \u2014 skipped.")
            info['dob'] = ""
    else:
        info['dob'] = ""

    print("\n\u2500\u2500 EXTENDED INFO \u2500\u2500")
    info['partner']  = ask("[?] Partner/Spouse name     : ", "sara, ayesha")
    info['pet']      = ask("[?] Pet name                : ", "tommy, kitty")
    info['child']    = ask("[?] Child name              : ", "hamza, emma")
    info['city']     = ask("[?] City / Hometown         : ", "lahore, karachi")
    info['company']  = ask("[?] Company / School        : ", "google, fast_university")
    info['hobby']    = ask("[?] Hobby / Interest        : ", "cricket, gaming")
    info['phone_last4'] = ask("[?] Phone last 4 digits     : ", "4567, 0000")
    info['vehicle']  = ask("[?] Vehicle number          : ", "leB-1234")
    info['extra']    = ask("[?] Extra words (comma sep) : ", "love, admin")

    all_fields = [
        ('first_name', 'First name'), ('last_name', 'Last name'),
        ('nickname', 'Nickname'), ('username', 'Username'),
        ('dob', 'Date of birth'), ('partner', 'Partner name'),
        ('pet', 'Pet name'), ('child', 'Child name'),
        ('city', 'City'), ('company', 'Company/School'),
        ('hobby', 'Hobby'), ('phone_last4', 'Phone last 4'),
        ('vehicle', 'Vehicle number'), ('extra', 'Extra words'),
    ]
    empty = [label for key, label in all_fields if not info.get(key)]
    filled = [label for key, label in all_fields if info.get(key)]

    if not filled:
        print("\n[!] You left EVERYTHING empty. Cannot generate a wordlist.")
        sys.exit(1)

    print("\n" + "=" * 65)
    print("  CONFIRMATION")
    print("=" * 65)
    print(f"  \u2713 Filled : {', '.join(filled)}")
    if empty:
        print(f"  \u2717 Skipped: {', '.join(empty)}")
    else:
        print("  \u2717 Skipped: (none)")

    if empty:
        print(f"\n  You left {len(empty)} field(s) EMPTY. They will be skipped.")
        if not ask_yes_no("  Run with these skips?", default=True):
            print("\n[!] Aborted.")
            sys.exit(0)
    else:
        if not ask_yes_no("  All fields filled. Proceed?", default=True):
            print("\n[!] Aborted.")
            sys.exit(0)

    print("\n" + "-" * 65)
    print("  GENERATION OPTIONS")
    print("-" * 65)
    print("    \u2022 Leetspeak : ali \u2192 4l1, @li")
    info['use_leet'] = ask_yes_no("[?] Enable leetspeak?", True)
    print("    \u2022 Reverse   : ali \u2192 ila")
    info['add_reverse'] = ask_yes_no("[?] Add reversed words?", True)
    print("    \u2022 South Asian: 786, Allah, Khan")
    info['south_asian'] = ask_yes_no("[?] Add South Asian patterns?", True)

    size_str = ask("[?] Max passwords           : ", "200000", "200000")
    try:
        info['max_size'] = int(size_str)
    except ValueError:
        info['max_size'] = 200000

    info['output'] = ask("[?] Output file             : ", "wordlist.txt", "wordlist.txt")
    if not info['output']:
        info['output'] = "wordlist.txt"

    return info


def build_tokens(info):
    tokens = set()
    name_keys = ['first_name', 'last_name', 'nickname', 'username',
                 'partner', 'pet', 'child', 'city', 'company', 'hobby']
    for key in name_keys:
        val = (info.get(key) or '').strip()
        if val:
            for v in case_variations(val):
                tokens.add(v)

    fn = (info.get('first_name') or '').lower()
    ln = (info.get('last_name') or '').lower()
    un = (info.get('username') or '').lower()

    if fn and ln:
        tokens.update([fn+ln, fn+'_'+ln, fn+'.'+ln, fn[0]+ln, ln+fn, ln[0]+fn])
    if fn and un:
        tokens.update([fn+un, un+fn])

    dob = info.get('dob', '')
    if dob:
        tokens.add(dob)
        if len(dob) == 8:
            d, m, y = dob[:2], dob[2:4], dob[4:]
            tokens.update([d+m, d+m+y, d+m+y[2:], y+m+d, y[2:]+m+d, m+d+y, y])
        elif len(dob) == 6:
            d, m, y = dob[:2], dob[2:4], dob[4:]
            tokens.update([d+m+y, y+m+d, d+m, y])
        elif len(dob) == 4:
            tokens.add(dob)

    ph = info.get('phone_last4', '')
    if ph:
        tokens.update([ph, ph[::-1]])

    veh = info.get('vehicle', '')
    if veh:
        for v in case_variations(veh):
            tokens.add(v)

    extra = info.get('extra', '')
    if extra:
        for w in extra.split(','):
            w = w.strip()
            if w:
                for v in case_variations(w):
                    tokens.add(v)

    if info.get('south_asian'):
        for pattern in SOUTH_ASIAN_PATTERNS:
            tokens.update([pattern, pattern.capitalize()])

    return [t for t in tokens if t and len(t) >= 2]


def generate_wordlist(info):
    tokens = build_tokens(info)
    max_size = info['max_size']
    if not tokens:
        return []

    if info.get('use_leet'):
        leet_set = set()
        for t in tokens:
            if t.isalpha() and 2 <= len(t) <= 10:
                leet_set.update(leet_variations(t, max_variants=15))
        tokens = list(set(tokens) | leet_set)

    print(f"\n[*] Base tokens: {len(tokens)}")
    print("[*] Generating combinations...")

    passwords = set()

    for t in tokens:
        for n in COMMON_NUMBERS:
            for s in COMMON_SPECIALS:
                passwords.add(f"{t}{n}{s}")
                if len(passwords) >= max_size:
                    break
            if len(passwords) >= max_size:
                break
        if len(passwords) >= max_size:
            break

    if len(passwords) < max_size:
        for a, b in itertools.product(tokens, repeat=2):
            if a == b:
                continue
            for n in ['', '1', '123', '786']:
                for s in ['', '@', '_', '.']:
                    passwords.add(f"{a}{s}{b}{n}")
                    if len(passwords) >= max_size:
                        break
                if len(passwords) >= max_size:
                    break
            if len(passwords) >= max_size:
                break

    if len(passwords) < max_size:
        cap_set = set()
        for p in list(passwords)[:max_size // 2]:
            if p and p[0].islower():
                cap_set.add(p.capitalize())
        passwords.update(cap_set)

    if info.get('add_reverse') and len(passwords) < max_size:
        rev_set = set()
        for p in list(passwords)[:max_size // 3]:
            rev_set.add(p[::-1])
        passwords.update(rev_set)

    passwords = list(passwords)[:max_size]
    print(f"[\u2713] Total passwords generated: {len(passwords)}")
    return passwords


def save_wordlist(passwords, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for p in passwords:
            f.write(p + '\n')
    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"[\u2713] Saved: {os.path.abspath(output_file)}")
    print(f"[\u2713] Size: {size_mb:.2f} MB")


def main():
    try:
        info = ask_questions()
        passwords = generate_wordlist(info)
        if passwords:
            save_wordlist(passwords, info['output'])
            print("\n" + "=" * 65)
            print("  \u2705 KeyForge complete! Wordlist ready.")
            print("=" * 65)
        else:
            print("\n[!] No passwords generated.")
    except KeyboardInterrupt:
        print("\n\n[!] Cancelled.")
        sys.exit(0)


if __name__ == "__main__":
    main()
