#!/usr/bin/env python3
"""
KeyForge - Smart Personal Wordlist Generator
Advanced CUPP alternative with category-based profiles.
For ethical/authorized use only.

Usage:
    python keyforge.py
"""

import os
import sys
import re
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

SHORT_NUMBERS = ['', '1', '12', '123', '1234', '12345', '123456',
                 '007', '69', '99', '111', '000', '786', '143']

LONG_NUMBERS = ['1234567', '12345678', '420', '2020', '2021',
                '2022', '2023', '2024', '2025', '2026']

SHORT_SPECIALS = ['', '!', '@', '#', '$', '.', '_', '-', '?', '*', '+']


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
    """
    Split comma-separated values. Handles all of these:
      - "abc,def,ghi"
      - "abc, def, ghi"
      - "abc , def , ghi"
      - "abc,  def  ,ghi"
      - "abc; def; ghi"  (semicolon bhi)
    """
    if not raw:
        return []
    # Comma ya semicolon se split karo
    parts = re.split(r'[,;]', raw)
    seen = set()
    result = []
    for p in parts:
        p = p.strip()
        if p and p.lower() not in seen:
            seen.add(p.lower())
            result.append(p)
    return result


def ask_field(label, example="", default=""):
    print()
    print(f"  {C.CYAN}┌─{C.END} {C.BOLD}{label}{C.END}")
    if example:
        print(f"  {C.CYAN}│{C.END}  {C.DIM}{example}{C.END}")
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


def ask_choice(prompt, choices):
    """
    choices: list of (key, label, description)
    Returns: selected key
    """
    print()
    print(f"  {C.YELLOW}{prompt}{C.END}")
    print()
    for i, (key, label, desc) in enumerate(choices, 1):
        print(f"    {C.BOLD}{i}.{C.END} {label}")
        if desc:
            print(f"       {C.DIM}{desc}{C.END}")
    print()
    while True:
        try:
            val = input(f"  {C.CYAN}└─>{C.END} ").strip()
        except EOFError:
            return choices[0][0]
        if not val:
            return choices[0][0]
        try:
            n = int(val)
            if 1 <= n <= len(choices):
                return choices[n-1][0]
        except ValueError:
            # Check by key name bhi
            for key, label, desc in choices:
                if val.lower() == key.lower():
                    return key
        print(f"    {C.RED}[!] Invalid. Try 1-{len(choices)}.{C.END}")


def section(title):
    print()
    print(f"{C.BLUE}{'━' * 65}{C.END}")
    print(f"{C.BOLD}{C.CYAN}  {title}{C.END}")
    print(f"{C.BLUE}{'━' * 65}{C.END}")


def case_variations(word):
    if not word:
        return []
    variants = [word.lower(), word.capitalize(), word.upper()]
    if ' ' in word:
        variants.append(word.title())
        variants.append(word.replace(' ', ''))
        variants.append(word.replace(' ', '_'))
        variants.append(word.replace(' ', '.'))
    variants.append(word[::-1])
    return variants


def leet_variations(word, max_variants=20):
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
    print(f"{C.CYAN}║{C.END}  {C.BOLD}{C.HEADER}K E Y F O R G E{C.END}  {C.DIM}─  Smart Wordlist Generator  v2.0.0{C.END}  {C.CYAN}║{C.END}")
    print(f"{C.CYAN}╚{'═' * 63}╝{C.END}")
    print()
    print(f"  {C.YELLOW}⚠{C.END}  For ethical/authorized use only (own accounts / pentest).")
    print(f"  {C.CYAN}💡{C.END} Leave any field empty to SKIP.")
    print(f"  {C.CYAN}💡{C.END} Use commas for multiple values: {C.BOLD}lahore, karachi, london{C.END}")


# ─────────────────────────────────────────────
#  CATEGORIES
# ─────────────────────────────────────────────
CATEGORIES = [
    ('person', '👤  Person (default)', 'General person — name, DOB, family, city'),
    ('company', '🏢  Company / Organization', 'Business name, CEO, founder, slogan, location'),
    ('place', '📍  Place / Location', 'City, street, landmarks, area names'),
    ('gaming', '🎮  Gaming / Gamer', 'Gamertag, favorite games, platform, clan'),
    ('social', '📱  Social Media / Influencer', 'Handle, niche, platform, subscribers'),
    ('student', '🎓  Student / University', 'Student name, university, roll no, department'),
    ('business', '🏪  Business / Shop', 'Shop name, owner, address, products'),
    ('custom', '🎯  Custom', 'Answer general questions only'),
]


