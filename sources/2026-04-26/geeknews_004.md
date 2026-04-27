---
source: geeknews
date: 2026-04-26
points: 7
url: "https://github.com/nakagami/grdpwasm"
title: grdpwasm - 웹 기반 RDP 클라이언트
---

# grdpwasm - 웹 기반 RDP 클라이언트

A web-based RDP client built with Go WebAssembly and grdp. Connect to a Windows Remote Desktop server directly from your browser — no plugins required.
Browser (WASM) ──WebSocket──► proxy (Go) ──TCP──► RDP Server
Because browsers cannot open raw TCP sockets, a lightweight Go proxy server bridges WebSocket connections from the browser to the RDP server's TCP port.
- Go 1.24 or later
- A reachable RDP server (Windows or any RDP-compatible host)
git clone https://github.com/nakagami/grdpwasm.git
cd grdpwasm
make all
make all
produces:
make serve
# or equivalently:
./proxy/proxy -listen :8080 -static static
Then open http://localhost:8080 in your browser.
- Open
http://localhost:8080
in a browser. - Fill in the connection form:
- Host — hostname or IP address of the RDP server
- Port — RDP port (default
3389
) - Domain — Windows domain (leave blank for local accounts)
- User — username
- Password — password
- Width / Height — initial desktop resolution
- Click Connect.
- The remote desktop appears in the canvas. Click the canvas to capture keyboard focus.
- Click Disconnect to end the session.
All standard keyboard input is forwarded to the remote desktop via RDP scan codes. Mouse move, button clicks, and scroll wheel are fully supported.
Note: The browser tab must have focus for keyboard events to be forwarded. Click inside the canvas area if keys stop responding.
Remote audio is streamed via RDPSND and played through the browser's Web Audio API (PCM 44100 Hz, stereo, 16-bit signed little-endian).
- The proxy accepts connections from any origin. Run it only on a trusted network or add authentication before exposing it to the internet.
- Credentials are transmitted from the browser to the proxy over WebSocket. Use HTTPS/WSS (put the proxy behind a TLS-terminating reverse proxy such as nginx or Caddy) when accessing it over an untrusted network.
make wasm # rebuild only the WASM binary
make proxy # rebuild only the proxy server
make wasm_exec # refresh wasm_exec.js from the local Go toolchain
make clean # remove all build artifacts
GPLv3 — see grdp LICENSE.