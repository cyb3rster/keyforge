#!/usr/bin/env python3
"""KeyForge - Smart Wordlist Generator with AI Refinement. Ethical use only."""

import os
import sys
import re
import json
import itertools
import time
import random
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

GEMINI_FALLBACK_MODELS = [
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]

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
    env_checks = [
        ('GEMINI_API_KEY', 'gemini'),
        ('OPENAI_API_KEY', 'openai'),
        ('CLAUDE_API_KEY', 'claude'),
        ('API_KEY', 'custom'),
    ]
    for env_var, provider in env_checks:
        key = os.environ.get(env_var, '').strip()
        if key:
            return key, provider

    config = load_config()
    for p in ('gemini', 'openai', 'claude'):
        key = (config.get(f'{p}_api_key', '') or '').strip()
        if key:
            return key, p

    key = (config.get('api_key', '') or '').strip()
    if key:
        provider = config.get('ai_provider', 'custom') or 'custom'
        return key, provider

    return '', 'none'


def save_api_key(key, provider):
    config = load_config()
    config['api_key'] = key
    if provider:
        config[f'{provider}_api_key'] = key
        config['ai_provider'] = provider
    else:
        config['ai_provider'] = config.get('ai_provider', 'gemini')
    return save_config(config)


def ask_ai_provider(default='gemini'):
    section("AI PROVIDER")
    options = [
        ('gemini', 'Google Gemini', 'Default'),
        ('openai', 'OpenAI (ChatGPT)', 'Not implemented yet'),
        ('claude', 'Anthropic (Claude)', 'Not implemented yet'),
        ('custom', 'Custom / Other', 'Uses Gemini fallback for now'),
    ]
    print()
    for i, (key, label, desc) in enumerate(options, 1):
        print(f"    {C.BOLD}{i}.{C.END} {label}")
        if desc:
            print(f"       {C.DIM}{desc}{C.END}")
    print()
    default_keys = [o[0] for o in options]
    while True:
        try:
            val = input(f"  {C.CYAN}>{C.END} ").strip()
        except EOFError:
            return default if default in default_keys else 'gemini'
        if not val:
            return default if default in default_keys else 'gemini'
        try:
            n = int(val)
            if 1 <= n <= len(options):
                return options[n-1][0]
        except ValueError:
            for key, label, desc in options:
                if val.lower() == key.lower():
                    return key
        print(f"    {C.RED}[!] Invalid. Try 1-{len(options)}.{C.END}")


