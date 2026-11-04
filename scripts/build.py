#!/usr/bin/env python3
"""Generates every SVG used by the profile README. Standard library only.

    python scripts/build.py          static assets and live.svg
    python scripts/build.py --live   live.svg only (used by the daily workflow)

live.svg keeps its previous version if an API call fails.
"""
import json, math, os, random, sys, urllib.request
from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
USER, CF = "Ajayendra2705", "Ajay_2705"
BG, PANEL, LINE, TEXT, MUTED = "#0a0e14", "#10161f", "#222c39", "#e8edf3", "#8b98a9"
GREEN, RED, AMBER, BLUE, VIOLET = "#2fd08a", "#f0616d", "#f2b84b", "#5aa9ff", "#b48cff"
SANS = "'Segoe UI',Inter,-apple-system,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono','Cascadia Code',Consolas,Menlo,monospace"
REDUCE = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def svg(w, h, body, css="", label=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(label)}"><style>{css}{REDUCE}</style>{body}</svg>\n')


def write(name, content):
    (ASSETS / name).write_text(content, encoding="utf-8")


def wrap(text, n):
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 > n and cur:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur]


def hero():
    W, H = 1200, 210
    body = (f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
            f'<text x="48" y="104" font-family="{SANS}" font-size="60" font-weight="700" fill="{TEXT}">Ajayendra Bansod</text>'
            f'<text x="50" y="152" font-family="{MONO}" font-size="19" fill="{MUTED}">Trading systems, quant research and algorithms. IIT Kharagpur, Class of 2027.</text>')
    write("hero.svg", svg(W, H, body, "", "Ajayendra Bansod: trading systems, quant research and algorithms. IIT Kharagpur, Class of 2027."))


def title(name, text):
    w = 1200
    body = (f'<rect x="0" y="18" width="4" height="22" fill="{GREEN}"/>'
            f'<text x="16" y="36" font-family="{MONO}" font-size="20" font-weight="600" fill="{MUTED}">'
            f'<tspan fill="{GREEN}">$</tspan> {escape(text)}</text>'
            f'<path d="M{24 + len(text) * 13 + 30} 29H{w}" stroke="{MUTED}" opacity=".3"/>')
    write(f"title-{name}.svg", svg(w, 56, body, "", text))


