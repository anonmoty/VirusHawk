# VirusHawk
<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!--                        VIRUSHAWK - README.md                            -->
<!--              Professional Security Research Documentation               -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->

<div align="center">

<!-- Animated Header Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0a0a,50:FF6B00,100:0a0a0a&height=220&section=header&text=VIRUSHAWK&fontSize=80&fontColor=00BFFF&animation=fadeIn&fontAlignY=35&desc=Analyze%20%7C%20Detect%20%7C%20Defend&descAlignY=58&descSize=18&descColor=00BFFF" width="100%" />

<!-- Typing Animation -->
<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&weight=800&size=24&duration=2500&pause=700&color=00BFFF&center=true&vCenter=true&multiline=true&width=750&height=110&lines=%5B%2B%5D+Initializing+VirusHawk...;%5B%2B%5D+Loading+analysis+modules...;%5B%2B%5D+Scanning+suspicious+file...;%5B%2B%5D+Threat+Analysis+Complete+%5B%E2%9C%94%5D" alt="Typing SVG" />

<br>

<!-- Status Badges -->
<p>
<img src="https://img.shields.io/badge/VERSION-1.0.0-FF6B00?style=for-the-badge&labelColor=0a0a0a&logo=gitbook&logoColor=00BFFF" />
<img src="https://img.shields.io/badge/PYTHON-3.8%2B-FF6B00?style=for-the-badge&labelColor=0a0a0a&logo=python&logoColor=00BFFF" />
<img src="https://img.shields.io/badge/LICENSE-MIT-FF6B00?style=for-the-badge&labelColor=0a0a0a&logo=opensourceinitiative&logoColor=00BFFF" />
<img src="https://img.shields.io/badge/STATUS-ACTIVE-FF6B00?style=for-the-badge&labelColor=0a0a0a&logo=statuspage&logoColor=00BFFF" />
</p>

<p>
<img src="https://img.shields.io/badge/PLATFORM-LINUX%20%7C%20WIN%20%7C%20MAC-FF6B00?style=for-the-badge&labelColor=0a0a0a&logo=linux&logoColor=00BFFF" />
<img src="https://img.shields.io/badge/MALWARE-ANALYSIS-FF6B00?style=for-the-badge&labelColor=0a0a0a&logo=hackaday&logoColor=00BFFF" />
<img src="https://img.shields.io/badge/THREAT-INTEL-FF6B00?style=for-the-badge&labelColor=0a0a0a&logo=target&logoColor=00BFFF" />
</p>

<br>

<!-- Matrix Rain GIF -->
<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%" />

</div>

---

<div align="center">

```ascii
██╗   ██╗██╗██████╗ ██╗   ██╗███████╗██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗
██║   ██║██║██╔══██╗██║   ██║██╔════╝██║  ██║██╔══██╗██║    ██║██║ ██╔╝
██║   ██║██║██████╔╝██║   ██║███████╗███████║███████║██║ █╗ ██║█████╔╝ 
██║   ██║██║██╔══██╗██║   ██║╚════██║██╔══██║██╔══██║██║███╗██║██╔═██╗ 
╚██████╔╝██║██║  ██║╚██████╔╝███████║██║  ██║██║  ██║╚███╔███╔╝██║  ██╗
 ╚═════╝ ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝

                    [ Analyze | Detect | Defend ]
```

</div>

---

## ⚠️ Legal Disclaimer

<div align="center">

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   VIRUSHAWK is a malware analysis and threat detection tool built    ║
║   for EDUCATIONAL and RESEARCH purposes only.                        ║
║                                                                      ║
║   ▸ Use ONLY on files you own or have permission to analyze.         ║
║   ▸ Analyzing malware you don't own is ILLEGAL.                      ║
║   ▸ Always follow ethical guidelines and local laws.                 ║
║   ▸ The author is NOT responsible for any misuse or damage.          ║
║                                                                      ║
║   Analyze responsibly. Learn ethically. Defend proactively.          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

</div>

---

## 🎯 Overview

> **VIRUSHAWK** is a Python-based **malware analysis and threat detection framework** designed for **security researchers, malware analysts, and incident responders**. It provides a modular environment to inspect suspicious files, extract indicators, and identify potential threats — all in a controlled, ethical manner.

Whether you're analyzing a suspicious executable or studying malware behavior in a sandbox — VirusHawk gives you the **vision and precision** you need.

---

## ✨ Core Features

<div align="center">

