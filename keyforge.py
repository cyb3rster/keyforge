#!/usr/bin/env python3
"""KeyForge - Smart Wordlist Generator with AI Refinement. Ethical use only."""

import os
import sys
import re
import json
import itertools
import urllib.request
import urllib.error

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

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".keyforge")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


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


def split_values(raw):
    if not raw:
        return []
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
    print(f"  {C.CYAN}--{C.END} {C.BOLD}{label}{C.END}")
    if example:
        print(f"  {C.CYAN}|{C.END}  {C.DIM}{example}{C.END}")
    try:
        val = input(f"  {C.CYAN}>{C.END} ").strip()
    except EOFError:
        return default
    if val.lower() in ('skip', 's', 'none', 'na', 'n/a', 'unknown'):
        return default
    return val if val else default


def ask_yes_no(prompt, default=False):
    marker = 'y' if default else 'n'
    try:
        val = input(f"  {C.YELLOW}?{C.END} {prompt} (y/n) [{marker}]: ").strip().lower()
    except EOFError:
        return default
    if not val:
        return default
    return val in ('y', 'yes', '1', 'true')


def ask_int(prompt, default, min_val=1, max_val=10**9):
    try:
        val = input(f"  {C.YELLOW}?{C.END} {prompt} [{default}]: ").strip()
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
        print(f"    {C.RED}[!] Invalid, using default: {default}{C.END}")
        return default


def ask_choice(prompt, choices):
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
            val = input(f"  {C.CYAN}>{C.END} ").strip()
        except EOFError:
            return choices[0][0]
        if not val:
            return choices[0][0]
        try:
            n = int(val)
            if 1 <= n <= len(choices):
                return choices[n-1][0]
        except ValueError:
            for key, label, desc in choices:
                if val.lower() == key.lower():
                    return key
        print(f"    {C.RED}[!] Invalid. Try 1-{len(choices)}.{C.END}")


def section(title):
    print()
    print(f"{C.BLUE}{'=' * 65}{C.END}")
    print(f"{C.BOLD}{C.CYAN}  {title}{C.END}")
    print(f"{C.BLUE}{'=' * 65}{C.END}")


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
    print(f"{C.CYAN}+{'=' * 63}+{C.END}")
    print(f"{C.CYAN}|{C.END}  {C.BOLD}{C.HEADER}K E Y F O R G E{C.END}  {C.DIM}-  Wordlist Generator  v3.0.0{C.END}  {C.CYAN}|{C.END}")
    print(f"{C.CYAN}+{'=' * 63}+{C.END}")
    print()
    print(f"  {C.YELLOW}[!]{C.END}  For ethical/authorized use only.")
    print(f"  {C.CYAN}[i]{C.END} Leave any field empty to SKIP.")
    print(f"  {C.CYAN}[i]{C.END} Use commas for multiple: {C.BOLD}lahore, karachi{C.END}")


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(config):
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        if os.name != 'nt':
            try:
                os.chmod(CONFIG_FILE, 0o600)
            except Exception:
                pass
        return True
    except Exception as e:
        print(f"  {C.RED}[!] Could not save config: {e}{C.END}")
        return False


def get_api_key():
    env_key = os.environ.get('GEMINI_API_KEY', '').strip()
    if env_key:
        return env_key, 'env'
    config = load_config()
    key = config.get('gemini_api_key', '').strip()
    if key:
        return key, 'file'
    return '', 'none'


