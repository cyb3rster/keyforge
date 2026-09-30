#!/usr/bin/env python3
"""
KeyForge - Smart Personal Wordlist Generator
Advanced CUPP alternative. For ethical/authorized use only.

Usage:
    python keyforge.py
"""

import os
import sys
import random
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

# ─────────────────────────────────────────────
#  COLORS
# ─────────────────────────────────────────────
class C:
    HEADER = '\033[95m'
    BLUE   = '\033[94m'
    CYAN   = '\033[96m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    RED    = '\033[91m'
    BOLD   = '\033[1m'
    DIM    = '\033[2m'
    END    = '\033[0m'

    @staticmethod
    def enable_windows():
        """Windows 10+ pe ANSI colors enable karo."""
        if os.name == 'nt':
            os.system('')  # enables VT100 on Windows 10+

C.enable_windows()


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def ask_field(label, example="", default=""):
    """Clean prompt with example on separate line."""
    print()
    print(f"  {C.CYAN}┌─{C.END} {C.BOLD}{label}{C.END}")
    if example:
        print(f"  {C.CYAN}│{C.END}  {C.DIM}Example: {example}{C.END}")
    try:
        val = input(f"  {C.CYAN}└─>{C.END} ").strip()
    except EOFError:
        return default

    if val.lower() in ('skip', 's', 'none', 'na', 'n/a', 'unknown'):
        return default
    return val if val else default


def ask_yes_no(prompt, default=False):
    marker = 'y' if default else 'n'
    try:
        val = input(f"  {C.YELLOW}?{C.END} {prompt} {C.DIM}(y/n) [{marker}]{C.END}: ").strip().lower()
    except EOFError:
        return default
    if not val:
        return default
    return val in ('y', 'yes', '1', 'true')


def ask_int(prompt, default, min_val=1, max_val=10**9):
    try:
        val = input(f"  {C.YELLOW}?{C.END} {prompt} {C.DIM}[{default}]{C.END}: ").strip()
    except EOFError:
        return default
    if not val:
        return default
    try:
        n = int(val)
        if n < min_val:
            print(f"    {C.RED}[!] Too small, using minimum: {min_val}{C.END}")
            return min_val
        if n > max_val:
            print(f"    {C.RED}[!] Too large, using maximum: {max_val}{C.END}")
            return max_val
        return n
    except ValueError:
        print(f"    {C.RED}[!] Invalid number, using default: {default}{C.END}")
        return default


def section(title):
    print()
    print(f"{C.BLUE}{'━' * 65}{C.END}")
    print(f"{C.BOLD}{C.CYAN}  {title}{C.END}")
    print(f"{C.BLUE}{'━' * 65}{C.END}")


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


# ─────────────────────────────────────────────
#  BANNER
# ─────────────────────────────────────────────
def print_banner():
    print()
    print(f"{C.CYAN}╔{'═' * 63}╗{C.END}")
    print(f"{C.CYAN}║{C.END}  {C.BOLD}{C.HEADER}K E Y F O R G E{C.END}  {C.DIM}─  Smart Wordlist Generator  v1.0.0{C.END}  {C.CYAN}║{C.END}")
    print(f"{C.CYAN}╚{'═' * 63}╝{C.END}")
    print()
    print(f"  {C.YELLOW}⚠{C.END}  For ethical/authorized use only (own accounts / pentest).")
    print(f"  {C.CYAN}💡{C.END} Leave any field empty to SKIP — you'll get a confirmation.")


# ─────────────────────────────────────────────
#  QUESTIONS
# ─────────────────────────────────────────────
def ask_questions():
    print_banner()
    info = {}

    section("BASIC INFO")
    info['first_name'] = ask_field("First name", "ali, ahmed, john")
    info['last_name']  = ask_field("Last name / Surname", "khan, smith, malik")
    info['nickname']   = ask_field("Nickname", "alu, sunny, jr")
    info['username']   = ask_field("Username / Handle", "alikhan92, cool_dev")

    section("DATE OF BIRTH")
    print(f"  {C.DIM}Formats: DDMMYYYY (15081998) | DDMMYY (150898) | YYYY (1998){C.END}")
    dob = ask_field("Date of birth", "15081998 or 150898 or 1998")
    if dob:
        clean = ''.join(c for c in dob if c.isdigit())
        if len(clean) in (4, 6, 8):
            info['dob'] = clean
        else:
            print(f"    {C.RED}[!] Invalid ({len(clean)} digits) — skipped.{C.END}")
            info['dob'] = ""
    else:
        info['dob'] = ""

    section("EXTENDED INFO")
    info['partner'] = ask_field("Partner / Spouse name", "sara, ayesha")
    info['pet']     = ask_field("Pet name", "tommy, kitty")
    info['child']   = ask_field("Child name", "hamza, emma")
    info['city']    = ask_field("City / Hometown", "lahore, karachi")
    info['company'] = ask_field("Company / School", "google, fast_university")
    info['hobby']   = ask_field("Hobby / Interest", "cricket, gaming")
    info['phone_last4'] = ask_field("Phone last 4 digits", "4567, 0000")
    info['vehicle'] = ask_field("Vehicle number", "leB-1234")
    info['extra']   = ask_field("Extra words (comma sep)", "love, admin")

    # Check empty
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
        print(f"\n  {C.RED}[!] You left EVERYTHING empty. Cannot generate a wordlist.{C.END}")
        sys.exit(1)

    # Confirmation
    section("CONFIRMATION")
    print(f"  {C.GREEN}✓ Filled :{C.END} {', '.join(filled)}")
    if empty:
        print(f"  {C.YELLOW}✗ Skipped:{C.END} {', '.join(empty)}")
        print()
        print(f"  {C.YELLOW}You left {len(empty)} field(s) EMPTY. They will be skipped.{C.END}")
        if not ask_yes_no("Run with these skips?", default=True):
            print(f"\n  {C.RED}[!] Aborted.{C.END}")
            sys.exit(0)
    else:
        print(f"  {C.GREEN}✗ Skipped:{C.END} (none)")
        if not ask_yes_no("All fields filled. Proceed?", default=True):
            print(f"\n  {C.RED}[!] Aborted.{C.END}")
            sys.exit(0)

    # Generation Options
    section("GENERATION OPTIONS")

    print(f"  {C.DIM}• Leetspeak : ali → 4l1, @li{C.END}")
    info['use_leet'] = ask_yes_no("Enable leetspeak?", True)

    print(f"  {C.DIM}• Reverse   : ali → ila{C.END}")
    info['add_reverse'] = ask_yes_no("Add reversed words?", True)

    print(f"  {C.DIM}• South Asian: 786, Allah, Khan{C.END}")
    info['south_asian'] = ask_yes_no("Add South Asian patterns?", True)

    section("PASSWORD LENGTH")
    info['min_len'] = ask_int("Minimum password length", 6, 1, 100)
    info['max_len'] = ask_int("Maximum password length", 25, 1, 100)
    if info['min_len'] > info['max_len']:
        print(f"  {C.RED}[!] Min > Max. Swapping.{C.END}")
        info['min_len'], info['max_len'] = info['max_len'], info['min_len']

    section("OUTPUT SETTINGS")
    info['max_size'] = ask_int("Max passwords to generate", 200000, 1, 50000000)
    info['output'] = ask_field("Output file", "wordlist.txt") or "wordlist.txt"

    return info


# ─────────────────────────────────────────────
#  BUILD TOKENS (USER FIRST, THEN PATTERNS)
# ─────────────────────────────────────────────
def build_tokens(info):
    """
    Priority-based token building:
    1. User input tokens (names, DOB, city, etc.) — HIGHEST priority
    2. Leetspeak variants of user tokens
    3. Combined user tokens
    4. South Asian patterns — LOWEST priority
    """
    user_tokens = []      # ordered — user input
    pattern_tokens = []   # ordered — South Asian

    # ── 1. User input tokens (in order)
    name_keys = ['first_name', 'last_name', 'nickname', 'username',
                 'partner', 'pet', 'child', 'city', 'company', 'hobby']
    for key in name_keys:
        val = (info.get(key) or '').strip()
        if val:
            for v in case_variations(val):
                if v and len(v) >= 2:
                    user_tokens.append(v)

    # ── 2. Full name combos
    fn = (info.get('first_name') or '').lower()
    ln = (info.get('last_name') or '').lower()
    un = (info.get('username') or '').lower()

    if fn and ln:
        user_tokens.extend([fn+ln, fn+'_'+ln, fn+'.'+ln,
                            fn[0]+ln, ln+fn, ln[0]+fn])
    if fn and un:
        user_tokens.extend([fn+un, un+fn])

    # ── 3. DOB variations
    dob = info.get('dob', '')
    if dob:
        user_tokens.append(dob)
        if len(dob) == 8:
            d, m, y = dob[:2], dob[2:4], dob[4:]
            user_tokens.extend([d+m, d+m+y, d+m+y[2:],
                                y+m+d, y[2:]+m+d, m+d+y, y])
        elif len(dob) == 6:
            d, m, y = dob[:2], dob[2:4], dob[4:]
            user_tokens.extend([d+m+y, y+m+d, d+m, y])
        elif len(dob) == 4:
            user_tokens.append(dob)

    # ── 4. Phone last 4
    ph = info.get('phone_last4', '')
    if ph:
        user_tokens.extend([ph, ph[::-1]])

    # ── 5. Vehicle
    veh = info.get('vehicle', '')
    if veh:
        for v in case_variations(veh):
            user_tokens.append(v)

    # ── 6. Extra words
    extra = info.get('extra', '')
    if extra:
        for w in extra.split(','):
            w = w.strip()
            if w:
                for v in case_variations(w):
                    user_tokens.append(v)

    # Deduplicate user tokens (keep order)
    seen = set()
    user_tokens = [t for t in user_tokens
                   if t and len(t) >= 2 and not (t in seen or seen.add(t))]

    # ── 7. Leetspeak expansion (based on user tokens)
    if info.get('use_leet'):
        leet_tokens = []
        for t in user_tokens:
            if t.isalpha() and 2 <= len(t) <= 10:
                leet_tokens.extend(leet_variations(t, max_variants=10))
        # dedupe leet
        leet_seen = set()
        leet_tokens = [t for t in leet_tokens
                       if not (t in leet_seen or leet_seen.add(t))]
        user_tokens = user_tokens + leet_tokens

    # ── 8. South Asian patterns (LOWEST priority)
    if info.get('south_asian'):
        for pattern in SOUTH_ASIAN_PATTERNS:
            pattern_tokens.append(pattern)
            pattern_tokens.append(pattern.capitalize())

    # FINAL ORDER: user first, patterns last
    return user_tokens, pattern_tokens


# ─────────────────────────────────────────────
#  GENERATE
# ─────────────────────────────────────────────
def generate_wordlist(info):
    user_tokens, pattern_tokens = build_tokens(info)

    if not user_tokens and not pattern_tokens:
        return []

    print()
    print(f"  {C.CYAN}[*]{C.END} User tokens  : {C.BOLD}{len(user_tokens)}{C.END}")
    print(f"  {C.CYAN}[*]{C.END} Pattern tokens: {C.BOLD}{len(pattern_tokens)}{C.END}")
    print(f"  {C.CYAN}[*]{C.END} Length range : {C.BOLD}{info['min_len']}-{info['max_len']}{C.END} chars")
    print(f"  {C.CYAN}[*]{C.END} Generating combinations...")
    print()

    max_size = info['max_size']
    min_len = info['min_len']
    max_len = info['max_len']

    passwords = []
    seen = set()

    def add(pw):
        if not pw:
            return False
        if not (min_len <= len(pw) <= max_len):
            return False
        if pw in seen:
            return False
        seen.add(pw)
        passwords.append(pw)
        return True

    # ── Phase 1: User tokens + numbers + specials (HIGH PRIORITY)
    # Iterate numbers/specials in natural order so short & common ones come first
    for t in user_tokens:
        for n in COMMON_NUMBERS:
            for s in COMMON_SPECIALS:
                if add(f"{t}{n}{s}"):
                    if len(passwords) >= max_size:
                        break
            if len(passwords) >= max_size:
                break
        if len(passwords) >= max_size:
            break

    # ── Phase 2: User token pairs
    if len(passwords) < max_size:
        for a in user_tokens:
            for b in user_tokens:
                if a == b:
                    continue
                for n in ['', '1', '123', '786']:
                    for s in ['', '@', '_', '.']:
                        if add(f"{a}{s}{b}{n}"):
                            if len(passwords) >= max_size:
                                break
                    if len(passwords) >= max_size:
                        break
                if len(passwords) >= max_size:
                    break
            if len(passwords) >= max_size:
                break

    # ── Phase 3: Capitalize
    if len(passwords) < max_size:
        for p in list(passwords):
            if p and p[0].islower():
                add(p.capitalize())
            if len(passwords) >= max_size:
                break

    # ── Phase 4: Reverse
    if info.get('add_reverse') and len(passwords) < max_size:
        for p in list(passwords):
            add(p[::-1])
            if len(passwords) >= max_size:
                break

    # ── Phase 5: South Asian patterns (LOW PRIORITY)
    if len(passwords) < max_size and pattern_tokens:
        for t in pattern_tokens:
            for n in COMMON_NUMBERS:
                for s in COMMON_SPECIALS:
                    if add(f"{t}{n}{s}"):
                        if len(passwords) >= max_size:
                            break
                if len(passwords) >= max_size:
                    break
            if len(passwords) >= max_size:
                break

    passwords = passwords[:max_size]
    print(f"  {C.GREEN}[✓]{C.END} Total passwords generated: {C.BOLD}{len(passwords)}{C.END}")
    return passwords


# ─────────────────────────────────────────────
#  SAVE
# ─────────────────────────────────────────────
def save_wordlist(passwords, output_file):
    # Add .txt if no extension given
    if not os.path.splitext(output_file)[1]:
        output_file += '.txt'

    with open(output_file, 'w', encoding='utf-8') as f:
        for p in passwords:
            f.write(p + '\n')

    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"  {C.GREEN}[✓]{C.END} Saved: {C.BOLD}{os.path.abspath(output_file)}{C.END}")
    print(f"  {C.GREEN}[✓]{C.END} Size : {size_mb:.2f} MB")
    return output_file


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    try:
        info = ask_questions()
        passwords = generate_wordlist(info)
        if passwords:
            save_wordlist(passwords, info['output'])
            print()
            print(f"{C.GREEN}{'═' * 65}{C.END}")
            print(f"  {C.BOLD}{C.GREEN}✅ KeyForge complete! Wordlist ready.{C.END}")
            print(f"{C.GREEN}{'═' * 65}{C.END}")
            print()
        else:
            print(f"\n  {C.RED}[!] No passwords generated.{C.END}")
    except KeyboardInterrupt:
        print(f"\n\n  {C.RED}[!] Cancelled.{C.END}")
        sys.exit(0)


if __name__ == "__main__":
    main()
