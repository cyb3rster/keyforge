<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=KeyForge&fontSize=80&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Smart%20Personal%20Wordlist%20Generator&descAlignY=55&descSize=20" width="100%"/>

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&duration=3000&pause=800&color=00D9FF&center=true&vCenter=true&multiline=true&width=700&height=100&lines=Generate+smart+wordlists+in+seconds;CUPP+alternative+with+more+features;Zero+dependencies+%7C+Single+file" alt="Typing SVG" />
</a>

<p>
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-00D9FF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Dependencies-Zero-brightgreen?style=for-the-badge" />
</p>

</div>

## ⚡ Quick Start

**3 commands. That's it.**

```bash
git clone https://github.com/cyb3rster/keyforge.git
cd keyforge
python keyforge.py
```

> **No installation. No dependencies. No setup.** Just Python 3.8+.

## 🖥️ Platform Commands

| Platform | Command |
|----------|---------|
| 🐧 **Linux** | `python3 keyforge.py` |
| 🍎 **macOS** | `python3 keyforge.py` |
| 🪟 **Windows** | `python keyforge.py` |

## ✨ Features

- 🎯 Interactive prompts with **examples**
- ✅ **Confirmation** before generation (see skipped fields)
- 🌏 **South Asian** patterns (786, Allah, Khan, Malik)
- 🔐 **Leetspeak** variants (`ali` → `4l1`, `@li`)
- 🔄 **Reversed** words (`ali` → `ila`)
- 📱 Phone **last 4** digits
- 🚗 **Vehicle** number
- 👤 Username / Handle field
- 🛡️ Safe skip (empty = auto skip)
- 📦 **Zero dependencies** — only Python stdlib

## 📖 How to Use

**1. Clone & Run:**

```bash
git clone https://github.com/cyb3rster/keyforge.git
cd keyforge
python keyforge.py
```

**2. Enter info** (any field can be skipped with Enter):

```
── BASIC INFO ──
[?] First name              : ali
    └─ Example: ali, ahmed, john
[?] Last name / Surname     : khan
    └─ Example: khan, smith, malik
[?] Nickname                : 
    └─ Example: alu, sunny, jr
...
```

**3. Confirm skipped fields:**

```
=================================================================
  CONFIRMATION
=================================================================
  ✓ Filled : First name, Last name, City
  ✗ Skipped: Nickname, Username, Date of birth, ...

  You left 11 field(s) EMPTY. They will be skipped.
  Run with these skips? (y/n) [y]: y
```

**4. Wordlist generated:** `wordlist.txt`

## 🎬 Example Output

Input:
```
First name : ali
Last name  : khan
DOB        : 15081998
City       : lahore
```

Generated `wordlist.txt` contains:
```
ali
Ali
ALI
khan
Khan
alikhan
ali.khan
ali_khan
akhan
khanali
ali123
ali@123
ali786
4l1
@li
ali1998
15081998
150898
1998
alikhan786
...
```

## 🆚 KeyForge vs CUPP

| Feature | CUPP | KeyForge |
|:--------|:----:|:--------:|
| Zero dependencies | ❌ | ✅ |
| Single file | ❌ | ✅ |
| Examples in prompts | ❌ | ✅ |
| Confirmation screen | ❌ | ✅ |
| South Asian patterns | ❌ | ✅ |
| Reverse words | ❌ | ✅ |
| Phone last 4 | ❌ | ✅ |
| Vehicle number | ❌ | ✅ |
| Username field | ❌ | ✅ |
| Works on Windows | Partial | ✅ |

## ⚠️ Disclaimer

**For ethical/authorized use only.**

Use it on:
- ✅ Your own accounts
- ✅ Authorized penetration testing
- ✅ CTF / Lab environments
- ✅ Learning security

**Misuse is illegal.** In Pakistan, unauthorized access is a crime under PECA Act 2016.

## 📄 License

MIT — see [LICENSE](LICENSE).

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first.

## ⭐ Show your support

Give a ⭐️ if this project helped you!

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer&animation=fadeIn" width="100%"/>

**Made with ❤️ by [cyb3rster](https://github.com/cyb3rster)**

</div>