def manage_api_key():
    while True:
        config = load_config()
        file_has_key = bool(
            (config.get('api_key') or '').strip() or
            any((config.get(f'{p}_api_key') or '').strip() for p in ('gemini', 'openai', 'claude'))
        )

        section("API KEY MANAGEMENT")

        env_key = None
        env_provider = None
        for env_var, provider in [
            ('GEMINI_API_KEY', 'gemini'),
            ('OPENAI_API_KEY', 'openai'),
            ('CLAUDE_API_KEY', 'claude'),
            ('API_KEY', 'custom')
        ]:
            key = os.environ.get(env_var, '').strip()
            if key:
                env_key = key
                env_provider = provider
                break

        if env_key:
            masked = env_key[:8] + '...' + env_key[-4:] if len(env_key) > 12 else '***'
            print(f"  {C.GREEN}[OK]{C.END} Current key : {C.BOLD}{masked}{C.END}")
            print(f"  {C.DIM}Source: Environment Variable ({env_provider.upper()}){C.END}")
        elif file_has_key:
            key, provider = get_api_key()
            masked = key[:8] + '...' + key[-4:] if len(key) > 12 else '***'
            print(f"  {C.GREEN}[OK]{C.END} Current key : {C.BOLD}{masked}{C.END}")
            print(f"  {C.DIM}Source: Local ({CONFIG_FILE})  Provider: {provider.upper()}{C.END}")
        else:
            print(f"  {C.YELLOW}[!]{C.END} No API key configured")
            print(f"  {C.DIM}Get AI API key:{C.END}")
            print(f"    {C.DIM}Gemini   : https://aistudio.google.com/app/apikey{C.END}")
            print(f"    {C.DIM}OpenAI   : https://platform.openai.com/api-keys{C.END}")
            print(f"    {C.DIM}Claude   : https://console.anthropic.com/settings/keys{C.END}")

        print()
        print(f"  {C.BOLD}Options:{C.END}")
        print(f"    1. Add / Replace API key")
        if file_has_key:
            print(f"    2. Delete API key")
            print(f"    3. Back")
            max_choice = 3
        else:
            print(f"    2. Back")
            max_choice = 2
        print()

        try:
            choice = input(f"  {C.CYAN}>{C.END} ").strip()
        except EOFError:
            return

        if choice == '1':
            print()
            print(f"  {C.DIM}Get AI API key:{C.END}")
            print(f"    {C.DIM}Gemini   : https://aistudio.google.com/app/apikey{C.END}")
            print(f"    {C.DIM}OpenAI   : https://platform.openai.com/api-keys{C.END}")
            print(f"    {C.DIM}Claude   : https://console.anthropic.com/settings/keys{C.END}")
            print()
            provider = ask_ai_provider(default=config.get('ai_provider', 'gemini'))
            try:
                new_key = input(f"  {C.YELLOW}?{C.END} Paste API key: ").strip()
            except EOFError:
                continue
            if not new_key:
                print(f"  {C.RED}[!] Empty key not allowed.{C.END}")
                continue
            # Accept ANY non-empty API key format. Google Gemini supports both old and new keys.
            if save_api_key(new_key, provider):
                print(f"  {C.GREEN}[OK]{C.END} Key saved: {CONFIG_FILE}")
                print(f"  {C.GREEN}[OK]{C.END} Provider saved: {provider.upper()}")
            input(f"\n  Press Enter...")
        elif choice == '2' and file_has_key:
            if ask_yes_no("Delete API key?", default=False):
                config = load_config()
                config.pop('api_key', None)
                for p in ('gemini', 'openai', 'claude'):
                    config.pop(f'{p}_api_key', None)
                config.pop('ai_provider', None)
                save_config(config)
                print(f"  {C.GREEN}[OK]{C.END} Deleted.")
            input(f"\n  Press Enter...")
        elif choice == str(max_choice):
            return
        else:
            print(f"  {C.RED}[!] Invalid.{C.END}")


