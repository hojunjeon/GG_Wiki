---
source: geeknews
date: 2026-05-12
points: 19
url: "https://github.com/patrickhener/goshs"
title: goshs - 개발자를 위한 다기능 단일 바이너리 파일 서버
---

# goshs - 개발자를 위한 다기능 단일 바이너리 파일 서버

You're mid-engagement. You need to transfer a file, catch an SMB hash, or stand up a quick HTTPS server — and python3 -m http.server
won't cut it.
goshs is a single-binary file server built for the moments when you need more than Python's SimpleHTTPServer but don't want to configure Apache. HTTP/S, WebDAV, SFTP, SMB, LDAP/S, basic auth, share links, DNS/SMTP callbacks, NTLM hash capture + cracking — all from one command.
Try it out yourself: demo.goshs.de
# Serve the current directory on port 8000
goshs
# Serve with HTTPS (self-signed) and basic auth
goshs -s -ss -b user:password
# Capture SMB hashes
goshs -smb -smb-domain CORP
# Capture LDAP credentials and NTLM hashes (with optional wordlist cracking)
goshs -ldap
goshs -ldap -ldap-wordlist /usr/share/wordlists/rockyou.txt
# Catch DNS callbacks and receive emails
goshs -dns -dns-ip 1.2.3.4 -smtp -smtp-domain your-domain.com
For a detailed documentation go to docs.goshs.de
🐚 Shell completion
goshs can install tab completion for bash, fish, and zsh:
goshs --completion bash
goshs --completion fish
goshs --completion zsh
On macOS with Homebrew the correct Homebrew path is used automatically. After installation the command prints an exact activation instruction, e.g.:
source ~/.local/share/bash-completion/completions/goshs
🔧 Build yourself
Building requirements are esbuild and sass. After installing these packages run:
git clone https://github.com/patrickhener/goshs.git
cd goshs
make build-all
These are the awesome contributors that made goshs
even more secure ❤️
Join the Discord Community and start connecting.
A special thank you goes to sc0tfree for inspiring this project with his project updog written in Python.