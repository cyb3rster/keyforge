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
        if os.name == 'nt':
            os.system('')

C.enable_windows()


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def split_values(raw):
    """Split comma-separated values, strip, dedupe."""
    if not raw:
        return []
    parts = [p.strip() for p in raw.split(',')]
    seen = set()
    result = []
    for p in parts:
        if p and p.lower() not in seen:
            seen.add(p.lower())
            result.append(p)
    return result


def ask_field(label, example="", default=""):
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
            return min_val
        if n > max_val:
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
    """Saare case variations."""
    if not word:
        return []
    variants = [word.lower(), word.capitalize(), word.upper()]
    # Title case bhi agar multi-word
    if ' ' in word:
        variants.append(word.title())
    # Reverse
    variants.append(word[::-1])
    return variants


def leet_variations(word, max_variants=20):
    """Leetspeak variants (limited)."""
    word = word.lower()
    choices = [LEET_MAP.get(ch, [ch]) for ch in word]
    variants = set()
    for combo in itertools.product(*choices):
        variants.add(''.join(combo))
        if len(variants) >= max_variants:
            break
    return list(variants)


def print_banner():
    print()
    print(f"{C.CYAN}╔{'═' * 63}╗{C.END}")
    print(f"{C.CYAN}║{C.END}  {C.BOLD}{C.HEADER}K E Y F O R G E{C.END}  {C.DIM}─  Smart Wordlist Generator  v1.0.0{C.END}  {C.CYAN}║{C.END}")
    print(f"{C.CYAN}╚{'═' * 63}╝{C.END}")
    print()
    print(f"  {C.YELLOW}⚠{C.END}  For ethical/authorized use only (own accounts / pentest).")
    print(f"  {C.CYAN}💡{C.END} Leave any field empty to SKIP.")
    print(f"  {C.CYAN}💡{C.END} Use commas to add multiple values: {C.BOLD}lahore, karachi, london{C.END}")