# ─────────────────────────────────────────────
#  QUESTION TEMPLATES PER CATEGORY
# ─────────────────────────────────────────────
def ask_person_questions(info):
    section("PERSON DETAILS")
    info['first_name'] = ask_field("First name", "Example: ali, ahmed, john")
    info['last_name']  = ask_field("Last name / Surname", "Example: khan, smith, malik")
    info['nickname']   = ask_field("Nickname (comma for multiple)", "Example: alu, sunny, jr")
    info['username']   = ask_field("Username / Handle (comma for multiple)", "Example: alikhan92, cool_dev")

    section("DATE OF BIRTH")
    print(f"  {C.DIM}Formats: DDMMYYYY (15081998) | DDMMYY (150898) | YYYY (1998){C.END}")
    dob = ask_field("Date of birth", "Example: 15081998 or 150898 or 1998")
    if dob:
        clean = ''.join(c for c in dob if c.isdigit())
        if len(clean) in (4, 6, 8):
            info['dob'] = clean
        else:
            print(f"    {C.RED}[!] Invalid ({len(clean)} digits) — skipped.{C.END}")
            info['dob'] = ""
    else:
        info['dob'] = ""

    section("FAMILY / RELATIONS")
    info['partner'] = ask_field("Partner / Spouse name", "Example: sara, ayesha")
    info['child']   = ask_field("Child name(s)", "Example: hamza, emma")
    info['parent']  = ask_field("Parent name(s)", "Example: imran, nazia")
    info['sibling'] = ask_field("Sibling name(s)", "Example: ahmed, fatima")

    section("PERSONAL INFO")
    info['pet']     = ask_field("Pet name(s)", "Example: tommy, kitty")
    info['city']    = ask_field("City / Hometown (comma for multiple)", "Example: lahore, karachi")
    info['company'] = ask_field("Company / School (comma for multiple)", "Example: google, fast_university")
    info['hobby']   = ask_field("Hobby / Interest (comma for multiple)", "Example: cricket, gaming")
    info['phone_last4'] = ask_field("Phone last 4 digits (comma for multiple)", "Example: 4567, 0000")
    info['vehicle'] = ask_field("Vehicle number (comma for multiple)", "Example: leB-1234")
    info['extra']   = ask_field("Extra words (comma for multiple)", "Example: love, admin, cyberster")


def ask_company_questions(info):
    section("COMPANY DETAILS")
    info['company']   = ask_field("Company name (comma for multiple)", "Example: google, microsoft, apple")
    info['short_name'] = ask_field("Short name / Abbreviation", "Example: goog, msft, appl")
    info['founded']   = ask_field("Founded year", "Example: 1998, 2004")
    info['ceo']       = ask_field("CEO name (comma for multiple)", "Example: sundar_pichai, satya_nadella")
    info['founder']   = ask_field("Founder name(s) (comma for multiple)", "Example: larry_page, bill_gates")
    info['manager']   = ask_field("Manager / Team lead name", "Example: john, sarah")
    info['slogan']    = ask_field("Slogan / Tagline", "Example: just_do_it, think_different")
    info['product']   = ask_field("Product(s) / Service(s)", "Example: search, android, cloud")

    section("COMPANY LOCATION")
    info['city']      = ask_field("City / HQ location (comma for multiple)", "Example: california, seattle")
    info['country']   = ask_field("Country", "Example: usa, uk, pakistan")
    info['address']   = ask_field("Address keyword", "Example: mountain_view, redmond")

    section("COMPANY CULTURE")
    info['industry']  = ask_field("Industry", "Example: tech, finance, healthcare")
    info['department'] = ask_field("Department", "Example: engineering, marketing, hr")
    info['extra']     = ask_field("Extra words (comma for multiple)", "Example: employee, admin, staff")
    info['founded_dob'] = ""


def ask_place_questions(info):
    section("PLACE DETAILS")
    info['place']     = ask_field("Main place / City name", "Example: lahore, karachi, london")
    info['area']      = ask_field("Area / Neighborhood (comma for multiple)", "Example: gulberg, dha, johar")
    info['street']    = ask_field("Street / Road name", "Example: main_boulevard, mall_road")
    info['landmark']  = ask_field("Nearby landmark", "Example: liberty_market, minar_e_pakistan")
    info['postal']    = ask_field("Postal code / ZIP", "Example: 54000, 74200")

    section("PLACE INFO")
    info['country']   = ask_field("Country", "Example: pakistan, india, usa")
    info['province']  = ask_field("Province / State", "Example: punjab, sindh")
    info['language']  = ask_field("Local language", "Example: urdu, punjabi, english")
    info['nickname']  = ask_field("Nickname of place (comma for multiple)", "Example: city_of_gardens, heart_of_pakistan")
    info['famous_for'] = ask_field("Famous for", "Example: food, history, culture")
    info['extra']     = ask_field("Extra words (comma for multiple)", "Example: tourism, travel, visit")
    info['company']   = ""