def manage_api_key():
    while True:
        key, source = get_api_key()
        section("API KEY MANAGEMENT")

        if key:
            masked = key[:8] + '...' + key[-4:] if len(key) > 12 else '***'
            source_label = 'Environment Variable' if source == 'env' else f'Local ({CONFIG_FILE})'
            print(f"  {C.GREEN}[OK]{C.END} Current key : {C.BOLD}{masked}{C.END}")
            print(f"  {C.DIM}Source: {source_label}{C.END}")
        else:
            print(f"  {C.YELLOW}[!]{C.END} No API key configured")
            print(f"  {C.DIM}Get free: https://aistudio.google.com/app/apikey{C.END}")

        print()
        print(f"  {C.BOLD}Options:{C.END}")
        print(f"    1. Add / Replace API key")
        if key and source == 'file':
            print(f"    2. Delete API key")
            print(f"    3. Back")
            max_c = 3
        else:
            print(f"    2. Back")
            max_c = 2

        print()
        try:
            choice = input(f"  {C.CYAN}>{C.END} ").strip()
        except EOFError:
            return

        if choice == '1':
            print()
            print(f"  {C.DIM}Get key: https://aistudio.google.com/app/apikey{C.END}")
            try:
                new_key = input(f"  {C.YELLOW}?{C.END} Paste API key: ").strip()
            except EOFError:
                continue
            if not new_key:
                print(f"  {C.RED}[!] Empty.{C.END}")
                continue
            config = load_config()
            config['gemini_api_key'] = new_key
            if save_config(config):
                print(f"  {C.GREEN}[OK]{C.END} Key saved: {CONFIG_FILE}")
            input(f"\n  Press Enter...")
        elif choice == '2' and key and source == 'file':
            if ask_yes_no("Delete API key?", default=False):
                config = load_config()
                config.pop('gemini_api_key', None)
                save_config(config)
                print(f"  {C.GREEN}[OK]{C.END} Deleted.")
            input(f"\n  Press Enter...")
        elif choice == str(max_c):
            return
        else:
            print(f"  {C.RED}[!] Invalid.{C.END}")


CATEGORIES = [
    ('person',   '👤  Person (default)',            'Name, DOB, family, city'),
    ('company',  '🏢  Company / Organization',      'Company, CEO, founder, slogan'),
    ('place',    '📍  Place / Location',            'City, street, landmarks'),
    ('gaming',   '🎮  Gaming / Gamer',              'Gamertag, games, clan'),
    ('social',   '📱  Social Media / Influencer',   'Handle, niche, platform'),
    ('student',  '🎓  Student / University',        'Name, university, roll no'),
    ('business', '🏪  Business / Shop',             'Shop name, owner, products'),
    ('custom',   '🎯  Custom',                      'General questions'),
]


def ask_person_questions(info):
    section("PERSON DETAILS")
    info['first_name'] = ask_field("First name", "Example: ali, ahmed")
    info['last_name']  = ask_field("Last name", "Example: khan, smith")
    info['nickname']   = ask_field("Nickname (comma for multiple)", "Example: alu, sunny")
    info['username']   = ask_field("Username (comma for multiple)", "Example: alikhan92")
    section("DATE OF BIRTH")
    print(f"  {C.DIM}DDMMYYYY (15081998) | DDMMYY (150898) | YYYY (1998){C.END}")
    dob = ask_field("Date of birth", "Example: 15081998")
    if dob:
        clean = ''.join(c for c in dob if c.isdigit())
        info['dob'] = clean if len(clean) in (4, 6, 8) else ""
    else:
        info['dob'] = ""
    section("FAMILY / RELATIONS")
    info['partner'] = ask_field("Partner name", "Example: sara")
    info['child']   = ask_field("Child name(s)", "Example: hamza")
    info['parent']  = ask_field("Parent name(s)", "Example: imran")
    info['sibling'] = ask_field("Sibling name(s)", "Example: ahmed")
    section("PERSONAL INFO")
    info['pet']     = ask_field("Pet name(s)", "Example: tommy")
    info['city']    = ask_field("City (comma)", "Example: lahore, karachi")
    info['company'] = ask_field("Company / School", "Example: google, fast")
    info['hobby']   = ask_field("Hobby (comma)", "Example: cricket, gaming")
    info['phone_last4'] = ask_field("Phone last 4", "Example: 4567")
    info['vehicle'] = ask_field("Vehicle number", "Example: leB-1234")
    info['extra']   = ask_field("Extra words (comma)", "Example: love, admin")


def ask_company_questions(info):
    section("COMPANY DETAILS")
    info['company']   = ask_field("Company name (comma)", "Example: google, microsoft")
    info['short_name'] = ask_field("Short name / Abbreviation", "Example: goog")
    info['founded']   = ask_field("Founded year", "Example: 1998")
    info['ceo']       = ask_field("CEO name (comma)", "Example: sundar_pichai")
    info['founder']   = ask_field("Founder (comma)", "Example: larry_page")
    info['manager']   = ask_field("Manager name", "Example: john")
    info['slogan']    = ask_field("Slogan", "Example: just_do_it")
    info['product']   = ask_field("Products", "Example: search, android")
    section("LOCATION")
    info['city']      = ask_field("City (comma)", "Example: california")
    info['country']   = ask_field("Country", "Example: usa")
    info['address']   = ask_field("Address keyword", "Example: mountain_view")
    section("CULTURE")
    info['industry']  = ask_field("Industry", "Example: tech")
    info['department'] = ask_field("Department", "Example: engineering")
    info['extra']     = ask_field("Extra (comma)", "Example: employee, staff")
    info['dob']       = ""


