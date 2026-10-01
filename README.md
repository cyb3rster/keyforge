<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=KeyForge&fontSize=80&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Smart%20Wordlist%20Generator%20with%20AI&descAlignY=55&descSize=20" width="100%"/>

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&duration=3000&pause=800&color=00D9FF&center=true&vCenter=true&multiline=true&width=750&height=100&lines=Generate+smart+wordlists;Category-based+questions;AI-powered+refinement;Zero+dependencies" alt="Typing SVG" />
</a>

<p>
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-00D9FF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Version-3.0.0-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AI-Gemini-purple?style=for-the-badge&logo=google" />
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

KeyForge supports **8 intelligent categories** — each asks relevant questions:

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
- 🤖 **AI-powered refinement** with Google Gemini
- 📝 **Comma-separated multi-values** — `london, paris, tokyo`
- ✅ **Confirmation screen** before generation
- 🌏 **South Asian patterns** (optional) — 786, Allah, Khan
- 🔐 **Leetspeak variants** — `alex` → `4l3x`, `@lex`
- 🔄 **Reversed words** — `alex` → `xela`
- 📱 Phone, vehicle, username support
- 🎛️ **Length filter** — min/max password length
- ⚡ **Round-robin generation** — every input gets its turn
- 📦 **Zero dependencies** — Python stdlib only
- 🔒 **Local API key storage** — never sent anywhere except Google

## 📖 How to Use

### Basic Flow

```
Choose target category:
  1. 👤  Person
  2. 🏢  Company
  3. 📍  Place
  4. 🎮  Gaming
  5. 📱  Social Media
  6. 🎓  Student
  7. 🏪  Business
  8. 🎯  Custom

? 1

── PERSON DETAILS ──
[?] First name              : alex
[?] Last name / Surname     : smith
[?] Nickname                : al, alex_s
[?] Username                : alexsmith92
[?] Date of birth           : 15081998
[?] City                    : london, paris
[?] Company / School        : google, mit
[?] Hobby                   : cricket, gaming
[?] Extra words             : admin, hello
```

### Comma Support — All Formats Work

```
london, paris, tokyo
london,paris,tokyo
london , paris , tokyo
london; paris; tokyo
```

All produce the same tokens: `london`, `paris`, `tokyo`

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
alex
Alex
ALEX
xela
smith
Smith
SMITH
htims
al
alexsmith
alex.smith
alex_smith
asmith
smithalex
alexsmith92
london
paris
google
mit
cricket
gaming
15081998
150898
1998
alex123
smith123
alex!
smith!
alex@123
smith@123
...
```

## 🤖 AI Refine Mode (Optional)

KeyForge has an **AI mode** that uses the Gemini API to generate even smarter passwords.

### How It Works

1. Base wordlist is generated (normal flow)
2. At the end, the tool asks:
   ```
   🤖 AI REFINE MODE
   
   Current wordlist: 65074 passwords
   ? Use AI to generate more targeted passwords? (y/n) [n]: y
   ```
3. AI takes your base tokens and creates realistic passwords
4. Adds them to the existing list (skipping duplicates)
5. If not satisfied → new round with different preferences

### Setup — Get Free API Key

1. Go to: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Login with Google account
3. Click **"Create API Key"**
4. Copy it — the key starts with `AIzaSy...` or `AQ.Ab8...` (both are valid)

### Store API Key (3 Options)

**Option 1: Built-in menu (Recommended)**

When you first use AI mode, the tool prompts you:

```
🔑 API KEY MANAGEMENT

  ⚠ No API key configured
  Get free key: https://aistudio.google.com/app/apikey

  Options:
    1. Add / Replace API key
    2. Back

  └─> 1

  ? Paste your API key: AIzaSy... or AQ.Ab8...
  [✓] Key saved to: C:\Users\you\.keyforge\config.json
  (Stored locally on your machine only)
```

Key is only saved on your machine: `~/.keyforge/config.json`

**Option 2: Environment Variable (One-time session)**

Windows CMD:
```cmd
set GEMINI_API_KEY=AIzaSy...your_key
python keyforge.py
```

Linux/Mac:
```bash
export GEMINI_API_KEY="AIzaSy...your_key"
python3 keyforge.py
```

**Option 3: Environment Variable (Permanent)**

Windows:
```cmd
setx GEMINI_API_KEY "AIzaSy...your_key"
```
(CMD restart required)

Linux/Mac — add to `~/.bashrc` or `~/.zshrc`:
```bash
export GEMINI_API_KEY="AIzaSy...your_key"
```

### Manage API Key

**Change key:**

```
🔑 API KEY MANAGEMENT
  ✓ Current key : AIzaSy...xyz
  Source       : Local Config

  Options:
    1. Add / Replace API key   ← paste new key here
    2. Delete API key
    3. Back
```

**Delete key:**

```
  Options:
    1. Add / Replace API key
    2. Delete API key          ← delete from here
    3. Back