def ask_gaming_questions(info):
    section("GAMER DETAILS")
    info['username']   = ask_field("Gamertag / IGN (comma for multiple)", "Example: sniper_pro, xX_dark_Xx")
    info['first_name'] = ask_field("Real name (optional)", "Example: ali, ahmed")
    info['last_name']  = ask_field("Surname (optional)", "Example: khan")
    info['nickname']   = ask_field("Nickname (comma for multiple)", "Example: alu, sunny")

    section("GAMING INFO")
    info['game']      = ask_field("Favorite game(s) (comma for multiple)", "Example: pubg, valorant, csgo, minecraft")
    info['platform']  = ask_field("Platform(s)", "Example: pc, ps5, xbox, mobile")
    info['clan']      = ask_field("Clan / Team name", "Example: team_soul, fnatic")
    info['rank']      = ask_field("Rank / Level", "Example: diamond, gold, level_50")
    info['fav_weapon'] = ask_field("Favorite weapon / character", "Example: awm, ak47, jett")
    info['stream']    = ask_field("Streaming platform", "Example: twitch, youtube, kick")
    info['discord']   = ask_field("Discord tag", "Example: alu_1234")

    section("GAMING COMMUNITY")
    info['city']      = ask_field("City", "Example: lahore, karachi")
    info['extra']     = ask_field("Extra words (comma for multiple)", "Example: pro, noob, elite, gg")
    info['company']   = ""
    info['dob']       = ""


def ask_social_questions(info):
    section("SOCIAL MEDIA DETAILS")
    info['username']  = ask_field("Main handle (comma for multiple)", "Example: alikhan, alikhan92")
    info['first_name'] = ask_field("Real name", "Example: ali")
    info['last_name'] = ask_field("Surname", "Example: khan")
    info['nickname']  = ask_field("Nickname (comma for multiple)", "Example: alu, sunny")

    section("CONTENT INFO")
    info['platform']  = ask_field("Platform(s)", "Example: instagram, youtube, tiktok")
    info['niche']     = ask_field("Niche / Category", "Example: tech, gaming, beauty, travel")
    info['subs_count'] = ask_field("Subscriber / Follower count", "Example: 100k, 1m, 50000")
    info['brand']     = ask_field("Brand / Sponsor name", "Example: nike, samsung")

    section("SOCIAL INFO")
    info['city']      = ask_field("City", "Example: lahore, karachi")
    info['email_word'] = ask_field("Email keyword", "Example: business, contact, collab")
    info['extra']     = ask_field("Extra words (comma for multiple)", "Example: viral, trending, reels")
    info['company']   = ""
    info['dob']       = ""


def ask_student_questions(info):
    section("STUDENT DETAILS")
    info['first_name'] = ask_field("First name", "Example: ali")
    info['last_name']  = ask_field("Last name", "Example: khan")
    info['nickname']   = ask_field("Nickname", "Example: alu")
    info['username']   = ask_field("Username / Handle", "Example: alikhan92")

    section("UNIVERSITY / SCHOOL")
    info['company']    = ask_field("University / School name (comma for multiple)", "Example: fast, nust, virtual_university")
    info['department'] = ask_field("Department / Major", "Example: cs, ee, bba, medical")
    info['roll_no']    = ask_field("Roll number / Student ID", "Example: 20cs123, fa20bscs001")
    info['semester']   = ask_field("Semester / Year", "Example: 4th, 2024, freshman")
    info['section']    = ask_field("Section / Class", "Example: a, b, blue")

    section("ACADEMIC INFO")
    info['city']       = ask_field("City of study", "Example: lahore, islamabad")
    info['hobby']      = ask_field("Hobby / Interest", "Example: coding, cricket")
    info['extra']      = ask_field("Extra words (comma for multiple)", "Example: student, exam, cgpa, topper")
    info['dob']        = ""


