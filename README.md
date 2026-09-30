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
- 📝 **Comma-separated multi-values** — `lahore, karachi, london`
- ✅ **Confirmation screen** before generation
- 🌏 **South Asian patterns** (optional) — 786, Allah, Khan
- 🔐 **Leetspeak variants** — `ali` → `4l1`, `@li`
- 🔄 **Reversed words** — `ali` → `ila`
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

All produce the same tokens: `lahore`, `karachi`, `london`

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
umerimran
umer.imran
umer_imran
umer@imran
imran@umer
um3r@1234
umer123
imran123
um3r123
lahore123
cyberster123
umer!
imran!
umer@123
cyberster@123
...
```

## 🤖 AI Refine Mode (Optional)

KeyForge ke paas **AI mode** hai jo Gemini API use karke aur bhi smart passwords banata hai.

### How It Works

1. Base wordlist generate hoti hai (normal flow)
2. End mein poochha jata hai:
   ```
   🤖 AI REFINE MODE
   
   Current wordlist: 65074 passwords
   ? Use AI to generate more targeted passwords? (y/n) [n]: y
   ```
3. AI tumhare base tokens ko leke realistic passwords banata hai
4. Existing list mein add karta hai (duplicates skip karke)
5. Agar satisfied nahi → naya round with different preferences

### Setup — Get Free API Key

1. Jao: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Google account se login karo
3. **"Create API Key"** click karo
4. Copy karo — key `AIzaSy...` se start hoti hai

### Store API Key (3 Options)

**Option 1: Built-in menu (Recommended)**

Jab first time AI mode use karo, tool khud poochta hai:

```
🔑 API KEY MANAGEMENT

  ⚠ No API key configured
  Get free key: https://aistudio.google.com/app/apikey

  Options:
    1. Add / Replace API key
    2. Back

  └─> 1

  ? Paste your API key: AIzaSy...
  [✓] Key saved to: C:\Users\you\.keyforge\config.json
  (Stored locally on your machine only)
```

Key sirf tumhari machine pe save hoti hai: `~/.keyforge/config.json`

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
(CMD restart karna padega)

Linux/Mac — `~/.bashrc` ya `~/.zshrc` mein add karo:
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
    1. Add / Replace API key   ← yahan naya key paste karo
    2. Delete API key
    3. Back
```

**Delete key:**

```
  Options:
    1. Add / Replace API key
    2. Delete API key          ← yahan se delete
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

Jab AI mode start hota hai:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AI REFINEMENT — ROUND 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  What kind of passwords do you need?
    1. Simple & short (ali123, khan@1)
    2. Medium (ali.khan123, khan@2024)
    3. Complex (Um3r@Khan123, cyb3r_2024!)
    4. All types (recommended)

  ? Choose [4]: 4

  Any specific pattern hint? (Enter to skip)
  ? Pattern: name @ company 2024

  How many extra passwords? (10-50000)
  ? Count [500]: 1000
```

### Multi-Round Flow

Pehli round ke baad:

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

Agar `1` dabao → AI **naye sawal** puchega, **naye preferences** ke saath naye passwords banayega. **Duplicates skip honge**.

### Duplicate Prevention

- AI ko explicitly bola jata hai: **"DO NOT use any password already in the existing list"**
- Code level pe bhi filter hai: har AI password existing set mein check hota hai
- **Kabhi bhi duplicate wordlist mein add nahi hoga**

## 🧠 How Generation Works

KeyForge uses a **priority-based multi-phase strategy**:

1. **Phase 1** — Two-token + separator (`welcome@pny`, `ali_khan`)
2. **Phase 2** — Two-token + number (`alikhan123`, `pny786`)
3. **Phase 3** — Simple tokens (`umer`, `imran`)
4. **Phase 4** — token + number (`umer123`)
5. **Phase 5** — token + special (`umer!`)
6. **Phase 6** — token + number + special (`um3r@1234`)
7. **Phase 7** — Capitalize (`Umer123`)
8. **Phase 8** — Reverse (`remu`)
9. **Phase 9** — Three-token combos (`umer_imran_lahore`)
10. **Phase 10** — Long numbers (`umer2024`)

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
  💡 Use commas for multiple values: lahore, karachi, london

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
[?] First name              : umer
[?] Last name / Surname     : imran
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