| | Feature | Description |
|:---:|:---|:---|
| 🔍 | **File Analysis** | Inspects suspicious files efficiently |
| 🧬 | **Hash Extraction** | Generates MD5, SHA1, SHA256 |
| 🧪 | **String Extraction** | Pulls readable strings from binaries |
| 🛡️ | **VirusTotal Lookup** | Checks hashes against VT database |
| 📡 | **Network Indicators** | Extracts URLs, IPs, domains |
| 🧰 | **PE Analysis** | Examines PE headers and sections |
| ⚡ | **Multi-Threaded Engine** | Fast parallel analysis |
| 📊 | **Live Progress Bar** | Real-time terminal feedback |
| 📝 | **JSON Reports** | Structured, machine-readable output |
| 🎨 | **Hacker Terminal UI** | Orange + Blue aesthetic |

</div>

---

## 🚀 Installation

<div align="center">
<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&weight=700&size=18&duration=2000&pause=500&color=00BFFF&center=true&vCenter=true&width=500&lines=%5B%2B%5D+Installing+VirusHawk...;%5B%2B%5D+Almost+there...;%5B%E2%9C%94%5D+Ready+to+analyze." alt="Installing" />
</div>

### ⚡ One-Line Install

```bash
git clone https://github.com/anonmoty/VirusHawk.git && cd VirusHawk && pip install -r requirements.txt && python virushawk.py --help
```

### 🐧 Linux / 🍎 macOS

```bash
# Step 1 — Clone the repo
git clone https://github.com/anonmoty/VirusHawk.git

# Step 2 — Enter the directory
cd VirusHawk

# Step 3 — Install dependencies
pip install -r requirements.txt

# Step 4 — Start analyzing
python virushawk.py --help
```

### 🪟 Windows (PowerShell)

```powershell
git clone https://github.com/anonmoty/VirusHawk.git
cd VirusHawk
pip install -r requirements.txt
python virushawk.py --help
```

---

## 🎯 Usage

```bash
# Analyze a suspicious file
python virushawk.py --file suspicious.exe

# Hash only
python virushawk.py --file sample.bin --hash

# Extract strings
python virushawk.py --file sample.bin --strings

# Full analysis
python virushawk.py --file suspicious.exe --full --output reports/analysis.json

# VirusTotal lookup
python virushawk.py --file sample.bin --vt
```

### CLI Flags

| Flag | Description |
|:---|:---|
| `--file` | Path to suspicious file |
| `--hash` | Extract file hashes only |
| `--strings` | Extract readable strings |
| `--full` | Run full analysis |
| `--vt` | Lookup on VirusTotal |
| `--output` | Report output path |
| `--verbose` | Enable verbose logging |
| `--help` | Show help menu |

---

## 🧠 How It Works

```mermaid
graph TD
    A[Start] --> B[Load File]
    B --> C[Hash Extraction]
    C --> D[String Extraction]
    D --> E[PE Analysis]
    E --> F{Threat Detected?}
    F -->|Yes| G[Log Indicators]
    F -->|No| H[Mark as Clean]
    G --> I[Generate Report]
    H --> I
    I --> J[Done]

    style A fill:#1a0d00,stroke:#FF6B00,color:#00BFFF
    style G fill:#1a0d00,stroke:#FF6B00,color:#00BFFF
    style J fill:#1a0d00,stroke:#FF6B00,color:#00BFFF
```

1. **Load** — Reads the suspicious file
2. **Hash** — Generates MD5, SHA1, SHA256
3. **Strings** — Extracts readable text
4. **Analyze** — Examines PE headers and sections
5. **Detect** — Identifies suspicious indicators
6. **Report** — Displays structured findings

---

## 📁 Project Structure

```
VirusHawk/
├── virushawk.py              # Main entry point
├── core/
│   ├── __init__.py
│   ├── analyzer.py           # Analysis engine
│   ├── hasher.py             # Hash generator
│   ├── strings.py            # String extractor
│   └── reporter.py           # Report generator
├── payloads/                 # Sample files for testing
├── reports/                  # Generated reports
├── tests/                    # Unit tests
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 📸 Demo

<div align="center">

```
╔═════════════════════════════════════════════════════════════╗
║  ██╗   ██╗██╗██████╗ ██╗   ██╗███████╗██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗ ║
║  ██║   ██║██║██╔══██╗██║   ██║██╔════╝██║  ██║██╔══██╗██║    ██║██║ ██╔╝ ║
║  ██║   ██║██║██████╔╝██║   ██║███████╗███████║███████║██║ █╗ ██║█████╔╝  ║
║  ██║   ██║██║██╔══██╗██║   ██║╚════██║██╔══██║██╔══██║██║███╗██║██╔═██╗  ║
║  ╚██████╔╝██║██║  ██║╚██████╔╝███████║██║  ██║██║  ██║╚███╔███╔╝██║  ██╗ ║
║   ╚═════╝ ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝ ║
╚═════════════════════════════════════════════════════════════╝

