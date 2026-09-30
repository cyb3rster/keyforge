<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=KeyForge&fontSize=80&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Smart%20Personal%20Wordlist%20Generator&descAlignY=55&descSize=20" width="100%"/>

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&duration=3000&pause=800&color=00D9FF&center=true&vCenter=true&multiline=true&width=750&height=100&lines=Generate+smart+wordlists+in+seconds;Category-based+intelligent+generation;Zero+dependencies+%7C+Single+file" alt="Typing SVG" />
</a>

<p>
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-00D9FF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Version-2.0.0-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Dependencies-Zero-brightgreen?style=for-the-badge" />
</p>

</div>

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/cyb3rster/keyforge.git
```

### 2. Enter the folder

```bash
cd keyforge
```

### 3. Run the tool

```bash
python keyforge.py
```

> **No installation. No dependencies. No setup.** Just Python 3.8+.

## 🖥️ Platform Commands

### 🐧 Linux

```bash
python3 keyforge.py
```

### 🍎 macOS

```bash
python3 keyforge.py
```

### 🪟 Windows

```bash
python keyforge.py
```

## 🎯 Categories

KeyForge now supports **8 intelligent categories** — each asks relevant questions:

| # | Category | What it asks |
|---|----------|--------------|
| 1 | 👤 **Person** | Name, DOB, family, city, hobby |
| 2 | 🏢 **Company** | Company, CEO, founder, slogan, products |
| 3 | 📍 **Place** | City, area, street, landmark, famous-for |
| 4 | 🎮 **Gaming** | Gamertag, games, platform, clan, rank |
| 5 | 📱 **Social Media** | Handle, niche, platform, subscribers |
| 6 | 🎓 **Student** | Name, university, roll no, department |
| 7 | 🏪 **Business** | Shop name, owner, slogan, products |
| 8 | 🎯 **Custom** | General questions only |

## ✨ Features

- 🎯 **Category-based** intelligent questions
- 📝 **Comma-separated multi-values** — `lahore, karachi, london`
- ✅ **Confirmation screen** before generation
- 🌏 **South Asian patterns** (optional) — 786, Allah, Khan
- 🔐 **Leetspeak variants** — `ali` → `4l1`, `@li`
- 🔄 **Reversed words** — `ali` → `ila`
- 📱 Phone, vehicle, username support
- 🎛️ **Length filter** — min/max password length
- ⚡ **Round-robin generation** — every input gets its turn
- 📦 **Zero dependencies** — Python stdlib only

## 📖 How to Use

### Example: Person Wordlist

```
Choose target category:
  1. 👤  Person
  2. 🏢  Company
  3. 📍  Place
  4. 🎮  Gaming
  ...

? 1

── PERSON DETAILS ──
[?] First name              : umer
[?] Last name / Surname     : imran
[?] Nickname                : um3r, umer_khan
[?] Username                : jus_um3rr
[?] Date of birth           : 03082005
[?] City                    : lahore, karachi
[?] Company / School        : cyberster, virtual university
[?] Hobby                   : hacking, cybersecurity
[?] Extra words             : cyb3r, um3r, cyberster
```

### Comma Support — All Formats Work

```
lahore, karachi, london
lahore,karachi,london
lahore , karachi , london
lahore; karachi; london
```

All of these produce the same tokens: `lahore`, `karachi`, `london`

### Confirmation Screen

```
═══════════════════════════════════════════════════════════
  CONFIRMATION
═══════════════════════════════════════════════════════════
  Category: PERSON

  ✓ Filled : First name, Last name, Nickname, City, Company, Hobby
  ✗ Skipped: Partner, Pet, Child, Phone, Vehicle

  You left 5 field(s) EMPTY.
  ? Run with these skips? (y/n) [y]: y