def ask_place_questions(info):
    section("PLACE DETAILS")
    info['place']     = ask_field("Main place / City", "Example: lahore")
    info['area']      = ask_field("Area (comma)", "Example: gulberg, dha")
    info['street']    = ask_field("Street name", "Example: mall_road")
    info['landmark']  = ask_field("Landmark", "Example: liberty_market")
    info['postal']    = ask_field("Postal code", "Example: 54000")
    section("PLACE INFO")
    info['country']   = ask_field("Country", "Example: pakistan")
    info['province']  = ask_field("Province", "Example: punjab")
    info['language']  = ask_field("Local language", "Example: urdu")
    info['nickname']  = ask_field("Nickname (comma)", "Example: city_of_gardens")
    info['famous_for'] = ask_field("Famous for", "Example: food")
    info['extra']     = ask_field("Extra (comma)", "Example: tourism")
    info['company']   = ""
    info['dob']       = ""


def ask_gaming_questions(info):
    section("GAMER DETAILS")
    info['username']   = ask_field("Gamertag (comma)", "Example: sniper_pro")
    info['first_name'] = ask_field("Real name", "Example: ali")
    info['last_name']  = ask_field("Surname", "Example: khan")
    info['nickname']   = ask_field("Nickname", "Example: alu")
    section("GAMING INFO")
    info['game']      = ask_field("Games (comma)", "Example: pubg, valorant")
    info['platform']  = ask_field("Platform(s)", "Example: pc, ps5")
    info['clan']      = ask_field("Clan name", "Example: team_soul")
    info['rank']      = ask_field("Rank", "Example: diamond")
    info['fav_weapon'] = ask_field("Fav weapon", "Example: awm")
    info['stream']    = ask_field("Stream platform", "Example: twitch")
    info['discord']   = ask_field("Discord tag", "Example: alu_1234")
    section("COMMUNITY")
    info['city']      = ask_field("City", "Example: lahore")
    info['extra']     = ask_field("Extra (comma)", "Example: pro, elite")
    info['company']   = ""
    info['dob']       = ""


def ask_social_questions(info):
    section("SOCIAL MEDIA DETAILS")
    info['username']  = ask_field("Handle (comma)", "Example: alikhan")
    info['first_name'] = ask_field("Real name", "Example: ali")
    info['last_name'] = ask_field("Surname", "Example: khan")
    info['nickname']  = ask_field("Nickname", "Example: alu")
    section("CONTENT INFO")
    info['platform']  = ask_field("Platforms", "Example: instagram, youtube")
    info['niche']     = ask_field("Niche", "Example: tech, gaming")
    info['subs_count'] = ask_field("Sub count", "Example: 100k")
    info['brand']     = ask_field("Brand name", "Example: nike")
    section("SOCIAL INFO")
    info['city']      = ask_field("City", "Example: lahore")
    info['email_word'] = ask_field("Email keyword", "Example: business")
    info['extra']     = ask_field("Extra (comma)", "Example: viral, reels")
    info['company']   = ""
    info['dob']       = ""


def ask_student_questions(info):
    section("STUDENT DETAILS")
    info['first_name'] = ask_field("First name", "Example: ali")
    info['last_name']  = ask_field("Last name", "Example: khan")
    info['nickname']   = ask_field("Nickname", "Example: alu")
    info['username']   = ask_field("Username", "Example: alikhan92")
    section("UNIVERSITY")
    info['company']    = ask_field("University (comma)", "Example: fast, nust")
    info['department'] = ask_field("Department", "Example: cs, ee")
    info['roll_no']    = ask_field("Roll number", "Example: 20cs123")
    info['semester']   = ask_field("Semester", "Example: 4th")
    info['section']    = ask_field("Section", "Example: a")
    section("ACADEMIC")
    info['city']       = ask_field("City", "Example: lahore")
    info['hobby']      = ask_field("Hobby", "Example: coding")
    info['extra']      = ask_field("Extra (comma)", "Example: student, exam")
    info['dob']        = ""