# ─────────────────────────────────────────────
#  QUESTIONS
# ─────────────────────────────────────────────
def ask_questions():
    print_banner()
    info = {}

    section("BASIC INFO")
    info['first_name'] = ask_field("First name", "ali, ahmed, john")
    info['last_name']  = ask_field("Last name / Surname", "khan, smith, malik")
    info['nickname']   = ask_field("Nickname (comma for multiple)", "alu, sunny")
    info['username']   = ask_field("Username / Handle (comma for multiple)", "alikhan92, cool_dev")

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
    info['city']    = ask_field("City / Hometown (comma for multiple)", "lahore, karachi")
    info['company'] = ask_field("Company / School (comma for multiple)", "google, fast_university")
    info['hobby']   = ask_field("Hobby / Interest (comma for multiple)", "cricket, gaming")
    info['phone_last4'] = ask_field("Phone last 4 digits (comma for multiple)", "4567, 0000")
    info['vehicle'] = ask_field("Vehicle number (comma for multiple)", "leB-1234")
    info['extra']   = ask_field("Extra words (comma for multiple)", "love, admin")

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

    section("GENERATION OPTIONS")

    print(f"  {C.DIM}• Leetspeak : ali → 4l1, @li{C.END}")
    info['use_leet'] = ask_yes_no("Enable leetspeak?", True)

    print(f"  {C.DIM}• Reverse   : ali → ila{C.END}")
    info['add_reverse'] = ask_yes_no("Add reversed words?", True)

    print(f"  {C.DIM}• South Asian: 786, Allah, Khan (only if you want){C.END}")
    info['south_asian'] = ask_yes_no("Add South Asian patterns?", False)

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
#  BUILD TOKEN POOL
# ─────────────────────────────────────────────
def build_token_pool(info):
    """
    Returns:
      base_tokens: list of primary words (user input)
      all_tokens : list of all variations (leet, case, etc.)
    """
    base_tokens = []      # primary words
    all_tokens = []       # variations

    # ── 1. Collect base tokens from all fields (each value separately)
    multi_fields = ['nickname', 'username', 'partner', 'pet', 'child',
                    'city', 'company', 'hobby', 'extra']
    for key in multi_fields:
        raw = (info.get(key) or '').strip()
        if raw:
            for v in split_values(raw):
                if v and len(v) >= 2:
                    base_tokens.append(v)

    # Single fields (only one value each)
    single_fields = ['first_name', 'last_name', 'vehicle']
    for key in single_fields:
        val = (info.get(key) or '').strip()
        if val:
            base_tokens.append(val)

    # Phone last4 (can be multiple)
    ph_raw = (info.get('phone_last4') or '').strip()
    if ph_raw:
        for p in split_values(ph_raw):
            if p:
                base_tokens.append(p)

    # ── 2. Add DOB variations
    dob = info.get('dob', '')
    if dob:
        base_tokens.append(dob)
        if len(dob) == 8:
            d, m, y = dob[:2], dob[2:4], dob[4:]
            for v in [d+m, d+m+y, d+m+y[2:], y+m+d, y[2:]+m+d, m+d+y, y]:
                base_tokens.append(v)
        elif len(dob) == 6:
            d, m, y = dob[:2], dob[2:4], dob[4:]
            for v in [d+m+y, y+m+d, d+m, y]:
                base_tokens.append(v)
        elif len(dob) == 4:
            base_tokens.append(dob)

    # ── 3. Deduplicate base tokens (case-insensitive)
    seen_lower = set()
    unique_base = []
    for t in base_tokens:
        if t and t.lower() not in seen_lower:
            seen_lower.add(t.lower())
            unique_base.append(t)

    # ── 4. Create case variations
    for t in unique_base:
        for v in case_variations(t):
            if v and len(v) >= 2:
                all_tokens.append(v)

    # ── 5. Leetspeak variations
    if info.get('use_leet'):
        leet_list = []
        for t in unique_base:
            if t.isalpha() and 2 <= len(t) <= 12:
                leet_list.extend(leet_variations(t, max_variants=12))
        for t in leet_list:
            if t and len(t) >= 2:
                all_tokens.append(t)

    # ── 6. Deduplicate all_tokens
    seen = set()
    all_tokens = [t for t in all_tokens
                  if t and not (t in seen or seen.add(t))]

    # ── 7. South Asian patterns (optional, lowest priority)
    if info.get('south_asian'):
        sa_patterns = ['786', '143', '420', '007', '000',
                       'allah', 'ali', 'hussain', 'raza', 'haider',
                       'khan', 'malik', 'butt', 'chaudhry', 'sheikh',
                       'gujjar', 'rajput', 'memon', 'ansari', 'qureshi']
        for p in sa_patterns:
            for v in [p, p.capitalize()]:
                if v not in seen:
                    seen.add(v)
                    all_tokens.append(v)

    return unique_base, all_tokens


# ─────────────────────────────────────────────
#  NUMBERS & SPECIALS
# ─────────────────────────────────────────────
SHORT_NUMBERS = ['', '1', '12', '123', '1234', '12345', '123456',
                 '007', '69', '99', '111', '000', '786', '143']

LONG_NUMBERS = ['1234567', '12345678', '420', '2020', '2021',
                '2022', '2023', '2024', '2025', '2026']

SHORT_SPECIALS = ['', '!', '@', '#', '$', '.', '_', '-', '?', '*', '+']