[✓] File: suspicious.exe
[✓] Size: 245 KB
[✓] Type: PE32 Executable
[→] Analyzing...

[████████████████████████░░░░░░] 80% | Analyzing...
[✓] MD5:  d41d8cd98f00b204e9800998ecf8427e
[✓] SHA256: e3b0c44298fc1c149afbf4c8996fb924...
[!] Suspicious: Embedded URL found
[!] Suspicious: Base64 payload detected
[✓] Analysis complete in 3.21s
[✓] Report: reports/analysis_2024.json

        Stay Vigilant! 🛡️
```

</div>

---

## 🛠️ Requirements

```txt
requests>=2.28.0
colorama>=0.4.6
tqdm>=4.65.0
rich>=13.0.0
pefile>=2023.2.7
```

Install:

```bash
pip install -r requirements.txt
```

---

## 🎨 Hacker Terminal Theme

VirusHawk uses an **orange + electric blue** theme by default:

```python
THEME = {
    "primary":   "\033[38;5;208m",  # Neon Orange
    "secondary": "\033[38;5;39m",   # Electric Blue
    "accent":    "\033[38;5;214m",  # Amber
    "error":     "\033[38;5;196m",  # Red
    "warning":   "\033[38;5;220m",  # Yellow
    "info":      "\033[38;5;39m",   # Blue
    "reset":     "\033[0m",         # Reset
}
```

---

## 🔥 Power User Tips

### Combine with Other Tools

```bash
# VirusHawk + YARA
python virushawk.py --file sample.bin --full
yara -r rules/ sample.bin