def ask_business_questions(info):
    section("BUSINESS DETAILS")
    info['company']    = ask_field("Shop / Business name (comma for multiple)", "Example: ali_store, khan_traders")
    info['owner']      = ask_field("Owner name", "Example: ali, imran")
    info['slogan']     = ask_field("Slogan / Tagline", "Example: best_prices, quality_first")
    info['type']       = ask_field("Business type", "Example: electronics, food, clothing")

    section("BUSINESS INFO")
    info['city']       = ask_field("City (comma for multiple)", "Example: lahore, karachi")
    info['area']       = ask_field("Area / Market name", "Example: hall_road, liberty_market")
    info['product']    = ask_field("Main product(s)", "Example: mobile, laptop, shoes")
    info['phone_last4'] = ask_field("Phone last 4 digits", "Example: 4567")

    section("BUSINESS EXTRA")
    info['extra']      = ask_field("Extra words (comma for multiple)", "Example: shop, store, business, sale")
    info['dob']        = ""


def ask_custom_questions(info):
    section("CUSTOM DETAILS")
    info['first_name'] = ask_field("Main word 1", "Example: ali, google, lahore")
    info['last_name']  = ask_field("Main word 2", "Example: khan, inc, city")
    info['nickname']   = ask_field("Alternate word(s) (comma for multiple)", "Example: alu, g, lhr")
    info['username']   = ask_field("Handle / Username", "Example: alikhan92")
    info['city']       = ask_field("Location / Place", "Example: lahore")
    info['company']    = ask_field("Organization", "Example: company_name")
    info['hobby']      = ask_field("Interest / Hobby", "Example: gaming")
    info['extra']      = ask_field("Extra words (comma for multiple)", "Example: cyber, admin, love")
    info['dob']        = ""


# ─────────────────────────────────────────────
#  MAIN QUESTION FLOW
# ─────────────────────────────────────────────
def ask_questions():
    print_banner()

    # ── Category Selection
    section("CHOOSE TARGET CATEGORY")
    category = ask_choice("What do you want to generate a wordlist for?",
                         CATEGORIES)

    info = {'category': category}

    # ── Category-specific questions
    if category == 'person':
        ask_person_questions(info)
    elif category == 'company':
        ask_company_questions(info)
    elif category == 'place':
        ask_place_questions(info)
    elif category == 'gaming':
        ask_gaming_questions(info)
    elif category == 'social':
        ask_social_questions(info)
    elif category == 'student':
        ask_student_questions(info)
    elif category == 'business':
        ask_business_questions(info)
    else:
        ask_custom_questions(info)

    # ── Confirmation
    all_fields = [(k, k.replace('_', ' ').title())
                  for k in info.keys() if k != 'category']
    empty = [label for key, label in all_fields if not info.get(key)]
    filled = [label for key, label in all_fields if info.get(key)]

    if not filled:
        print(f"\n  {C.RED}[!] You left EVERYTHING empty. Cannot generate a wordlist.{C.END}")
        sys.exit(1)

    section("CONFIRMATION")
    print(f"  {C.BOLD}Category:{C.END} {C.GREEN}{category.upper()}{C.END}")
    print()
    print(f"  {C.GREEN}✓ Filled :{C.END} {', '.join(filled)}")
    if empty:
        print(f"  {C.YELLOW}✗ Skipped:{C.END} {', '.join(empty)}")
        print()
        print(f"  {C.YELLOW}You left {len(empty)} field(s) EMPTY.{C.END}")
        if not ask_yes_no("Run with these skips?", default=True):
            print(f"\n  {C.RED}[!] Aborted.{C.END}")
            sys.exit(0)
    else:
        print(f"  {C.GREEN}✗ Skipped:{C.END} (none)")

    # ── Options
    section("GENERATION OPTIONS")
    print(f"  {C.DIM}• Leetspeak : ali → 4l1, @li{C.END}")
    info['use_leet'] = ask_yes_no("Enable leetspeak?", True)

    print(f"  {C.DIM}• Reverse   : ali → ila{C.END}")
    info['add_reverse'] = ask_yes_no("Add reversed words?", True)

    print(f"  {C.DIM}• South Asian: 786, Allah, Khan{C.END}")
    info['south_asian'] = ask_yes_no("Add South Asian patterns?", False)

    section("PASSWORD LENGTH")
    info['min_len'] = ask_int("Minimum password length", 6, 1, 100)
    info['max_len'] = ask_int("Maximum password length", 25, 1, 100)
    if info['min_len'] > info['max_len']:
        info['min_len'], info['max_len'] = info['max_len'], info['min_len']

    section("OUTPUT SETTINGS")
    info['max_size'] = ask_int("Max passwords to generate", 200000, 1, 50000000)
    info['output'] = ask_field("Output file", "Example: wordlist.txt (default)") or "wordlist.txt"

    return info