```

### Output

Generated `wordlist.txt` will contain:

```
umer
Umer
UMER
remu
imran
Imran
IMRAN
narmi
um3r
Um3r
jus_um3rr
lahore
karachi
cyberster
virtual
university
hacking
cybersecurity
03082005
030805
2005
umer123
imran123
um3r123
lahore123
cyberster123
umer!
imran!
umer@123
um3r@1234
umerimran
umer.imran
um3r_umer
cyberster@123
...
```

## 🆚 KeyForge vs CUPP

| Feature | CUPP | KeyForge |
|:--------|:----:|:--------:|
| Zero dependencies | ❌ | ✅ |
| Single file | ❌ | ✅ |
| **Category-based questions** | ❌ | ✅ |
| **Comma multi-values** | ❌ | ✅ |
| Examples in prompts | ❌ | ✅ |
| Confirmation screen | ❌ | ✅ |
| Length filter | ❌ | ✅ |
| Round-robin generation | ❌ | ✅ |
| South Asian patterns | ❌ | ✅ |
| Reverse words | ❌ | ✅ |
| Phone last 4 | ❌ | ✅ |
| Vehicle number | ❌ | ✅ |
| Works on Windows | Partial | ✅ |

## 🎬 Demo

```text
╔═══════════════════════════════════════════════════════════════╗
║  K E Y F O R G E  ─  Smart Wordlist Generator  v2.0.0        ║
╚═══════════════════════════════════════════════════════════════╝

  ⚠  For ethical/authorized use only (own accounts / pentest).
  💡 Leave any field empty to SKIP.
  💡 Use commas for multiple values: lahore, karachi, london

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CHOOSE TARGET CATEGORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  What do you want to generate a wordlist for?

    1. 👤  Person (default)
       General person — name, DOB, family, city
    2. 🏢  Company / Organization
       Business name, CEO, founder, slogan, location
    3. 📍  Place / Location
       City, street, landmarks, area names
    4. 🎮  Gaming / Gamer
       Gamertag, favorite games, platform, clan
    5. 📱  Social Media / Influencer
       Handle, niche, platform, subscribers
    6. 🎓  Student / University
       Student name, university, roll no, department
    7. 🏪  Business / Shop
       Shop name, owner, address, products
    8. 🎯  Custom
       Answer general questions only

  └─> 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PERSON DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌─ First name
  │  Example: ali, ahmed, john
  └─> umer

  ┌─ Last name / Surname
  │  Example: khan, smith, malik
  └─> imran

  ...

  [*] Category        : PERSON
  [*] Base tokens     : 24
  [*] Total variations: 168
  [*] Length range    : 6-25 chars
  [*] Max passwords   : 200000
  [*] Generating...

  [✓] Total passwords generated: 200000
  [✓] Saved: C:\Users\umeri\Downloads\keyforge\wordlist.txt
  [✓] Size : 2.14 MB

  # ═════════════════════════════════════════════
#  AI FEATURE — Gemini API
# ═════════════════════════════════════════════

GEMINI_MODEL = "gemini-1.5-flash-latest"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".keyforge")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


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
        section("🔑 API KEY MANAGEMENT")
        if key:
            masked = key[:8] + '...' + key[-4:] if len(key) > 12 else '***'
            src_label = 'Environment Variable (GEMINI_API_KEY)' if source == 'env' else f'Local Config ({CONFIG_FILE})'
            print(f"  {C.GREEN}✓{C.END} Current key : {C.BOLD}{masked}{C.END}")
            print(f"  {C.DIM}Source       : {src_label}{C.END}")
        else:
            print(f"  {C.YELLOW}⚠{C.END} No API key configured")
            print(f"  {C.DIM}Get free key: https://aistudio.google.com/app/apikey{C.END}")
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
            choice = input(f"  {C.CYAN}└─>{C.END} ").strip()
        except EOFError:
            return
        if choice == '1':
            print()
            print(f"  {C.DIM}Get free key: https://aistudio.google.com/app/apikey{C.END}")
            print()
            try:
                new_key = input(f"  {C.YELLOW}?{C.END} Paste your API key: ").strip()
            except EOFError:
                continue
            if not new_key:
                print(f"  {C.RED}[!] Empty. Cancelled.{C.END}")
                continue
            config = load_config()
            config['gemini_api_key'] = new_key
            if save_config(config):
                print(f"  {C.GREEN}[✓]{C.END} Key saved to: {CONFIG_FILE}")
                print(f"  {C.DIM}(Stored locally on your machine only){C.END}")
            input(f"\n  Press Enter to continue...")
        elif choice == '2' and key and source == 'file':
            if ask_yes_no("Delete saved API key?", default=False):
                config = load_config()
                config.pop('gemini_api_key', None)
                save_config(config)
                print(f"  {C.GREEN}[✓]{C.END} Key deleted.")
            input(f"\n  Press Enter to continue...")
        elif choice == str(max_c):
            return
        else:
            print(f"  {C.RED}[!] Invalid choice.{C.END}")