# VirusHawk + VirusTotal API
python virushawk.py --file sample.bin --vt --output vt_report.json
```

### Sandbox Analysis

```bash
# Run in isolated VM
python virushawk.py --file malware.exe --full --output report.json
```

---

## 🐛 Security Research Workflow

VirusHawk fits perfectly into your analysis pipeline:

```
1. Sample Collection     →  MalwareBazaar / VT
2. Static Analysis       →  VirusHawk  ← you are here
3. Dynamic Analysis      →  Cuckoo / Any.Run
4. Rule Creation         →  YARA
5. Threat Intel Sharing  →  MISP
```

### Use Cases for Researchers

- 🔍 **Static analysis** of suspicious files
- 📜 **Indicator extraction** for threat intel
- 🗺️ **PE structure mapping** for reverse engineering
- 🧪 **AV evasion testing** in safe labs
- 📊 **Structured reports** for documentation

---

## 🗺️ Roadmap

- [x] File hash extraction
- [x] String extraction
- [x] PE header analysis
- [x] JSON report generation
- [x] Hacker terminal UI
- [ ] YARA rule integration
- [ ] VirusTotal API support
- [ ] Sandbox integration
- [ ] Docker image
- [ ] Web dashboard

---

## 🤝 Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create your branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

## 🙏 Credits

- **Author:** [@anonmoty](https://github.com/anonmoty)
- **Inspired by:** The malware research community
- **Built with:** Python, caffeine, and curiosity ☕

---

<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&weight=800&size=22&duration=3000&pause=1000&color=00BFFF&center=true&vCenter=true&width=600&lines=Stay+Vigilant.;Analyze+Ethically.;Defend+Proactively!+%F0%9F%9B%A1%EF%B8%8F" alt="Footer" />

<br><br>

### ⭐ If this tool helped you, drop a star!

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0a0a,50:FF6B00,100:0a0a0a&height=120&section=footer" width="100%" />

</div>

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!--                        VIRUSHAWK - README.md                            -->
<!--              Professional Malware Analysis Documentation                -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->

<div align="center">

# 🦅 VIRUSHAWK

### `Analyze • Detect • Defend`

**A Python-based malware analysis and threat detection framework for security researchers.**

[![Version](https://img.shields.io/badge/version-1.0.0-red?style=flat-square)](https://github.com/anonmoty/VirusHawk)
[![Python](https://img.shields.io/badge/python-3.8+-green?style=flat-square)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20win%20%7C%20mac-red?style=flat-square)](https://github.com/anonmoty/VirusHawk)
[![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)](https://github.com/anonmoty/VirusHawk)

</div>

---

```
████████████████████████████████████████████████████████████████████████
█                                                                      █
█   ██╗   ██╗██╗██████╗ ██╗   ██╗███████╗██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗
█   ██║   ██║██║██╔══██╗██║   ██║██╔════╝██║  ██║██╔══██╗██║    ██║██║ ██╔╝
█   ██║   ██║██║██████╔╝██║   ██║███████╗███████║███████║██║ █╗ ██║█████╔╝ 
█   ██║   ██║██║██╔══██╗██║   ██║╚════██║██╔══██║██╔══██║██║███╗██║██╔═██╗ 
█   ╚██████╔╝██║██║  ██║╚██████╔╝███████║██║  ██║██║  ██║╚███╔███╔╝██║  ██╗
█    ╚═════╝ ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝
█                                                                      █
█                        [ Analyze | Detect | Defend ]                 █
█                                                                      █
████████████████████████████████████████████████████████████████████████
```

---

## ⚠️ Disclaimer

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   VIRUSHAWK is built for EDUCATIONAL and RESEARCH purposes only.     ║
║                                                                      ║
║   ▸ Analyze ONLY files you own or have permission to inspect.        ║
║   ▸ Unauthorized malware analysis is ILLEGAL.                        ║
║   ▸ Follow ethical guidelines and local laws at all times.           ║
║   ▸ The author is NOT responsible for any misuse.                    ║
║                                                                      ║
║   Analyze responsibly. Learn ethically. Defend proactively.          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 🎯 What Is VirusHawk?

**VirusHawk** is a Python-based malware analysis and threat detection framework. It helps security researchers inspect suspicious files, extract indicators of compromise (IOCs), and identify potential threats — all inside a controlled, ethical environment.

Built for:
- 🔬 Malware analysts
- 🛡️ Incident responders
- 🎓 Security students
- 🧪 Threat hunters

---

## ✨ Features

```
┌─────────────────────────────────────────────────────────────────────┐
│  [01] 🔍 File Analysis        → Inspects suspicious files            │
│  [02] 🧬 Hash Extraction       → MD5, SHA1, SHA256                   │
│  [03] 🧪 String Extraction     → Pulls readable strings              │
│  [04] 🛡️ VirusTotal Lookup     → Checks hashes against VT            │
│  [05] 📡 Network Indicators    → Extracts URLs, IPs, domains         │
│  [06] 🧰 PE Analysis           → Examines PE headers and sections    │
│  [07] ⚡ Multi-Threaded        → Fast parallel analysis              │
│  [08] 📊 Progress Bar          → Real-time feedback                  │
│  [09] 📝 JSON Reports          → Machine-readable output             │
│  [10] 🎨 Terminal UI           → Clean hacker-style display          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

```bash
# Clone
git clone https://github.com/anonmoty/VirusHawk.git
cd VirusHawk

# Install dependencies
pip install -r requirements.txt

# Run
python virushawk.py --help
```

**One-liner:**

```bash
git clone https://github.com/anonmoty/VirusHawk.git && cd VirusHawk && pip install -r requirements.txt && python virushawk.py --help
```

---

## 🎯 Usage

```bash
# Analyze a file
python virushawk.py --file suspicious.exe

# Hash only
python virushawk.py --file sample.bin --hash

# Extract strings
python virushawk.py --file sample.bin --strings

# Full analysis
python virushawk.py --file suspicious.exe --full --output reports/analysis.json

# VirusTotal lookup
python virushawk.py --file sample.bin --vt
```

### CLI Flags

```
┌─────────────────────────────────────────────────────────────────────┐
│  --file      →  Path to suspicious file                             │
│  --hash      →  Extract file hashes only                            │
│  --strings   →  Extract readable strings                            │
│  --full      →  Run full analysis                                   │
│  --vt        →  Lookup on VirusTotal                                │
│  --output    →  Report output path                                  │
│  --verbose   →  Verbose logging                                     │
│  --help      →  Show help                                           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 How It Works

```mermaid
graph LR
    A[Load File] --> B[Hash]
    B --> C[Strings]
    C --> D[PE Analysis]
    D --> E{Threat?}
    E -->|Yes| F[Log IOC]
    E -->|No| G[Mark Clean]
    F --> H[Report]
    G --> H
    H --> I[Done]

    style A fill:#1a0000,stroke:#FF0000,color:#00FF00
    style F fill:#1a0000,stroke:#FF0000,color:#00FF00
    style I fill:#1a0000,stroke:#FF0000,color:#00FF00