```

**Manual delete:**

Windows:
```cmd
del %USERPROFILE%\.keyforge\config.json
```

Linux/Mac:
```bash
rm ~/.keyforge/config.json
```

### AI Preferences

When AI mode starts:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AI REFINEMENT — ROUND 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  What kind of passwords do you need?
    1. Simple & short (alex123, smith@1)
    2. Medium (alex.smith123, smith@2024)
    3. Complex (Al3x@Smith123, cyber_2024!)
    4. All types (recommended)

  ? Choose [4]: 4

  Any specific pattern hint? (Enter to skip)
  ? Pattern: name @ company 2024

  How many extra passwords? (10-50000)
  ? Count [500]: 1000
```

### Multi-Round Flow

After the first round:

```
  [✓] AI returned: 847 passwords
  [✓] New added  : 762
  [✓] Total now  : 65836

  What next?
    1. More questions (new round with different preferences)
    2. I'm satisfied, finish
    3. Skip to save & exit

  └─> 1

  [*] Starting new round...
```

If you press `1` → AI asks **new questions**, generates new passwords with **new preferences**. **Duplicates are skipped.**

### Duplicate Prevention

- AI is explicitly told: **"DO NOT use any password already in the existing list"**
- Code-level filter: every AI password is checked against the existing set
- **Duplicates are never added to the wordlist**

## 🧠 How Generation Works

KeyForge uses a **priority-based multi-phase strategy**:

1. **Phase 1** — Two-token + separator (`hello@world`, `alex_khan`)
2. **Phase 2** — Two-token + number (`alexsmith123`, `smith786`)
3. **Phase 3** — Simple tokens (`alex`, `smith`)
4. **Phase 4** — token + number (`alex123`)
5. **Phase 5** — token + special (`alex!`)
6. **Phase 6** — token + number + special (`al3x@1234`)
7. **Phase 7** — Capitalize (`Alex123`)
8. **Phase 8** — Reverse (`xela`)
9. **Phase 9** — Three-token combos (`alex_smith_london`)
10. **Phase 10** — Long numbers (`alex2024`)

**Every input gets fair treatment** — no single token dominates.

## 🔒 Privacy

- **API key:** stored locally only (`~/.keyforge/config.json`)
- **Key never sent** anywhere except Google Gemini API (as required for auth)
- **Base tokens** sent once per AI call to Gemini — no other data
- **Wordlist never uploaded** anywhere
- **No telemetry, no analytics, no tracking**
- **Core tool works 100% offline** — AI mode is optional

## 🆚 KeyForge vs CUPP

| Feature | CUPP | KeyForge |
|:--------|:----:|:--------:|
| Zero dependencies | ❌ | ✅ |
| Single file | ❌ | ✅ |
| Category-based questions | ❌ | ✅ |
| **AI-powered refinement** | ❌ | ✅ |
| Comma multi-values | ❌ | ✅ |
| Confirmation screen | ❌ | ✅ |
| Length filter | ❌ | ✅ |
| Multi-round AI | ❌ | ✅ |
| Duplicate prevention | Partial | ✅ |
| Local API key storage | ❌ | ✅ |
| South Asian patterns | ❌ | ✅ |
| Works on Windows | Partial | ✅ |

## 🎬 Demo

```text
╔═══════════════════════════════════════════════════════════════╗
║  K E Y F O R G E  ─  Wordlist Generator  v3.0.0             ║
╚═══════════════════════════════════════════════════════════════╝

  ⚠  For ethical/authorized use only (own accounts / pentest).
  💡 Leave any field empty to SKIP.
  💡 Use commas for multiple values: london, paris, tokyo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CHOOSE TARGET CATEGORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    1. 👤  Person (default)
    2. 🏢  Company / Organization
    3. 📍  Place / Location
    4. 🎮  Gaming / Gamer
    5. 📱  Social Media / Influencer
    6. 🎓  Student / University
    7. 🏪  Business / Shop
    8. 🎯  Custom

  └─> 1

── PERSON DETAILS ──
[?] First name              : alex
[?] Last name / Surname     : smith
...

  [*] Category        : PERSON
  [*] Base tokens     : 24
  [*] Total variations: 168
  [*] Length range    : 6-25 chars
  [*] Max passwords   : 200000
  [*] Generating...

  [✓] Total passwords generated: 200000
  [✓] Saved: C:\Users\you\Downloads\keyforge\wordlist.txt
  [✓] Size : 2.14 MB

═══════════════════════════════════════════════════════════════════
  🤖 AI REFINE MODE
═══════════════════════════════════════════════════════════════════

  Current wordlist: 200000 passwords
  ? Use AI to generate more targeted passwords? (y/n) [n]: y
  ...
```

## ⚠️ Disclaimer

**For ethical/authorized use only.**

Use it on:
- ✅ Your own accounts
- ✅ Authorized penetration testing
- ✅ CTF / Lab environments
- ✅ Learning security

**NOT** for:
- ❌ Hacking someone else's account
- ❌ Unauthorized access
- ❌ Any illegal activity

**Misuse is illegal.** In Pakistan, unauthorized access is a crime under **PECA Act 2016** (3-7 years jail + fine). The author is **not responsible** for misuse.

## 📄 License

MIT — see [LICENSE](LICENSE).

## 🤝 Contributing

Pull requests welcome! For major changes, open an issue first.

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Open Pull Request

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer&animation=fadeIn" width="100%"/>

**Made with ❤️ by [cyb3rster](https://github.com/cyb3rster)**

</div>