def scoreboard():
    tiles = [("#6", "AMS Derive", "national rank, of 2,500+", GREEN),
             ("#24", "IMC Prosperity 4", "global, manual trading, of ~19k teams", AMBER),
             ("1955", "Codeforces", "Candidate Master / CodeChef 4 Star", BLUE),
             ("#21", "IICPC QuantFest", "coding round / Regionals rank 243", GREEN),
             ("Top 40", "QuantStorm", "national finalist, market making", AMBER),
             ("18.7/20", "Akuna trading challenge", "market-making autograder", AMBER),
             ("#356", "IICPC Codefest", "Prelims, top 2.5% of 13,800+", BLUE),
             ("#21", "Cambridge Battlecode", "international ladder, 517 teams, Nov 2026", VIOLET),
             ("Top 400", "Integral Cup", "of 3,100+, backed by Optiver", GREEN)]
    tw, th, gap, body = 389, 132, 16, ""
    for i, (val, lab, sub, col) in enumerate(tiles):
        x, y = (i % 3) * (tw + gap), (i // 3) * (th + gap)
        body += (f'<g class="f" style="animation-delay:{i * .08:.2f}s"><rect x="{x + .5}" y="{y + .5}" width="{tw - 1}" height="{th - 1}" rx="10" fill="{PANEL}" stroke="{LINE}"/>'
                 f'<rect x="{x}" y="{y + 22}" width="3" height="46" fill="{col}"/>'
                 f'<text x="{x + 22}" y="{y + 60}" font-family="{SANS}" font-size="42" font-weight="700" fill="{TEXT}">{val}</text>'
                 f'<text x="{x + 22}" y="{y + 92}" font-family="{SANS}" font-size="16" font-weight="600" fill="{TEXT}">{lab}</text>'
                 f'<text x="{x + 22}" y="{y + 114}" font-family="{MONO}" font-size="13" fill="{MUTED}">{sub}</text></g>')
    css = "@keyframes f{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}.f{animation:f .5s ease-out both}"
    write("scoreboard.svg", svg(1199, 3 * th + 2 * gap, body, css, "Competition results"))


def motif(kind, col):
    """Decorative plot, drawn in a 540 x 96 box."""
    r = random.Random(kind)
    if kind == "bars":
        out = ""
        for i, v in enumerate([84, 72, 66, 52, 44, 36, 30, 22]):
            out += (f'<rect x="{i * 68}" y="{96 - v}" width="52" height="{v}" rx="3" fill="{col}" opacity="{1 - i * .09:.2f}" '
                    f'class="g" style="animation-delay:{i * .1:.1f}s"/>')
        return out
    if kind == "smile":
        out = ""
        for k, op in ((60, .3), (40, .55), (22, 1)):
            pts = " ".join(f"{x * 6},{84 - k * .4 - 62 * ((x - 45) / 45) ** 2:.1f}" for x in range(0, 91, 3))
            out += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.5" opacity="{op}"/>'
        return out
    if kind == "series":
        noisy, smooth, dots = [], [], ""
        for x in range(0, 91):
            base = 50 + 22 * math.sin(x / 11)
            n = base + r.uniform(-9, 9)
            if x in (19, 52, 74):
                n = max(6, min(90, base + (42 if x == 52 else -44)))
                dots += f'<circle cx="{x * 6}" cy="{n:.1f}" r="4.5" fill="{RED}"/>'
            noisy.append(f"{x * 6},{n:.1f}")
            smooth.append(f"{x * 6},{base:.1f}")
        return (f'<polyline points="{" ".join(noisy)}" fill="none" stroke="{MUTED}" opacity=".55"/>'
                f'<polyline points="{" ".join(smooth)}" fill="none" stroke="{col}" stroke-width="3"/>{dots}')
    if kind == "seq":
        out = ""
        for i in range(7):
            out += f'<rect x="{i * 28}" y="34" width="22" height="28" rx="4" fill="#2a3543"/>'
        for i in range(4):
            out += f'<rect x="{370 + i * 42}" y="34" width="34" height="28" rx="4" fill="{col}"/>'
        return out + (f'<path d="M200 48H356" stroke="{col}" stroke-width="2" stroke-dasharray="6 6" class="d"/>'
                      f'<path d="M350 41l9 7-9 7" fill="none" stroke="{col}" stroke-width="2"/>')
    if kind == "graph":
        nodes = [(30, 48), (150, 18), (150, 78), (290, 48), (420, 18), (510, 70)]
        edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5)]
        out = "".join(f'<path d="M{nodes[a][0]} {nodes[a][1]}L{nodes[b][0]} {nodes[b][1]}" stroke="{col}" stroke-width="2" opacity=".6" class="d" stroke-dasharray="6 6"/>' for a, b in edges)
        return out + "".join(f'<circle cx="{x}" cy="{y}" r="11" fill="{PANEL}" stroke="{col}" stroke-width="2.5"/>' for x, y in nodes)
    if kind == "exec":
        pts = []
        for i in range(0, 91, 3):
            y = 90 - 84 * math.sinh(2.2 * (1 - i / 90)) / math.sinh(2.2)
            pts.append(f"{i * 6},{y:.1f}")
        bars = ""
        for i in range(0, 90, 9):
            a = 90 - 84 * math.sinh(2.2 * (1 - i / 90)) / math.sinh(2.2)
            b = 90 - 84 * math.sinh(2.2 * (1 - (i + 9) / 90)) / math.sinh(2.2)
            h = max((b - a) * 1.6, 2)
            bars += f'<rect x="{i * 6 + 8}" y="{96 - h:.1f}" width="34" height="{h:.1f}" rx="2" fill="{col}" opacity=".28"/>'
        return bars + f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="3"/>'
    if kind == "pairs":
        a, b = [], []
        for x in range(0, 91):
            t = 30 + 18 * math.sin(x / 13) + r.uniform(-2, 2)
            a.append(f"{x * 6},{t:.1f}")
            b.append(f"{x * 6},{t + 26 + 11 * math.sin(x / 5) + r.uniform(-2, 2):.1f}")
        return (f'<polyline points="{" ".join(a)}" fill="none" stroke="{col}" stroke-width="2.5"/>'
                f'<polyline points="{" ".join(b)}" fill="none" stroke="{MUTED}" stroke-width="2"/>')
    if kind == "board":
        out = ""
        for row in range(4):
            for c in range(22):
                v = r.random()
                fill = "#1a2330" if v < .74 else "#2a3543" if v < .88 else col if v < .95 else RED
                cls = ' class="u"' if fill in (col, RED) else ""
                out += f'<rect{cls} x="{c * 24.5}" y="{row * 24.5}" width="21" height="21" rx="3" fill="{fill}"/>'
        return out
    if kind == "cube":
        faces = [RED, GREEN, BLUE, AMBER, TEXT, "#2a3543"]
        out = ""
        for f in range(4):
            for i in range(9):
                out += f'<rect x="{f * 138 + (i % 3) * 32}" y="{(i // 3) * 32}" width="28" height="28" rx="4" fill="{r.choice(faces)}"/>'
        return out
    if kind == "steps":
        vals = [20, 26, 22, 34, 38, 34, 48, 54, 50, 62, 72, 68, 80, 88]
        pts = " ".join(f"{i * 41.5:.1f},{96 - v}" for i, v in enumerate(vals))
        dots = "".join(f'<circle cx="{i * 41.5:.1f}" cy="{96 - v}" r="4" fill="{col}"/>' for i, v in enumerate(vals))
        return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.5"/>{dots}'
    if kind == "sort":
        vals = [40, 88, 24, 66, 52, 16, 76, 34, 94, 46, 60, 28, 82, 20, 70]
        out = ""
        for i, v in enumerate(vals):
            fill = AMBER if i in (4, 5) else col
            out += f'<rect x="{i * 36.5:.1f}" y="{96 - v}" width="28" height="{v}" rx="3" fill="{fill}" class="g" style="animation-delay:{i * .05:.2f}s"/>'
        return out
    if kind == "agents":
        cx, cy = 270, 48
        nodes = [(cx + 230 * math.cos(a), cy + 40 * math.sin(a)) for a in [i * math.tau / 7 for i in range(7)]]
        out = "".join(f'<path d="M{cx} {cy}L{x:.1f} {y:.1f}" stroke="{col}" stroke-width="2" stroke-dasharray="6 6" opacity=".6" class="d"/>' for x, y in nodes)
        out += "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{PANEL}" stroke="{col}" stroke-width="2.5"/>' for x, y in nodes)
        return out + f'<circle cx="{cx}" cy="{cy}" r="14" fill="{col}"/>'
    if kind == "draw":
        pts = " ".join(f"{x * 3},{48 + 28 * math.sin(x / 9) * math.cos(x / 23):.1f}" for x in range(0, 75))
        return (f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round"/>'
                f'<rect x="262" y="16" width="96" height="64" rx="4" fill="none" stroke="{AMBER}" stroke-width="2.5"/>'
                f'<circle cx="425" cy="48" r="33" fill="none" stroke="{BLUE}" stroke-width="2.5"/>'
                f'<path d="M478 76L530 22M530 22h-20M530 22v20" fill="none" stroke="{RED}" stroke-width="2.5"/>')
    return ""