def ask_business_questions(info):
    section("BUSINESS DETAILS")
    info['company']    = ask_field("Shop name (comma)", "Example: ali_store")
    info['owner']      = ask_field("Owner name", "Example: ali")
    info['slogan']     = ask_field("Slogan", "Example: best_prices")
    info['type']       = ask_field("Business type", "Example: electronics")
    section("BUSINESS INFO")
    info['city']       = ask_field("City (comma)", "Example: lahore")
    info['area']       = ask_field("Area name", "Example: hall_road")
    info['product']    = ask_field("Products", "Example: mobile")
    info['phone_last4'] = ask_field("Phone last 4", "Example: 4567")
    section("EXTRA")
    info['extra']      = ask_field("Extra (comma)", "Example: shop, sale")
    info['dob']        = ""


def ask_custom_questions(info):
    section("CUSTOM DETAILS")
    info['first_name'] = ask_field("Main word 1", "Example: ali")
    info['last_name']  = ask_field("Main word 2", "Example: khan")
    info['nickname']   = ask_field("Alternate (comma)", "Example: alu, lhr")
    info['username']   = ask_field("Handle", "Example: alikhan92")
    info['city']       = ask_field("Location", "Example: lahore")
    info['company']    = ask_field("Organization", "Example: company")
    info['hobby']      = ask_field("Interest", "Example: gaming")
    info['extra']      = ask_field("Extra (comma)", "Example: cyber, admin")
    info['dob']        = ""


def ask_questions():
    print_banner()
    section("CHOOSE TARGET CATEGORY")
    category = ask_choice("What do you want to generate a wordlist for?", CATEGORIES)
    info = {'category': category}

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

    all_fields = [(k, k.replace('_', ' ').title()) for k in info.keys() if k != 'category']
    empty = [label for key, label in all_fields if not info.get(key)]
    filled = [label for key, label in all_fields if info.get(key)]

    if not filled:
        print(f"\n  {C.RED}[!] Everything empty. Cannot generate.{C.END}")
        sys.exit(1)

    section("CONFIRMATION")
    print(f"  {C.BOLD}Category:{C.END} {C.GREEN}{category.upper()}{C.END}")
    print()
    print(f"  {C.GREEN}[+]{C.END} Filled : {', '.join(filled)}")
    if empty:
        print(f"  {C.YELLOW}[-]{C.END} Skipped: {', '.join(empty)}")
        print()
        if not ask_yes_no(f"Run with {len(empty)} skip(s)?", default=True):
            print(f"\n  {C.RED}[!] Aborted.{C.END}")
            sys.exit(0)
    else:
        print(f"  {C.GREEN}[-]{C.END} Skipped: (none)")

    section("GENERATION OPTIONS")
    print(f"  {C.DIM}Leetspeak : ali -> 4l1, @li{C.END}")
    info['use_leet'] = ask_yes_no("Enable leetspeak?", True)
    print(f"  {C.DIM}Reverse   : ali -> ila{C.END}")
    info['add_reverse'] = ask_yes_no("Add reversed words?", True)
    print(f"  {C.DIM}South Asian: 786, Allah, Khan{C.END}")
    info['south_asian'] = ask_yes_no("Add South Asian patterns?", False)

    section("PASSWORD LENGTH")
    info['min_len'] = ask_int("Min password length", 6, 1, 100)
    info['max_len'] = ask_int("Max password length", 25, 1, 100)
    if info['min_len'] > info['max_len']:
        info['min_len'], info['max_len'] = info['max_len'], info['min_len']

    section("OUTPUT SETTINGS")
    info['max_size'] = ask_int("Max passwords", 200000, 1, 50000000)
    info['output'] = ask_field("Output file", "Example: wordlist.txt") or "wordlist.txt"

    return info


def build_token_pool(info):
    base_tokens = []
    all_tokens = []

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

    single_fields = ['first_name', 'last_name', 'vehicle', 'postal']
    for key in single_fields:
        val = (info.get(key) or '').strip()
        if val:
            base_tokens.append(val)

    ph_raw = (info.get('phone_last4') or '').strip()
    if ph_raw:
        for p in split_values(ph_raw):
            if p:
                base_tokens.append(p)

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

    seen_lower = set()
    unique_base = []
    for t in base_tokens:
        if t and t.lower() not in seen_lower:
            seen_lower.add(t.lower())
            unique_base.append(t)

    for t in unique_base:
        for v in case_variations(t):
            if v and len(v) >= 2:
                all_tokens.append(v)

    if info.get('use_leet'):
        leet_list = []
        for t in unique_base:
            if t.isalpha() and 2 <= len(t) <= 12:
                leet_list.extend(leet_variations(t, max_variants=12))
        for t in leet_list:
            if t and len(t) >= 2:
                all_tokens.append(t)

    seen = set()
    all_tokens = [t for t in all_tokens if t and not (t in seen or seen.add(t))]

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