```

1. **Load** — Reads the file
2. **Hash** — Generates MD5, SHA1, SHA256
3. **Strings** — Extracts readable text
4. **Analyze** — Examines PE headers
5. **Detect** — Flags suspicious indicators
6. **Report** — Outputs structured findings

---

## 📁 Structure

```
VirusHawk/
├── virushawk.py
├── core/
│   ├── analyzer.py
│   ├── hasher.py
│   ├── strings.py
│   └── reporter.py
├── payloads/
├── reports/
├── tests/
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 📸 Demo

```
██████████████████████████████████████████████████████████████████████
█                                                                    █
█   VIRUSHAWK v1.0.0                                                 █
█   ───────────────────────────────────────────────────────────      █
█                                                                    █
█   [✓] File: suspicious.exe                                         █
█   [✓] Size: 245 KB                                                 █
█   [✓] Type: PE32 Executable                                        █
█   [→] Analyzing...                                                 █
█                                                                    █
█   [████████████████████████░░░░░░] 80%                             █
█                                                                    █
█   [✓] MD5:    d41d8cd98f00b204e9800998ecf8427e                     █
█   [✓] SHA256: e3b0c44298fc1c149afbf4c8996fb924...                  █
█   [!] Suspicious: Embedded URL found                               █
█   [!] Suspicious: Base64 payload detected                          █
█   [✓] Analysis complete in 3.21s                                   █
█   [✓] Report: reports/analysis_2024.json                           █
█                                                                    █
█                        Stay Vigilant! 🛡️                           █
█                                                                    █
██████████████████████████████████████████████████████████████████████
```

---

## 🛠️ Requirements

```txt
requests>=2.28.0
colorama>=0.4.6
tqdm>=4.65.0
rich>=13.0.0
pefile>=2023.2.7
```

```bash
pip install -r requirements.txt
```

---

## 🎨 Terminal Theme

VirusHawk uses a **red + green** hacker palette:

```python
THEME = {
    "primary":   "\033[38;5;196m",  # Bright Red
    "secondary": "\033[38;5;46m",   # Matrix Green
    "accent":    "\033[38;5;214m",  # Amber
    "error":     "\033[38;5;196m",  # Red
    "warning":   "\033[38;5;220m",  # Yellow
    "info":      "\033[38;5;46m",   # Green
    "reset":     "\033[0m",
}
```

---

## 🔥 Power Tips

```bash
# VirusHawk + YARA
python virushawk.py --file sample.bin --full
yara -r rules/ sample.bin

# VirusHawk + VT API
python virushawk.py --file sample.bin --vt --output vt.json
```

---

## 🐛 Research Workflow

```
██████████████████████████████████████████████████████████████████████
█                                                                    █
█   [01] Sample Collection     →  MalwareBazaar / VT                 █
█   [02] Static Analysis       →  VirusHawk  ← you are here          █
█   [03] Dynamic Analysis      →  Cuckoo / Any.Run                   █
█   [04] Rule Creation         →  YARA                               █
█   [05] Threat Intel Sharing  →  MISP                               █
█                                                                    █
██████████████████████████████████████████████████████████████████████
```

### Use Cases

- 🔍 Static analysis of suspicious files
- 📜 IOC extraction for threat intel
- 🗺️ PE structure mapping
- 🧪 AV evasion testing in labs
- 📊 Structured reports

---

## 🗺️ Roadmap

```
┌─────────────────────────────────────────────────────────────────────┐
│  [x] Hash extraction                                                │
│  [x] String extraction                                              │
│  [x] PE header analysis                                             │
│  [x] JSON reports                                                   │
│  [x] Terminal UI                                                    │
│  [ ] YARA integration                                               │
│  [ ] VirusTotal API                                                 │
│  [ ] Sandbox integration                                            │
│  [ ] Docker image                                                   │
│  [ ] Web dashboard                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🤝 Contributing

1. Fork the repo
2. Create branch (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📜 License

MIT License. See [`LICENSE`](LICENSE).

---

## 🙏 Credits

- **Author:** [@anonmoty](https://github.com/anonmoty)
- **Inspired by:** The malware research community
- **Built with:** Python, caffeine, and curiosity ☕

---

<div align="center">

```
██████████████████████████████████████████████████████████████████████
█                                                                    █
█          🦅  STAY VIGILANT.  ANALYZE ETHICALLY.  DEFEND.  🦅        █
█                                                                    █
█                  ⭐  If this tool helped you, star it!  ⭐           █
█                                                                    █
██████████████████████████████████████████████████████████████████████
```

</div>