def cards():
    data = [("iicpc", "iicpc-platform", "Hosts trading engines in gVisor sandboxes, drives them with a 5,000-bot fleet at 13K requests/s, and ranks them live on latency and correctness.", ["Go", "Kubernetes", "gVisor"], "bars", GREEN),
            ("options", "Options-Pricing-Volatility-Research", "Arbitrage-free implied-volatility surface and delta-hedged backtest on real option quotes, testing the variance risk premium after costs.", ["Python", "SVI", "Greeks"], "smile", AMBER),
            ("exec", "Almgren-Chriss", "Optimal execution that splits large orders over time to balance market impact against price risk, in one and two assets.", ["Python", "Execution", "Market impact"], "exec", RED),
            ("pairs", "Pairs-Trading", "Statistical arbitrage research: finds cointegrated pairs and trades the spread between them.", ["Python", "Cointegration", "Stat arb"], "pairs", BLUE),
            ("battlecode", "Cambridge Battlecode bot", "C++ team bot for a strategy game AI competition. International ladder rank 21 of 517, with 2,300+ ranked matches.", ["C++", "Game AI", "Team of 3"], "board", VIOLET),
            ("rubik", "Rubik-s-Cube-Solver", "C++ cube simulator with 1D array, 3D array and bitboard models, solved with search and pattern databases.", ["C++", "Search", "Bitboards"], "cube", AMBER),
            ("cf", "Codeforces-Analyzer", "Timed Codeforces practice that estimates a rating from problem difficulty, solve time, attempts and hints.", ["React", "Chart.js", "Live demo"], "steps", GREEN),
            ("viz", "Algorithm-Visualizer", "Interactive web app that shows fundamental algorithms one operation at a time.", ["React", "Algorithms", "Live demo"], "sort", BLUE),
            ("mssa", "robust-mssa", "Robust multivariate singular spectrum analysis that extracts latent factors from financial time series containing sparse outliers.", ["Python", "Time series", "Research"], "series", BLUE),
            ("agents", "private-multi-agent-llm", "Optimizes privacy-utility trade-offs in distributed large language model agent networks using metaheuristic search.", ["Python", "LLM agents", "Research"], "agents", VIOLET),
            ("split", "spliteasy", "Splitwise-style expense sharing with groups, flexible splits, expense chat and settle-up.", ["Next.js", "Postgres", "Live demo"], "graph", GREEN),
            ("board", "Whiteboard", "Drawing app with accounts, saved canvases and real-time sync over Socket.IO.", ["React", "Socket.IO", "Live demo"], "draw", AMBER)]
    for key, name, desc, tags, kind, col in data:
        W, H = 590, 290
        txt = "".join(f'<text x="24" y="{190 + i * 22}" font-family="{SANS}" font-size="16" fill="{MUTED}">{escape(l)}</text>' for i, l in enumerate(wrap(desc, 68)))
        x, chips = 24, ""
        for t in tags:
            w = len(t) * 7.6 + 20
            chips += (f'<rect x="{x}" y="250" width="{w:.0f}" height="24" rx="12" fill="none" stroke="{col}" opacity=".6"/>'
                      f'<text x="{x + w / 2:.0f}" y="266" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{col}">{escape(t)}</text>')
            x += w + 8
        body = (f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
                f'<g transform="translate(25 24)">{motif(kind, col)}</g>'
                f'<text x="24" y="161" font-family="{SANS}" font-size="23" font-weight="700" fill="{TEXT}">{escape(name)}</text>{txt}{chips}')
        css = ("@keyframes g{from{opacity:0;transform:translateY(12px)}}.g{animation:g .6s ease-out both}"
               "@keyframes d{to{stroke-dashoffset:-24}}.d{animation:d 1.4s linear infinite}"
               "@keyframes u{50%{opacity:.35}}.u{animation:u 2.2s ease-in-out infinite}")
        write(f"card-{key}.svg", svg(W, H, body, css, name))