def call_gemini(api_key, category, base_tokens, existing_set, prefs, round_num=1):
    """Call Gemini API. Returns list of new unique passwords."""
    tokens_str = ', '.join(f'"{t}"' for t in base_tokens[:60])
    pattern_hint = prefs.get('pattern', '') or 'none'
    complexity = prefs.get('complexity', 'all types')
    count = prefs.get('count', 500)

    prompt = f"""You are a password wordlist generator for ethical security research.

Context:
- Category: {category}
- Base tokens: [{tokens_str}]
- Complexity: {complexity}
- Pattern hint: {pattern_hint}
- Round: {round_num}

TASK: Generate {count} realistic password combinations using ONLY the base tokens above.

RULES:
1. Combine tokens creatively — mix case, add numbers, symbols, leet-speak.
2. Use realistic patterns real humans choose:
   - name + year (ali2024, ali.1998)
   - name1 + sep + name2 (ali@khan, ali_khan)
   - leet-speak (ali -> 4l1, @li)
   - capitalized (Ali@Khan123)
   - reversed + number (ila123)
   - token + number + special (ali@123)
3. Length: 6-25 chars.
4. NO markdown, NO explanations, NO numbering, NO bullet points.
5. Output ONLY raw passwords, one per line.
6. NO duplicates with the base tokens.
7. DO NOT use any password already in the existing list.

Output format: raw passwords only, one per line, nothing else."""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.95,
            "maxOutputTokens": min(8192, count * 3),
        }
    }
    url = f"{GEMINI_URL}?key={api_key}"
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data,
                                 headers={'Content-Type': 'application/json'},
                                 method='POST')
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            result = json.loads(resp.read().decode('utf-8'))
        text = result['candidates'][0]['content']['parts'][0]['text']
        passwords = []
        for line in text.split('\n'):
            line = line.strip()
            line = re.sub(r'^[\d\.\)\-\*\s]+', '', line)
            line = line.strip('`\'" ')
            if line and 4 <= len(line) <= 50:
                if line not in existing_set:
                    passwords.append(line)
        return passwords
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')
        print(f"  {C.RED}[!] API error {e.code}: {body[:200]}{C.END}")
        return []
    except urllib.error.URLError as e:
        print(f"  {C.RED}[!] Network error: {e.reason}{C.END}")
        return []
    except Exception as e:
        print(f"  {C.RED}[!] Error: {e}{C.END}")
        return []


def ask_ai_preferences(round_num=1):
    section(f"AI REFINEMENT — ROUND {round_num}")

    prefs = {}
    print(f"  {C.DIM}What kind of passwords do you need?{C.END}")
    print(f"    {C.BOLD}1.{C.END} Simple & short (ali123, khan@1)")
    print(f"    {C.BOLD}2.{C.END} Medium (ali.khan123, khan@2024)")
    print(f"    {C.BOLD}3.{C.END} Complex (Um3r@Khan123, cyb3r_2024!)")
    print(f"    {C.BOLD}4.{C.END} All types (recommended)")
    print()
    try:
        cx = input(f"  {C.YELLOW}?{C.END} Choose [4]: ").strip() or "4"
    except EOFError:
        cx = "4"
    complexity_map = {
        '1': 'simple, short (6-8 chars), predictable',
        '2': 'medium (8-12 chars), mixed case',
        '3': 'complex (12-20 chars), leet, special chars',
        '4': 'all types — simple, medium, complex mixed',
    }
    prefs['complexity'] = complexity_map.get(cx, complexity_map['4'])

    print()
    print(f"  {C.DIM}Any specific pattern hint? (Enter to skip){C.END}")
    try:
        prefs['pattern'] = input(f"  {C.YELLOW}?{C.END} Pattern: ").strip()
    except EOFError:
        prefs['pattern'] = ""

    print()
    print(f"  {C.DIM}How many extra passwords? (10-50000){C.END}")
    try:
        n = input(f"  {C.YELLOW}?{C.END} Count [500]: ").strip() or "500"
        prefs['count'] = max(10, min(50000, int(n)))
    except (EOFError, ValueError):
        prefs['count'] = 500

    return prefs


