🍇 GitSquisher

**Clean • Secure • AI-First Project Zipper**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![Stars](https://img.shields.io/github/stars/johntrus/GitSquisher)](https://github.com/johntrus/GitSquisher/stargazers)

GitSquisher is a simple, safe desktop GUI tool that creates perfect `.gitignore`-respecting zipped snapshots of any project, then optionally encrypts them with production-grade AES-256 and automatic 90-day key rotation.

Perfect for securely sharing large codebases with AI coding assistants (Claude, Cursor, Grok, etc.) without ever leaking secrets, caches, models, or bloat.

## ✨ Key Features
- Interactive two-column **Project Structure** viewer with live Git status colors and one-click ignore toggles  
- Real-time preview counter: **📦 X clean files will be squished**  
- **Squish (Zip)** using `git archive` (preferred) or manual fallback  
- **🔐 Encrypt & Key** — automatic 90-day key rotation + full MultiFernet backward compatibility  
- **🔓 Decrypt Latest** — instantly restores the newest `.enc` file to a usable zip  
- Modern dark-themed responsive Tkinter GUI with graceful animated shutdown  
- Fully modular codebase designed for effortless AI-assisted expansion  

## 🚀 Quick Start
1. Clone or download the repository  
2. Run `python3 entry.py` (or `python3 gitsquisher_gui.py`)  
3. Click **Browse Folder** → select your project root → **Load Repo**  
4. Use the big buttons: **Squish (Zip)**, **Encrypt & Key**, or **Decrypt Latest**

## Why Developers Love GitSquisher
- Zero risk of including unwanted files or sensitive data  
- Built-in encryption with secure automatic key rotation  
- Intuitive GUI that makes complex workflows feel effortless  
- Perfect for sharing clean project archives with AI coding tools  

## Repo Description (copy-paste into GitHub “About”)
GitSquisher 🗜️🍇 — Clean .gitignore-respecting project zipping with AES-256 encryption, automatic key rotation, and an intuitive GUI. Perfect for securely sharing codebases with AI coding assistants.

## Security Note
Your `grem_encryption.key` is automatically ignored and never committed. The app handles secure rotation and deletion.

## License
MIT

Made with ❤️ for clean, secure, and AI-powered development workflows.
EOF