def buttons():
    for key, label, col in (("linkedin", "LinkedIn", BLUE), ("codeforces", "Codeforces", GREEN), ("codechef", "CodeChef", AMBER)):
        body = (f'<rect x=".5" y=".5" width="169" height="43" rx="8" fill="{PANEL}" stroke="{LINE}"/>'
                f'<circle cx="24" cy="22" r="4.5" fill="{col}"/>'
                f'<text x="38" y="28" font-family="{MONO}" font-size="15" font-weight="600" fill="{TEXT}">{label}</text>')
        write(f"btn-{key}.svg", svg(170, 44, body, "", label))


def fetch(url, token=None):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-readme"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def live():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    skip = ("HTML", "CSS", "Jupyter Notebook", "Batchfile", "Makefile", "CMake", "Dockerfile", "Shell", "PowerShell")
    try:
        hist = fetch(f"https://codeforces.com/api/user.rating?handle={CF}")["result"]
        info = fetch(f"https://codeforces.com/api/user.info?handles={CF}")["result"][0]
        repos = fetch(f"https://api.github.com/users/{USER}/repos?per_page=100&type=public", token)
        totals = {}
        for repo in repos:
            if repo["fork"] or repo["private"]:
                continue
            for lang, n in fetch(repo["languages_url"], token).items():
                if lang not in skip:
                    totals[lang] = totals.get(lang, 0) + n
    except Exception as exc:
        print(f"live.svg kept: {exc}")
        return
    W, H = 1200, 300
    px, py, pw, ph = 34, 92, 690, 170
    vals = [h["newRating"] for h in hist]
    lo, hi = min(vals) - 40, max(vals) + 40
    pts = [(px + pw * i / max(len(vals) - 1, 1), py + ph * (1 - (v - lo) / (hi - lo))) for i, v in enumerate(vals)]
    line = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    area = f"{px},{py + ph} {line} {pts[-1][0]:.1f},{py + ph}"
    length = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    gl = ""
    for v in range(math.ceil(lo / 200) * 200, int(hi) + 1, 200):
        y = py + ph * (1 - (v - lo) / (hi - lo))
        gl += (f'<path d="M{px} {y:.1f}H{px + pw}" stroke="{LINE}"/>'
               f'<text x="{px + pw + 8}" y="{y + 4:.1f}" font-family="{MONO}" font-size="11" fill="{MUTED}">{v}</text>')
    mx = max(range(len(vals)), key=vals.__getitem__)
    ex, ey = pts[-1]
    body = (f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
            f'<text x="{px}" y="42" font-family="{SANS}" font-size="18" font-weight="700" fill="{TEXT}">Codeforces rating</text>'
            f'<text x="{px}" y="66" font-family="{MONO}" font-size="13" fill="{MUTED}">{CF} / {info["rank"]} / max {info["maxRating"]} / {len(vals)} contests / updated daily</text>'
            f'{gl}<polygon points="{area}" fill="{GREEN}" opacity=".08"/>'
            f'<polyline class="l" points="{line}" fill="none" stroke="{GREEN}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<circle cx="{pts[mx][0]:.1f}" cy="{pts[mx][1]:.1f}" r="4" fill="{AMBER}"/>'
            f'<circle class="u" cx="{ex:.1f}" cy="{ey:.1f}" r="5" fill="{GREEN}"/>'
            f'<path d="M790 28V272" stroke="{LINE}"/>'
            f'<text x="820" y="42" font-family="{SANS}" font-size="18" font-weight="700" fill="{TEXT}">Languages</text>'
            f'<text x="820" y="66" font-family="{MONO}" font-size="13" fill="{MUTED}">public repositories, by code size</text>')
    colors = {"Python": BLUE, "JavaScript": AMBER, "TypeScript": VIOLET, "Go": "#47c9d8", "C++": RED, "C": "#7f8ea3", "C#": GREEN}
    top = sorted(totals.items(), key=lambda kv: -kv[1])[:6]
    total = sum(totals.values()) or 1
    for i, (lang, n) in enumerate(top):
        y, share = 92 + i * 30, n / total
        body += (f'<text x="820" y="{y + 12}" font-family="{MONO}" font-size="13" fill="{TEXT}">{escape(lang)}</text>'
                 f'<rect x="930" y="{y + 2}" width="190" height="10" rx="5" fill="#1a2330"/>'
                 f'<rect class="b" x="930" y="{y + 2}" width="{max(190 * share, 4):.1f}" height="10" rx="5" fill="{colors.get(lang, MUTED)}"/>'
                 f'<text x="1132" y="{y + 12}" font-family="{MONO}" font-size="12" fill="{MUTED}">{share * 100:.0f}%</text>')
    css = (f"@keyframes l{{from{{stroke-dashoffset:{length:.0f}}}to{{stroke-dashoffset:0}}}}.l{{stroke-dasharray:{length:.0f};animation:l 2.4s ease-out both}}"
           "@keyframes u{50%{opacity:.3}}.u{animation:u 1.6s ease-in-out infinite}"
           "@keyframes b{from{transform:scaleX(0)}}.b{transform-box:fill-box;transform-origin:left;animation:b 1.2s ease-out both}")
    write("live.svg", svg(W, H, body, css, f"Codeforces rating history, max {info['maxRating']}, and language breakdown"))
    print("live.svg updated")


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    if "--live" not in sys.argv:
        hero()
        scoreboard()
        cards()
        buttons()
        for name, text in (("results", "cat results.log"), ("trading", "ls ~/trading"), ("algo", "ls ~/algorithms-and-bots"), ("research", "ls ~/research"), ("apps", "ls ~/apps"), ("live", "watch stats"),
                           ("stack", "which tools"), ("activity", "git log --graph")):
            title(name, text)
    live()
