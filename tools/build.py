#!/usr/bin/env python3
"""Generates the animated SVGs of the profile README, one file per theme.

GitHub renders README images through <img>, so the SVGs can't load fonts or run
scripts: only inline CSS and SMIL animations, with system font stacks.
Run: python3 tools/build.py
"""
from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": dict(
        panel="#0d1117", raised="#161b22", border="#30363d", text="#e6edf3",
        muted="#8b949e", accent="#a78bfa", accent2="#5eead4", ok="#7ee787",
        crash="#f85149",
    ),
    "light": dict(
        panel="#ffffff", raised="#f6f8fa", border="#d0d7de", text="#1f2328",
        muted="#59636e", accent="#7c3aed", accent2="#0d9488", ok="#1a7f37",
        crash="#cf222e",
    ),
}

BASE_CSS = """
.sans{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif}
.mono{font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace}
.f{opacity:0;animation:fade .45s ease-out forwards}
.r{opacity:0;animation:rise .7s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes fade{to{opacity:1}}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
"""

# Without this the page still shows the final frame for people who asked for less motion.
REDUCED_CSS = """
@media (prefers-reduced-motion:reduce){
  *{animation:none!important}
  .f,.r{opacity:1}
}
"""


def svg(w, h, css, body, title):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<style>{BASE_CSS}{css}{REDUCED_CSS}</style>
{body}
</svg>
"""


def delay(s):
    return f'style="animation-delay:{s:.2f}s"'


# --- Header: an OTP supervision tree -------------------------------------------

def supervisor(t):
    w, h = 840, 300
    root = (640, 64, "Nicolo.Supervisor")
    kids = [(484, 154, "Phoenix"), (588, 154, "Ash"), (686, 154, "Astro"), (792, 154, "Design")]
    grand = [(484, 240, "LiveView"), (588, 240, "Oban"), (686, 240, "Tailwind"), (792, 240, "Blender")]
    crashing = "Oban"  # let it crash: the supervisor restarts it

    def node(x, y, label, cls="", wide=False):
        pw = len(label) * 7.6 + 32 if not wide else len(label) * 7.8 + 40
        return f"""<g class="node {cls}">
  <rect x="{x - pw / 2:.1f}" y="{y - 14}" width="{pw:.1f}" height="28" rx="14" fill="{t['raised']}" stroke="{t['border']}"/>
  <circle class="led" cx="{x - pw / 2 + 13:.1f}" cy="{y}" r="3.5" fill="{t['ok']}"/>
  <text class="mono" x="{x + 9:.1f}" y="{y + 4.5}" font-size="12.5" fill="{t['text']}" text-anchor="middle">{escape(label)}</text>
</g>"""

    edges, msgs = [], []
    rx, ry, _ = root
    for i, (x, y, _) in enumerate(kids):
        d = f"M{rx},{ry + 14} C{rx},{ry + 50} {x},{y - 50} {x},{y - 14}"
        edges.append(d)
        msgs.append((f"e{i}", d, 0.4 * i, i % 2 == 1))
    for i, ((x, y, _), (gx, gy, _)) in enumerate(zip(kids, grand)):
        d = f"M{x},{y + 14} L{gx},{gy - 14}"
        edges.append(d)
        msgs.append((f"g{i}", d, 0.9 + 0.35 * i, i % 2 == 0))

    edge_svg = "\n".join(
        f'<path id="p{i}" d="{d}" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>' for i, d in enumerate(edges)
    )
    msg_svg = "\n".join(
        f"""<circle r="3" fill="{t['accent2'] if up else t['accent']}">
  <animateMotion dur="2.2s" begin="{begin:.2f}s" repeatCount="indefinite" keyPoints="{'1;0' if up else '0;1'}" keyTimes="0;1" calcMode="linear"><mpath href="#p{i}"/></animateMotion>
</circle>"""
        for i, (_, _, begin, up) in enumerate(msgs)
    )

    css = f"""