def ai_refine_mode(passwords, info, min_len, max_len):
    """Main AI refinement loop with multi-round support."""
    print()
    print(f"{C.CYAN}{'═' * 65}{C.END}")
    print(f"  {C.BOLD}{C.HEADER}🤖 AI REFINE MODE{C.END}")
    print(f"{C.CYAN}{'═' * 65}{C.END}")
    print()
    print(f"  Current wordlist: {C.BOLD}{len(passwords)}{C.END} passwords")
    print(f"  {C.DIM}AI tumhare input ke basis pe aur smart passwords banayega.{C.END}")
    print(f"  {C.DIM}Requires: internet + free Gemini API key.{C.END}")
    print()

    if not ask_yes_no("Use AI to generate more targeted passwords?", default=False):
        return passwords

    api_key, source = get_api_key()
    if not api_key:
        print(f"  {C.YELLOW}[!] No API key configured.{C.END}")
        if ask_yes_no("Set up API key now?", default=True):
            manage_api_key()
            api_key, source = get_api_key()
        if not api_key:
            print(f"  {C.RED}[!] Skipping AI mode.{C.END}")
            return passwords

    _, _ = build_token_pool(info)
    unique_base, _ = build_token_pool(info)
    if not unique_base:
        print(f"  {C.RED}[!] No base tokens.{C.END}")
        return passwords

    round_num = 1
    while True:
        prefs = ask_ai_preferences(round_num)

        section(f"AI GENERATING — ROUND {round_num}")
        print(f"  {C.CYAN}[*]{C.END} Sending request...")
        print(f"  {C.CYAN}[*]{C.END} Requesting {prefs['count']} passwords")
        print()

        existing_set = set(passwords)
        new_passwords = call_gemini(api_key, info.get('category', 'custom'),
                                     unique_base, existing_set, prefs, round_num)

        if not new_passwords:
            print(f"  {C.RED}[!] AI returned nothing.{C.END}")
            if not ask_yes_no("Try again?", default=True):
                break
            round_num += 1
            continue

        added = 0
        for pw in new_passwords:
            pw = pw.strip()
            if not pw:
                continue
            if not (min_len <= len(pw) <= max_len):
                continue
            if pw in existing_set:
                continue
            existing_set.add(pw)
            passwords.append(pw)
            added += 1

        print(f"  {C.GREEN}[✓]{C.END} AI returned: {C.BOLD}{len(new_passwords)}{C.END}")
        print(f"  {C.GREEN}[✓]{C.END} New added  : {C.BOLD}{added}{C.END}")
        print(f"  {C.GREEN}[✓]{C.END} Total now  : {C.BOLD}{len(passwords)}{C.END}")

        save_wordlist(passwords, info['output'])

        print()
        print(f"  {C.BOLD}What next?{C.END}")
        print(f"    1. More questions (new round with different preferences)")
        print(f"    2. I'm satisfied, finish")
        print(f"    3. Skip to save & exit")
        print()
        try:
            choice = input(f"  {C.CYAN}└─>{C.END} ").strip()
        except EOFError:
            break

        if choice == '1':
            round_num += 1
            print(f"\n  {C.CYAN}[*]{C.END} Starting new round...")
            continue
        else:
            break

    return passwords

═════════════════════════════════════════════════════════════
  ✅ KeyForge complete! Wordlist ready.
═════════════════════════════════════════════════════════════
```

## 🧠 How Generation Works

KeyForge uses a **round-robin multi-phase strategy**:

1. **Phase 1** — Simple tokens (`umer`, `imran`, `lahore`)
2. **Phase 2** — `token + number` (`umer123`, `imran123`)
3. **Phase 3** — `token + special` (`umer!`, `imran@`)
4. **Phase 4** — `token + number + special` (`um3r@1234`)
5. **Phase 5** — Capitalized (`Umer123`)
6. **Phase 6** — Reversed (`remu`)
7. **Phase 7** — Two-token combos (`umerimran`, `umer.imran`)
8. **Phase 8** — Two-token + number + special (`um3r@imran123`)
9. **Phase 9** — Long numbers (`umer2024`)
10. **Phase 10** — Special + number (`um3r@1234`)

**Every input gets fair treatment** — no single token dominates.

## ⚠️ Disclaimer

**For ethical/authorized use only.**

Use it on:
- ✅ Your own accounts
- ✅ Authorized penetration testing
- ✅ CTF / Lab environments
- ✅ Learning security

**Misuse is illegal.** In Pakistan, unauthorized access is a crime under **PECA Act 2016** (3-7 years jail + fine).

## 📄 License

MIT — see [LICENSE](LICENSE).

## 🤝 Contributing

Pull requests welcome! For major changes, open an issue first.

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer&animation=fadeIn" width="100%"/>

**Made with ❤️ by [cyb3rster](https://github.com/cyb3rster)**

</div>