# ─────────────────────────────────────────────
#  BUILD TOKEN POOL
# ─────────────────────────────────────────────
def build_token_pool(info):
    base_tokens = []
    all_tokens = []

    # ── Multi-value fields (comma split)
    multi_fields = ['nickname', 'username', 'partner', 'pet', 'child',
                    'parent', 'sibling', 'city', 'company', 'hobby', 'extra',
                    'ceo', 'founder', 'manager', 'slogan', 'product',
                    'place', 'area', 'street', 'landmark', 'country',
                    'province', 'language', 'famous_for',
                    'game', 'platform', 'clan', 'rank', 'fav_weapon',
                    'stream', 'discord', 'niche', 'subs_count', 'brand',
                    'email_word', 'department', 'roll_no', 'semester',
                    'section', 'owner', 'type', 'industry', 'address',
                    'short_name', 'founded']
    for key in multi_fields:
        raw = (info.get(key) or '').strip()
        if raw:
            for v in split_values(raw):
                if v and len(v) >= 2:
                    base_tokens.append(v)

    # ── Single fields
    single_fields = ['first_name', 'last_name', 'vehicle', 'postal']
    for key in single_fields:
        val = (info.get(key) or '').strip()
        if val:
            base_tokens.append(val)

    # ── Phone
    ph_raw = (info.get('phone_last4') or '').strip()
    if ph_raw:
        for p in split_values(ph_raw):
            if p:
                base_tokens.append(p)

    # ── DOB
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

    # ── Deduplicate base
    seen_lower = set()
    unique_base = []
    for t in base_tokens:
        if t and t.lower() not in seen_lower:
            seen_lower.add(t.lower())
            unique_base.append(t)

    # ── Case variations
    for t in unique_base:
        for v in case_variations(t):
            if v and len(v) >= 2:
                all_tokens.append(v)

    # ── Leetspeak
    if info.get('use_leet'):
        leet_list = []
        for t in unique_base:
            if t.isalpha() and 2 <= len(t) <= 12:
                leet_list.extend(leet_variations(t, max_variants=12))
        for t in leet_list:
            if t and len(t) >= 2:
                all_tokens.append(t)

    # ── Dedupe
    seen = set()
    all_tokens = [t for t in all_tokens
                  if t and not (t in seen or seen.add(t))]

    # ── South Asian
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
#  GENERATE
# ─────────────────────────────────────────────
def generate_wordlist(info):
    unique_base, all_tokens = build_token_pool(info)

    if not all_tokens:
        return []

    print()
    print(f"  {C.CYAN}[*]{C.END} Category        : {C.BOLD}{info['category'].upper()}{C.END}")
    print(f"  {C.CYAN}[*]{C.END} Base tokens     : {C.BOLD}{len(unique_base)}{C.END}")
    print(f"  {C.CYAN}[*]{C.END} Total variations: {C.BOLD}{len(all_tokens)}{C.END}")
    print(f"  {C.CYAN}[*]{C.END} Length range    : {C.BOLD}{info['min_len']}-{info['max_len']}{C.END} chars")
    print(f"  {C.CYAN}[*]{C.END} Max passwords   : {C.BOLD}{info['max_size']}{C.END}")
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
    #  ROUND-ROBIN PHASES
    # ═══════════════════════════════════════════════

    # Phase 1: Simple tokens
    for t in all_tokens:
        add(t)
        if len(passwords) >= max_size:
            break

    # Phase 2: token + short number
    if len(passwords) < max_size:
        for n in SHORT_NUMBERS:
            for t in all_tokens:
                add(f"{t}{n}")
                if len(passwords) >= max_size:
                    break
            if len(passwords) >= max_size:
                break

    # Phase 3: token + special
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

    # Phase 4: token + number + special
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

    # Phase 5: Capitalize
    if len(passwords) < max_size:
        for p in list(passwords):
            if p and p[0].islower():
                add(p.capitalize())
            if len(passwords) >= max_size:
                break

    # Phase 6: Reverse
    if info.get('add_reverse') and len(passwords) < max_size:
        for p in list(passwords):
            add(p[::-1])
            if len(passwords) >= max_size:
                break

    # Phase 7: Two-token combos
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

    # Phase 8: Two-token + num + special
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

    # Phase 9: Long numbers
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

    # Phase 10: token + special
    # Phase 10: token + special + number (different order)
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