.pulse{{transform-box:fill-box;transform-origin:center;animation:ring 2.6s ease-out infinite}}
@keyframes ring{{from{{transform:scale(1);opacity:.6}}to{{transform:scale(1.35);opacity:0}}}}
.crash rect{{animation:crashbox 7s infinite}}
.crash .led{{animation:crashled 7s infinite}}
@keyframes crashbox{{0%,70%,86%,100%{{stroke:{t['border']};opacity:1}}72%,78%{{stroke:{t['crash']}}}80%,83%{{opacity:.25}}}}
@keyframes crashled{{0%,70%,86%,100%{{fill:{t['ok']}}}72%,83%{{fill:{t['crash']}}}}}
"""
    rpw = len(root[2]) * 7.8 + 40
    body = f"""<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{t['panel']}" stroke="{t['border']}"/>

<text class="mono r" {delay(0.1)} x="40" y="78" font-size="13" fill="{t['muted']}"><tspan fill="{t['accent']}">iex&gt;</tspan> Nicolo.whoami()</text>
<text class="sans r" {delay(0.25)} x="38" y="136" font-size="48" font-weight="700" letter-spacing="-1" fill="{t['text']}">Nicolò Boni</text>
<text class="sans r" {delay(0.4)} x="40" y="172" font-size="17" fill="{t['muted']}">Developer at Zoonect, Montecatini Terme</text>
<text class="sans r" {delay(0.55)} x="40" y="200" font-size="17" fill="{t['muted']}">Elixir apps, Astro sites, brand visuals.</text>
<text class="mono r" {delay(0.7)} x="40" y="248" font-size="12" fill="{t['muted']}">strategy: <tspan fill="{t['accent2']}">:one_for_one</tspan>  # let it crash</text>

<g class="f" {delay(0.3)}>
{edge_svg}
{msg_svg}
<rect class="pulse" x="{rx - rpw / 2:.1f}" y="{ry - 14}" width="{rpw:.1f}" height="28" rx="14" fill="none" stroke="{t['accent']}"/>
{node(rx, ry, root[2], wide=True)}
{"".join(node(x, y, l) for x, y, l in kids)}
{"".join(node(x, y, l, "crash" if l == crashing else "") for x, y, l in grand)}
</g>
"""
    return svg(w, h, css, body, "Nicolò Boni, developer at Zoonect")


# --- Stack card ----------------------------------------------------------------

STACK = [
    ("apps", [("Elixir", "#a074c4"), ("Phoenix", "#f26a2e"), ("LiveView", "#f26a2e"), ("Ash", "#e5484d"), ("Oban", "#4f86f7"), ("PostgreSQL", "#4169e1")]),
    ("web", [("Astro", "#ff5d01"), ("TypeScript", "#3178c6"), ("Tailwind", "#38bdf8")]),
    ("design", [("Figma", "#a259ff"), ("Blender", "#ea7600"), ("AI image & video", "#ec4899")]),
]


def stack(t):
    w, row_h = 840, 44
    h = 24 + row_h * len(STACK)
    rows, n = [], 0
    for r, (label, items) in enumerate(STACK):
        y = 34 + r * row_h
        rows.append(f'<text class="mono" x="24" y="{y + 5}" font-size="12" fill="{t["muted"]}">{label}</text>')
        x = 110
        for name, color in items:
            pw = len(name) * 6.9 + 38
            rows.append(f"""<g class="r" {delay(0.06 * n)}>
  <rect x="{x}" y="{y - 14}" width="{pw:.1f}" height="28" rx="14" fill="{t['raised']}" stroke="{t['border']}"/>
  <circle cx="{x + 15}" cy="{y}" r="4" fill="{color}"/>
  <text class="sans" x="{x + 26}" y="{y + 4.5}" font-size="13" fill="{t['text']}">{escape(name)}</text>
</g>""")
            x += pw + 10
            n += 1
    body = f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{t["panel"]}" stroke="{t["border"]}"/>\n' + "\n".join(rows)
    return svg(w, h, "", body, "Stack: Elixir, Phoenix, LiveView, Ash, Oban, PostgreSQL, Astro, TypeScript, Tailwind, Figma, Blender")


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for theme, t in THEMES.items():
        (ASSETS / f"header-{theme}.svg").write_text(supervisor(t), encoding="utf-8")
        (ASSETS / f"stack-{theme}.svg").write_text(stack(t), encoding="utf-8")
    print("\n".join(sorted(p.name for p in ASSETS.glob("*.svg"))))