def generate_wordlist(info):
    unique_base, all_tokens = build_token_pool(info)
    if not all_tokens:
        return []

    print()
    print(f"  {C.CYAN}[*]{C.END} Category        : {C.BOLD}{info['category'].upper()}{C.END}")
    print(f"  {C.CYAN}[*]{C.END} Base tokens     : {C.BOLD}{len(unique_base)}{C.END}")
    print(f"  {C.CYAN}[*]{C.END} Total variations: {C.BOLD}{len(all_tokens)}{C.END}")
    print(f"  {C.CYAN}[*]{C.END} Length range    : {C.BOLD}{info['min_len']}-{info['max_len']}{C.END}")
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

    # Priority 1: two-token + separator
    for a in all_tokens:
        for b in all_tokens:
            if a == b:
                continue
            for sep in ['@', '_', '.', '-', '#', '$', '!']:
                add(f"{a}{sep}{b}")
                if len(passwords) >= max_size: break
            if len(passwords) >= max_size: break
        if len(passwords) >= max_size: break

    # Priority 2: two-token + number
    if len(passwords) < max_size:
        for a in all_tokens:
            for b in all_tokens:
                if a == b:
                    continue
                for n in ['1', '12', '123', '1234', '007', '786']:
                    add(f"{a}{b}{n}")
                    add(f"{a}{n}{b}")
                    if len(passwords) >= max_size: break
                if len(passwords) >= max_size: break
            if len(passwords) >= max_size: break

    # Priority 3: simple tokens
    for t in all_tokens:
        add(t)
        if len(passwords) >= max_size: break

    # Priority 4: token + number
    if len(passwords) < max_size:
        for n in SHORT_NUMBERS:
            for t in all_tokens:
                add(f"{t}{n}")
                if len(passwords) >= max_size: break
            if len(passwords) >= max_size: break

    # Priority 5: token + special
    if len(passwords) < max_size:
        for s in SHORT_SPECIALS:
            if s == '':
                continue
            for t in all_tokens:
                add(f"{t}{s}")
                if len(passwords) >= max_size: break
            if len(passwords) >= max_size: break

    # Priority 6: token + number + special
    if len(passwords) < max_size:
        for n in SHORT_NUMBERS:
            for s in SHORT_SPECIALS:
                if s == '':
                    continue
                for t in all_tokens:
                    add(f"{t}{n}{s}")
                    if len(passwords) >= max_size: break
                if len(passwords) >= max_size: break
            if len(passwords) >= max_size: break

    # Priority 7: token + special + number
    if len(passwords) < max_size:
        for s in ['@', '!', '#', '$', '_', '.']:
            for n in ['1', '12', '123', '1234', '12345']:
                for t in all_tokens:
                    add(f"{t}{s}{n}")
                    if len(passwords) >= max_size: break
                if len(passwords) >= max_size: break
            if len(passwords) >= max_size: break

    # Priority 8: capitalize
    if len(passwords) < max_size:
        for p in list(passwords):
            if p and p[0].islower():
                add(p.capitalize())
            if len(passwords) >= max_size: break

    # Priority 9: reverse
    if info.get('add_reverse') and len(passwords) < max_size:
        for p in list(passwords):
            add(p[::-1])
            if len(passwords) >= max_size: break

    # Priority 10: two-token + sep + number
    if len(passwords) < max_size:
        for a in all_tokens[:len(unique_base) * 2]:
            for b in all_tokens[:len(unique_base) * 2]:
                if a == b: continue
                for sep in ['@', '_', '.']:
                    for n in ['1', '123', '1234']:
                        add(f"{a}{sep}{b}{n}")
                        if len(passwords) >= max_size: break
                    if len(passwords) >= max_size: break
                if len(passwords) >= max_size: break
            if len(passwords) >= max_size: break

    passwords = passwords[:max_size]
    print(f"  {C.GREEN}[OK]{C.END} Total passwords generated: {C.BOLD}{len(passwords)}{C.END}")
    return passwords


def save_wordlist(passwords, output_file):
    if not os.path.splitext(output_file)[1]:
        output_file += '.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for p in passwords:
            f.write(p + '\n')
    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"  {C.GREEN}[OK]{C.END} Saved: {C.BOLD}{os.path.abspath(output_file)}{C.END}")
   