def call_ai_api(key, provider, payload, timeout=90):
    """
    Call AI API with retry logic (for 503/429) and model fallback (for Gemini).
    
    - Retries on 503 (Service Unavailable) and 429 (Rate Limit) with exponential backoff + jitter
    - Falls back to next Gemini model on persistent 503 errors
    - Raises immediately for permanent errors (400, 401, 403, 404, etc.)
    
    Returns: JSON response dict on success
    Raises: Exception on all retries exhausted or permanent error
    """
    provider = (provider or 'gemini').lower()

    # Determine base URL and model list for fallback
    if provider == 'gemini':
        models_to_try = GEMINI_FALLBACK_MODELS
        base_url = "https://generativelanguage.googleapis.com/v1beta/models"
    else:
        # Non-Gemini providers: use fallback to Gemini
        if provider in ('openai', 'claude'):
            print(f"  {C.YELLOW}[!]{C.END} {provider.capitalize()} not yet implemented. Using Gemini fallback.")
        models_to_try = [GEMINI_FALLBACK_MODELS[0]]
        base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    # Try each model in sequence
    for model_idx, model_name in enumerate(models_to_try):
        url = f"{base_url}/{model_name}:generateContent"
        
        if model_idx > 0:
            print(f"  {C.GREEN}[OK]{C.END} Using model: {C.BOLD}{model_name}{C.END}")

        # Retry logic for this model
        retry_delays = [2, 4, 8]  # exponential backoff: 2s, 4s, 8s
        max_retries = len(retry_delays)
        
        for attempt in range(max_retries + 1):
            try:
                req = urllib.request.Request(
                    f"{url}?key={key}",
                    data=json.dumps(payload).encode('utf-8'),
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return json.loads(resp.read().decode('utf-8'))

            except urllib.error.HTTPError as e:
                # Permanent errors: raise immediately (don't retry or fallback)
                if e.code in (400, 401, 403):
                    try:
                        body = json.loads(e.read().decode('utf-8', 'ignore'))
                        msg = body.get('error', {}).get('message') or body.get('message') or e.reason
                    except Exception:
                        msg = e.reason
                    raise Exception(f"Permanent error {e.code}: {msg}")
                
                # 404: model not found (try next model)
                if e.code == 404:
                    print(f"  {C.YELLOW}[!]{C.END} Model {model_name} not found (404). Trying next model...")
                    break  # Break inner loop to try next model
                
                # 503 (Service Unavailable) or 429 (Rate Limit): retry with backoff
                if e.code in (503, 429):
                    is_overloaded = e.code == 503
                    status_name = "overloaded" if is_overloaded else "rate limited"
                    
                    if attempt < max_retries:
                        wait_time = retry_delays[attempt]
                        jitter = random.uniform(0, 1)
                        total_wait = wait_time + jitter
                        print(f"  {C.YELLOW}[!]{C.END} Model {model_name} is {status_name} ({e.code}). Retrying in {total_wait:.1f}s...")
                        time.sleep(total_wait)
                    else:
                        # All retries exhausted for this model
                        print(f"  {C.YELLOW}[!]{C.END} Model {model_name} failed after {max_retries} retries. Trying next model...")
                        break  # Break inner loop to try next model
                    continue  # Continue to next retry attempt
                
                # Other HTTP errors: raise
                try:
                    body = json.loads(e.read().decode('utf-8', 'ignore'))
                    msg = body.get('error', {}).get('message') or body.get('message') or e.reason
                except Exception:
                    msg = e.reason
                raise Exception(f"API error {e.code}: {msg}")

            except urllib.error.URLError as e:
                raise Exception(f"Network error: {e.reason}")

    # All models exhausted
    raise Exception("All models are currently overloaded. Please try again later.")


CATEGORIES = [
    ('person',   'Person (default)',           'Name, DOB, family, city'),
    ('company',  'Company / Organization',     'Company, CEO, founder, slogan'),
    ('place',    'Place / Location',           'City, street, landmarks'),
    ('gaming',   'Gaming / Gamer',             'Gamertag, games, clan'),
    ('social',   'Social Media / Influencer',  'Handle, niche, platform'),
    ('student',  'Student / University',       'Name, university, roll no'),
    ('business', 'Business / Shop',            'Shop name, owner, products'),
    ('custom',   'Custom',                     'General questions'),
]


def ask_person_questions(info):
    section("PERSON DETAILS")
    info['first_name'] = ask_field("First name", "Example: Ali, John, Rahul")
    info['last_name']  = ask_field("Last name", "Example: Khan, Smith, Kumar")
    info['nickname']   = ask_field("Nickname (comma)", "Example: Ali, Johnny, Sunny")
    info['username']   = ask_field("Username (comma)", "Example: alikhan92, jsmith")
    section("DATE OF BIRTH")
    print(f"  {C.DIM}DDMMYYYY (15081998) | DDMMYY (150898) | YYYY (1998){C.END}")
    dob = ask_field("Date of birth", "Example: 15081998")
    if dob:
        clean = ''.join(c for c in dob if c.isdigit())
        info['dob'] = clean if len(clean) in (4, 6, 8) else ""
    else:
        info['dob'] = ""
    section("FAMILY / RELATIONS")
    info['partner'] = ask_field("Partner name", "Example: Sarah, Emma")
    info['child']   = ask_field("Child name(s)", "Example: Aisha, Adam")
    info['parent']  = ask_field("Parent name(s)", "Example: Ahmed, Maria")
    info['sibling'] = ask_field("Sibling name(s)", "Example: Sara, Ali")
    section("PERSONAL INFO")
    info['pet']     = ask_field("Pet name(s)", "Example: Max, Lucy, Teddy")
    info['city']    = ask_field("City (comma)", "Example: New York, London, Tokyo")
    info['company'] = ask_field("Company / School", "Example: Google, Microsoft, Stanford")
    info['hobby']   = ask_field("Hobby (comma)", "Example: gaming, reading, travel")
    info['phone_last4'] = ask_field("Phone last 4", "Example: 4567")
    info['vehicle'] = ask_field("Vehicle number", "Example: AB-1234")
    info['extra']   = ask_field("Extra words (comma)", "Example: love, admin, hello")


def ask_company_questions(info):
    section("COMPANY DETAILS")
    info['company']    = ask_field("Company name (comma)", "Example: Google, Microsoft, Tesla")
    info['short_name'] = ask_field("Short name / Abbreviation", "Example: G, MSFT, TSLA")
    info['founded']    = ask_field("Founded year", "Example: 2024")
    info['ceo']        = ask_field("CEO name (comma)", "Example: Sundar Pichai, Satya Nadella")
    info['founder']    = ask_field("Founder (comma)", "Example: Larry Page, Elon Musk")
    info['manager']    = ask_field("Manager name", "Example: John, Sarah, Ahmed")
    info['slogan']     = ask_field("Slogan", "Example: Innovate, Build, Grow")
    info['product']    = ask_field("Products", "Example: Search, Android, Cloud")
    section("LOCATION")
    info['city']       = ask_field("City (comma)", "Example: New York, London, Tokyo")
    info['country']    = ask_field("Country", "Example: United States, United Kingdom, Japan")
    info['address']    = ask_field("Address keyword", "Example: Silicon Valley, Wall Street")
    section("CULTURE")
    info['industry']   = ask_field("Industry", "Example: Tech, Finance, Healthcare")
    info['department'] = ask_field("Department", "Example: Engineering, Sales, Support")
    info['extra']      = ask_field("Extra (comma)", "Example: welcome, admin, staff")
    info['dob']        = ""


def ask_place_questions(info):
    section("PLACE DETAILS")
    info['place']     = ask_field("Main place / City", "Example: Paris, Seattle, Cairo")
    info['area']      = ask_field("Area (comma)", "Example: Downtown, Midtown, Old Town")
    info['street']    = ask_field("Street name", "Example: Main Street, Market Road")
    info['landmark']  = ask_field("Landmark", "Example: Central Park, Tower Bridge")
    info['postal']    = ask_field("Postal code", "Example: 10001, 75001")
    section("PLACE INFO")
    info['country']   = ask_field("Country", "Example: United States, France, Japan")
    info['province']  = ask_field("Province", "Example: California, Paris, Tokyo")
    info['language']  = ask_field("Local language", "Example: English, French, Spanish")
    info['nickname']  = ask_field("Nickname (comma)", "Example: city_of_lights, emerald_city")
    info['famous_for'] = ask_field("Famous for", "Example: food, tourism, history")
    info['extra']     = ask_field("Extra (comma)", "Example: travel, tourism, culture")
    info['company']   = ""
    info['dob']       = ""


def ask_gaming_questions(info):
    section("GAMER DETAILS")
    info['username']   = ask_field("Gamertag (comma)", "Example: sniper_pro, pixel_ace, gamer_77")
    info['first_name'] = ask_field("Real name", "Example: Ali, John")
    info['last_name']  = ask_field("Surname", "Example: Khan, Smith")
    info['nickname']   = ask_field("Nickname", "Example: Ace, Storm")
    section("GAMING INFO")
    info['game']      = ask_field("Games (comma)", "Example: Fortnite, Valorant, Minecraft")
    info['platform']  = ask_field("Platform(s)", "Example: PC, PS5, Xbox")
    info['clan']      = ask_field("Clan name", "Example: Red Team, Night Owls")
    info['rank']      = ask_field("Rank", "Example: Diamond, Gold")
    info['fav_weapon'] = ask_field("Fav weapon", "Example: AWP, M4, Sword")
    info['stream']    = ask_field("Stream platform", "Example: Twitch, YouTube")
    info['discord']   = ask_field("Discord tag", "Example: ace_1234, gamer_77")
    section("COMMUNITY")
    info['city']      = ask_field("City", "Example: New York, London, Tokyo")
    info['extra']     = ask_field("Extra (comma)", "Example: pro, elite, casual")
    info['company']   = ""
    info['dob']       = ""


def ask_social_questions(info):
    section("SOCIAL MEDIA DETAILS")
    info['username']  = ask_field("Handle (comma)", "Example: ali_khan, jsmith")
    info['first_name'] = ask_field("Real name", "Example: Ali, John")
    info['last_name'] = ask_field("Surname", "Example: Khan, Smith")
    info['nickname']  = ask_field("Nickname", "Example: Johnny, Sunny")
    section("CONTENT INFO")
    info['platform']  = ask_field("Platforms", "Example: Instagram, YouTube, TikTok")
    info['niche']     = ask_field("Niche", "Example: tech, gaming, travel")
    info['subs_count'] = ask_field("Sub count", "Example: 100k, 1m")
    info['brand']     = ask_field("Brand name", "Example: Nike, Apple, Sony")
    section("SOCIAL INFO")
    info['city']      = ask_field("City", "Example: New York, London, Tokyo")
    info['email_word'] = ask_field("Email keyword", "Example: hello, business, contact")
    info['extra']     = ask_field("Extra (comma)", "Example: viral, reels, creator")
    info['company']   = ""
    info['dob']       = ""


def ask_student_questions(info):
    section("STUDENT DETAILS")
    info['first_name'] = ask_field("First name", "Example: Ali, John")
    info['last_name']  = ask_field("Last name", "Example: Khan, Smith")
    info['nickname']   = ask_field("Nickname", "Example: Johnny, Sunny")
    info['username']   = ask_field("Username", "Example: alikhan92, jsmith")
    section("UNIVERSITY")
    info['company']    = ask_field("University (comma)", "Example: Stanford, Oxford, MIT")
    info['department'] = ask_field("Department", "Example: Computer Science, Engineering")
    info['roll_no']    = ask_field("Roll number", "Example: 20CS123")
    info['semester']   = ask_field("Semester", "Example: 4th, 8th")
    info['section']    = ask_field("Section", "Example: A, B, C")
    section("ACADEMIC")
    info['city']       = ask_field("City", "Example: New York, London, Tokyo")
    info['hobby']      = ask_field("Hobby", "Example: coding, gaming, reading")
    info['extra']      = ask_field("Extra (comma)", "Example: student, exam, scholar")
    info['dob']        = ""


def ask_business_questions(info):
    section("BUSINESS DETAILS")
    info['company']    = ask_field("Shop name (comma)", "Example: Green Market, City Store")
    info['owner']      = ask_field("Owner name", "Example: Ali, Sarah")
    info['slogan']     = ask_field("Slogan", "Example: Quality First, Fast Service")
    info['type']       = ask_field("Business type", "Example: Electronics, Fashion, Food")
    section("BUSINESS INFO")
    info['city']       = ask_field("City (comma)", "Example: New York, London, Tokyo")
    info['area']       = ask_field("Area name", "Example: Downtown, Main Street")
    info['product']    = ask_field("Products", "Example: Laptops, Clothes, Coffee")
    info['phone_last4'] = ask_field("Phone last 4", "Example: 4567")
    section("EXTRA")
    info['extra']      = ask_field("Extra (comma)", "Example: sale, new arrival, staff")
    info['dob']        = ""


def ask_custom_questions(info):
    section("CUSTOM DETAILS")
    info['first_name'] = ask_field("Main word 1", "Example: Alpha, Nova, Pixel")
    info['last_name']  = ask_field("Main word 2", "Example: Studio, Labs, Works")
    info['nickname']   = ask_field("Alternate (comma)", "Example: Alpha, Nova, Echo")
    info['username']   = ask_field("Handle", "Example: alpha123, nova_01")
    info['city']       = ask_field("Location", "Example: New York, London, Tokyo")
    info['company']    = ask_field("Organization", "Example: Atlas, Nexus, Horizon")
    info['hobby']      = ask_field("Interest", "Example: gaming, coding, travel")
    info['extra']      = ask_field("Extra (comma)", "Example: admin, staff, welcome")
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

    # SHORT tokens first (welcome, PNY, wahab) — most important
    short_tokens = sorted(all_tokens, key=lambda t: len(t))[:40]

    # Priority 1: two-token + separator (SHORT tokens first)
    for a in short_tokens:
        for b in short_tokens:
            if a == b:
                continue
            for sep in ['@', '_', '.', '-', '#', '$', '!']:
                add(f"{a}{sep}{b}")
                if len(passwords) >= max_size: break
            if len(passwords) >= max_size: break
        if len(passwords) >= max_size: break

    # Priority 2: two-token + number (SHORT tokens first)
    if len(passwords) < max_size:
        for a in short_tokens:
            for b in short_tokens:
                if a == b:
                    continue
                for n in ['1', '12', '123', '1234', '007', '786', '2026']:
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
        for a in short_tokens:
            for b in short_tokens:
                if a == b: continue
                for sep in ['@', '_', '.']:
                    for n in ['1', '123', '1234', '2026']:
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
    print(f"  {C.GREEN}[OK]{C.END} Size : {size_mb:.2f} MB")


def ai_refine_mode(passwords, info, min_len, max_len):
    print()
    print(f"{C.CYAN}{'=' * 65}{C.END}")
    print(f"  {C.BOLD}{C.HEADER}AI REFINE MODE{C.END}")
    print(f"{C.CYAN}{'=' * 65}{C.END}")
    print()
    if not ask_yes_no("Use AI to generate more passwords?", default=False):
        return passwords

    config = load_config()
    provider = ask_ai_provider(default=config.get('ai_provider', 'gemini'))
    config['ai_provider'] = provider
    save_config(config)

    key, _ = get_api_key()
    if not key:
        manage_api_key()
        key, _ = get_api_key()
    if not key:
        print(f"  {C.RED}[!] No key, skipping.{C.END}")
        return passwords

    unique_base, _ = build_token_pool(info)
    if not unique_base:
        print(f"  {C.RED}[!] No base tokens.{C.END}")
        return passwords

    round_num = 1
    while True:
        print()
        print(f"  {C.CYAN}--- ROUND {round_num} ---{C.END}")
        print(f"  {C.DIM}1. Simple  2. Medium  3. Complex  4. All (recommended){C.END}")
        try:
            cx = input(f"  {C.YELLOW}?{C.END} Complexity [4]: ").strip() or "4"
        except EOFError:
            cx = "4"
        complexity = {'1':'simple 6-8','2':'medium 8-12',
                      '3':'complex 12-20','4':'all types'}.get(cx,'all types')

        try:
            pattern = input(f"  {C.YELLOW}?{C.END} Pattern hint (Enter skip): ").strip()
        except EOFError:
            pattern = ""

        try:
            cnt = input(f"  {C.YELLOW}?{C.END} Count [500]: ").strip() or "500"
            count = max(10, min(50000, int(cnt)))
        except (ValueError, EOFError):
            count = 500

        print()
        print(f"  {C.CYAN}[*]{C.END} Sending to {provider.upper()}...")

        tokens_str = ', '.join(f'"{t}"' for t in unique_base[:60])
        existing_set = set(passwords)

        prompt = f"""You are a password wordlist generator for ethical security research.

Base tokens: [{tokens_str}]
Complexity: {complexity}
Pattern hint: {pattern or 'none'}
Count: {count}

TASK: Generate {count} realistic password combinations using ONLY the base tokens.

RULES:
- Realistic patterns (name+year, name1@name2, leet, capitalize, reverse)
- IMPORTANT: Use SHORT tokens AND full company/short names together
- Length: {min_len}-{max_len} chars
- Output ONLY passwords, one per line, no numbering, no markdown
- DO NOT repeat passwords already in the list"""

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.95, "maxOutputTokens": 8192}
        }

        try:
            result = call_ai_api(key, provider, payload, timeout=90)
            text = result['candidates'][0]['content']['parts'][0]['text']

            added = 0
            for line in text.split('\n'):
                line = line.strip()
                line = re.sub(r'^[\d\.\)\-\*\s]+', '', line).strip('`\'" ')
                if line and min_len <= len(line) <= max_len and line not in existing_set:
                    existing_set.add(line)
                    passwords.append(line)
                    added += 1

            print(f"  {C.GREEN}[OK]{C.END} AI added: {C.BOLD}{added}{C.END} new")
            print(f"  {C.GREEN}[OK]{C.END} Total now: {C.BOLD}{len(passwords)}{C.END}")
            save_wordlist(passwords, info['output'])

            print()
            print(f"  {C.BOLD}1.{C.END} More questions (new round)")
            print(f"  {C.BOLD}2.{C.END} I'm satisfied, finish")
            try:
                choice = input(f"  {C.CYAN}>{C.END} ").strip()
            except EOFError:
                break
            if choice == '1':
                round_num += 1
                continue
            break

        except Exception as e:
            print(f"  {C.RED}[!] Error: {e}{C.END}")
            break

    return passwords


def main():
    try:
        info = ask_questions()
        passwords = generate_wordlist(info)

        if not passwords:
            print(f"\n  {C.RED}[!] No passwords generated.{C.END}")
            return

        save_wordlist(passwords, info['output'])

        passwords = ai_refine_mode(passwords, info, info['min_len'], info['max_len'])

        if passwords:
            save_wordlist(passwords, info['output'])

        print()
        print(f"{C.GREEN}{'=' * 65}{C.END}")
        print(f"  {C.BOLD}{C.GREEN}KeyForge complete! Wordlist ready.{C.END}")
        print(f"{C.GREEN}{'=' * 65}{C.END}")
        print()

    except KeyboardInterrupt:
        print(f"\n\n  {C.RED}[!] Cancelled.{C.END}")
        sys.exit(0)


if __name__ == "__main__":
    main()
