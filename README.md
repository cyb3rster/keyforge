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