# ─────────────────────────────────────────────
#  GENERATE — ROUND ROBIN ACROSS TOKENS
# ─────────────────────────────────────────────
def generate_wordlist(info):
    unique_base, all_tokens = build_token_pool(info)

    if not all_tokens:
        return []

    print()
    print(f"  {C.CYAN}[*]{C.END} Base tokens    : {C.BOLD}{len(unique_base)}{C.END}")
    print(f"  {C.CYAN}[*]{C.END} Total variations: {C.BOLD}{len(all_tokens)}{C.END}")
    print(f"  {C.CYAN}[*]{C.END} Length range   : {C.BOLD}{info['min_len']}-{info['max_len']}{C.END} chars")
    print(f"  {C.CYAN}[*]{C.END} Max passwords  : {C.BOLD}{info['max_size']}{C.END}")
    print(f"  {C.CYAN}[*]{C.END} Generating...")
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

    # ═══════════════════════════════════════════════
    #  ROUND-ROBIN STRATEGY
    #  Har phase mein sab tokens ki turn aaye
    # ═══════════════════════════════════════════════

    # ── PHASE 1: Simple tokens (as-is)
    for t in all_tokens:
        add(t)
        if len(passwords) >= max_size:
            break

    # ── PHASE 2: token + short number
    if len(passwords) < max_size:
        for n in SHORT_NUMBERS:
            for t in all_tokens:
                add(f"{t}{n}")
                if len(passwords) >= max_size:
                    break
            if len(passwords) >= max_size:
                break

    # ── PHASE 3: token + short special
    if len(passwords) < max_size:
        for s in SHORT_SPECIALS:
            if s == '':
                continue
            for t in all_tokens:
                add(f"{t}{s}")
                if len(passwords) >= max_size:
                    break
            if len(passwords) >= max_size:
                break

    # ── PHASE 4: token + number + special
    if len(passwords) < max_size:
        for n in SHORT_NUMBERS:
            for s in SHORT_SPECIALS:
                if s == '':
                    continue
                for t in all_tokens:
                    add(f"{t}{n}{s}")
                    if len(passwords) >= max_size:
                        break
                if len(passwords) >= max_size:
                    break
            if len(passwords) >= max_size:
                break

    # ── PHASE 5: Capitalize combos
    if len(passwords) < max_size:
        for p in list(passwords):
            if p and p[0].islower():
                add(p.capitalize())
            if len(passwords) >= max_size:
                break

    # ── PHASE 6: Reverse words
    if info.get('add_reverse') and len(passwords) < max_size:
        for p in list(passwords):
            add(p[::-1])
            if len(passwords) >= max_size:
                break

    # ── PHASE 7: Two-token combinations (round robin)
    if len(passwords) < max_size:
        for a in all_tokens[:len(unique_base) * 3]:
            for b in all_tokens[:len(unique_base) * 3]:
                if a == b:
                    continue
                add(f"{a}{b}")
                if len(passwords) >= max_size:
                    break
            if len(passwords) >= max_size:
                break

    # ── PHASE 8: Two-token + number + special (complex)
    if len(passwords) < max_size:
        for a in all_tokens[:len(unique_base) * 2]:
            for b in all_tokens[:len(unique_base) * 2]:
                if a == b:
                    continue
                for n in ['', '1', '123', '786', '007']:
                    for s in ['', '@', '_', '.', '!']:
                        if s == '' and n == '':
                            continue
                        add(f"{a}{s}{b}{n}")
                        if len(passwords) >= max_size:
                            break
                    if len(passwords) >= max_size:
                        break
                if len(passwords) >= max_size:
                    break
            if len(passwords) >= max_size:
                break

    # ── PHASE 9: Long numbers
    if len(passwords) < max_size:
        for n in LONG_NUMBERS:
            for t in all_tokens[:len(unique_base) * 2]:
                for s in ['', '!', '@']:
                    add(f"{t}{n}{s}")
                    if len(passwords) >= max_size:
                        break
                if len(passwords) >= max_size:
                    break
            if len(passwords) >= max_size:
                break

    # ── PHASE 10: token + special + number (different order)
    if len(passwords) < max_size:
        for s in ['@', '!', '#', '$']:
            for n in ['1', '12', '123', '1234']:
                for t in all_tokens[:len(unique_base) * 2]:
                    add(f"{t}{s}{n}")
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
