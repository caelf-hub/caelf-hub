#!/usr/bin/env python3
"""Generate premium SMIL SVG header/footer pairs for caelf-hub profile."""

from pathlib import Path

OUT = Path(__file__).resolve().parent
FONT_UI = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
FONT_MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "dark": {
        "bg0": "#0a0b0d",
        "bg1": "#12141a",
        "grid": "#2a2e38",
        "grid_faint": "#1e222b",
        "ink": "#f5f5f7",
        "muted": "#8e8e93",
        "faint": "#636366",
        "accent": "#8b3a45",
        "accent_soft": "#5c2a32",
        "circuit": "#3d4452",
        "node": "#c9a0a6",
        "stream": "#6b7385",
        "mesh_a": "#1a1520",
        "mesh_b": "#0f1a22",
        "mesh_c": "#1a1214",
        "particle": "#d1d1d6",
        "cursor": "#c9a0a6",
        "vignette": "#0a0b0d",
    },
    "light": {
        "bg0": "#fbfbfd",
        "bg1": "#f5f5f7",
        "grid": "#d2d2d7",
        "grid_faint": "#e5e5ea",
        "ink": "#1d1d1f",
        "muted": "#6e6e73",
        "faint": "#8e8e93",
        "accent": "#500000",
        "accent_soft": "#7a3a3a",
        "circuit": "#c7c7cc",
        "node": "#500000",
        "stream": "#aeaeb2",
        "mesh_a": "#f0eef2",
        "mesh_b": "#e8eef4",
        "mesh_c": "#f2ecec",
        "particle": "#1d1d1f",
        "cursor": "#500000",
        "vignette": "#fbfbfd",
    },
}

def build_particles(count: int = 96):
    """Deterministic particle field (x, y, r, opacity, dur, dx, dy, delay)."""
    out = []
    for i in range(count):
        x = (37 * i * i + 91 * i + 17) % 1240 + 20
        y = (53 * i + 29 * (i % 7) + 11) % 340 + 10
        r = 0.6 + (i % 5) * 0.18
        op = 0.12 + (i % 6) * 0.04
        dur = 14 + (i % 12)
        dx = ((i * 13) % 70) - 35
        dy = ((i * 17) % 50) - 25
        delay = (i % 20) * 0.18
        out.append((x, y, r, op, dur, dx, dy, delay))
    return out


PARTICLES = build_particles(140)

# Circuit nodes: (cx, cy, r)
NODES = [
    (980, 80, 3.5),
    (1040, 110, 2.5),
    (1100, 85, 3.0),
    (1145, 140, 2.2),
    (1065, 175, 2.8),
    (1180, 200, 2.4),
    (1005, 230, 2.6),
    (1120, 250, 3.2),
    (960, 280, 2.0),
    (1085, 300, 2.5),
    (1025, 55, 2.0),
    (1165, 95, 2.3),
    (1210, 160, 2.1),
    (990, 190, 2.4),
    (1155, 220, 2.0),
    (1045, 270, 2.2),
    (1195, 280, 2.6),
    (945, 150, 1.8),
]

# Circuit path segments (polyline points strings)
TRACES = [
    "980,80 1040,80 1040,110",
    "1040,110 1100,110 1100,85",
    "1100,85 1145,85 1145,140",
    "1040,110 1065,110 1065,175",
    "1065,175 1120,175 1120,250",
    "1120,250 1180,250 1180,200",
    "1065,175 1005,175 1005,230",
    "1005,230 960,230 960,280",
    "1120,250 1085,250 1085,300",
    "980,80 980,140 1005,140 1005,175",
    "1025,55 1025,80 980,80",
    "1100,85 1165,85 1165,95",
    "1145,140 1210,140 1210,160",
    "1005,230 990,230 990,190",
    "1120,250 1155,250 1155,220",
    "1085,300 1045,300 1045,270",
    "1180,200 1195,200 1195,280",
    "945,150 980,150 980,80",
    "945,150 945,230 960,230",
    "1165,95 1165,140 1145,140",
]

# Neural net nodes across mid-right field (avoid overlapping hero text)
NEURAL = [
    (720, 60), (760, 100), (800, 55), (840, 95), (880, 70),
    (730, 150), (770, 185), (815, 155), (860, 190), (900, 160),
    (740, 240), (785, 270), (830, 245), (875, 280), (915, 250),
    (700, 110), (695, 200), (705, 290),
]


def neural_layer(t: dict) -> str:
    lines = ['  <!-- Neural network -->', f'  <g fill="none" stroke="{t["circuit"]}" stroke-width="0.9">']
    # Connect nearby nodes
    for i, (x1, y1) in enumerate(NEURAL):
        for j, (x2, y2) in enumerate(NEURAL):
            if j <= i:
                continue
            dist2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
            if dist2 < 85 ** 2:
                delay = ((i + j) % 9) * 0.4
                lines.append(f'''    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" opacity="0.2">
      <animate attributeName="opacity" values="0.08;0.35;0.08" dur="5s" begin="{delay}s" repeatCount="indefinite"/>
    </line>''')
    lines.append('  </g>')
    lines.append(f'  <g fill="{t["node"]}">')
    for i, (x, y) in enumerate(NEURAL):
        delay = (i % 8) * 0.35
        lines.append(f'''    <circle cx="{x}" cy="{y}" r="2.2" opacity="0.4">
      <animate attributeName="opacity" values="0.2;0.75;0.2" dur="3.2s" begin="{delay}s" repeatCount="indefinite"/>
    </circle>''')
    lines.append('  </g>')
    return '\n'.join(lines) + '\n'


def mesh_layer(t: dict) -> str:
    return f'''  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t['bg0']}">
        <animate attributeName="stop-color" values="{t['bg0']};{t['mesh_a']};{t['bg0']}" dur="18s" repeatCount="indefinite"/>
      </stop>
      <stop offset="45%" stop-color="{t['bg1']}">
        <animate attributeName="stop-color" values="{t['bg1']};{t['mesh_b']};{t['bg1']}" dur="18s" begin="2s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="{t['bg0']}">
        <animate attributeName="stop-color" values="{t['bg0']};{t['mesh_c']};{t['bg0']}" dur="18s" begin="4s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>
    <radialGradient id="mesh1" cx="22%" cy="30%" r="45%">
      <stop offset="0%" stop-color="{t['accent_soft']}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{t['bg0']}" stop-opacity="0"/>
      <animate attributeName="cx" values="22%;28%;18%;22%" dur="22s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="30%;24%;36%;30%" dur="22s" repeatCount="indefinite"/>
    </radialGradient>
    <radialGradient id="mesh2" cx="78%" cy="60%" r="40%">
      <stop offset="0%" stop-color="{t['mesh_b']}" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="{t['bg0']}" stop-opacity="0"/>
      <animate attributeName="cx" values="78%;72%;82%;78%" dur="26s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="60%;68%;54%;60%" dur="26s" repeatCount="indefinite"/>
    </radialGradient>
    <radialGradient id="mesh3" cx="55%" cy="15%" r="35%">
      <stop offset="0%" stop-color="{t['mesh_a']}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{t['bg0']}" stop-opacity="0"/>
      <animate attributeName="cx" values="55%;60%;50%;55%" dur="20s" repeatCount="indefinite"/>
    </radialGradient>
    <clipPath id="frame">
      <rect width="1280" height="360" rx="0"/>
    </clipPath>
  </defs>
  <rect width="1280" height="360" fill="url(#bgGrad)"/>
  <rect width="1280" height="360" fill="url(#mesh1)">
    <animate attributeName="opacity" values="0.7;1;0.7" dur="14s" repeatCount="indefinite"/>
  </rect>
  <rect width="1280" height="360" fill="url(#mesh2)">
    <animate attributeName="opacity" values="0.6;0.95;0.6" dur="16s" begin="1s" repeatCount="indefinite"/>
  </rect>
  <rect width="1280" height="360" fill="url(#mesh3)" opacity="0.8"/>
'''


def grid_layer(t: dict, height: int = 360) -> str:
    lines = ['  <!-- Engineering grid -->', f'  <g stroke="{t["grid_faint"]}" stroke-width="1" fill="none">']
    for x in range(0, 1281, 20):
        op = 0.5 if x % 80 == 0 else (0.32 if x % 40 == 0 else 0.14)
        lines.append(f'    <line x1="{x}" y1="0" x2="{x}" y2="{height}" opacity="{op}"/>')
    for y in range(0, height + 1, 20):
        op = 0.5 if y % 80 == 0 else (0.32 if y % 40 == 0 else 0.14)
        lines.append(f'    <line x1="0" y1="{y}" x2="1280" y2="{y}" opacity="{op}"/>')
    lines.append('  </g>')
    lines.append(f'''  <g stroke="{t['grid']}" stroke-width="1" fill="none" opacity="0">
    <line x1="0" y1="120" x2="1280" y2="120"/>
    <line x1="0" y1="240" x2="1280" y2="240"/>
    <animate attributeName="opacity" values="0.15;0.45;0.15" dur="8s" repeatCount="indefinite"/>
  </g>''')
    return '\n'.join(lines) + '\n'


def particles_layer(t: dict) -> str:
    lines = ['  <!-- Particles -->', f'  <g fill="{t["particle"]}">']
    for i, (x, y, r, op, dur, dx, dy, delay) in enumerate(PARTICLES):
        lines.append(f'''    <circle cx="{x}" cy="{y}" r="{r}" opacity="{op}">
      <animateTransform attributeName="transform" type="translate" values="0,0; {dx},{dy}; 0,0" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="{op};{min(op + 0.25, 0.7):.2f};{op}" dur="{dur * 0.7:.1f}s" begin="{delay}s" repeatCount="indefinite"/>
    </circle>''')
    lines.append('  </g>')
    return '\n'.join(lines) + '\n'


def streams_layer(t: dict) -> str:
    streams = [
        (80, 300, 420, 300, 7, 0),
        (200, 320, 560, 320, 9, 1.5),
        (900, 40, 1200, 40, 8, 0.8),
        (850, 60, 1180, 60, 11, 2.2),
        (640, 340, 980, 340, 10, 0.4),
        (40, 40, 280, 40, 12, 1.0),
        (50, 60, 260, 60, 8, 2.8),
        (1000, 330, 1260, 330, 9, 1.7),
    ]
    lines = ['  <!-- Data streams -->', f'  <g fill="none" stroke="{t["stream"]}" stroke-width="1.2" stroke-linecap="round">']
    for x1, y1, x2, y2, dur, delay in streams:
        length = abs(x2 - x1)
        lines.append(f'''    <path d="M{x1},{y1} H{x2}" stroke-dasharray="6 14" opacity="0.35">
      <animate attributeName="stroke-dashoffset" from="0" to="-{length}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.2;0.5;0.2" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>
    </path>''')
    lines.append('  </g>')
    return '\n'.join(lines) + '\n'


def circuit_layer(t: dict) -> str:
    lines = ['  <!-- Circuit traces & nodes -->']
    lines.append(f'  <g fill="none" stroke="{t["circuit"]}" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">')
    for i, pts in enumerate(TRACES):
        delay = i * 0.35
        lines.append(f'''    <polyline points="{pts}" opacity="0.55">
      <animate attributeName="opacity" values="0.25;0.7;0.25" dur="3.6s" begin="{delay}s" repeatCount="indefinite"/>
    </polyline>''')
    lines.append('  </g>')
    lines.append(f'  <g fill="{t["node"]}">')
    for i, (cx, cy, r) in enumerate(NODES):
        delay = i * 0.4
        dur = 2.4 + (i % 4) * 0.45
        lines.append(f'''    <circle cx="{cx}" cy="{cy}" r="{r}" opacity="0.55">
      <animate attributeName="opacity" values="0.3;0.95;0.3" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>
      <animate attributeName="r" values="{r};{r * 1.35:.2f};{r}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{cx}" cy="{cy}" r="{r * 2.8:.1f}" fill="{t["accent"]}" opacity="0.08">
      <animate attributeName="opacity" values="0.04;0.16;0.04" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>
    </circle>''')
    lines.append('  </g>')
    # Floating geometry
    lines.append(f'''  <g fill="none" stroke="{t["circuit"]}" stroke-width="1" opacity="0.4">
    <rect x="1080" y="40" width="36" height="36" rx="2">
      <animateTransform attributeName="transform" type="rotate" values="0 1098 58; 360 1098 58" dur="48s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.25;0.55;0.25" dur="10s" repeatCount="indefinite"/>
    </rect>
    <polygon points="1180,280 1200,310 1160,310">
      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-8; 0,0" dur="9s" repeatCount="indefinite"/>
    </polygon>
  </g>
''')
    return '\n'.join(lines) + '\n'


def hero_text(t: dict) -> str:
    # Typewriter via clip reveal + cursor
    return f'''  <!-- Hero typography -->
  <g font-family="{FONT_UI}">
    <text x="64" y="148" fill="{t['ink']}" font-size="52" font-weight="600" letter-spacing="-0.8" opacity="0">
      Cael Findley
      <animate attributeName="opacity" from="0" to="1" begin="0.3s" dur="0.8s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate" values="0,10; 0,0" begin="0.3s" dur="0.8s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.2 0.8 0.2 1"/>
    </text>
    <!-- Cursor after name -->
    <rect x="400" y="112" width="2.5" height="42" fill="{t['cursor']}" opacity="0" rx="0.5">
      <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.18;0.19;0.48;0.49;1" dur="1.1s" begin="1.0s" repeatCount="indefinite"/>
      <animate attributeName="x" values="64;400" dur="1.4s" begin="0.3s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"/>
    </rect>
    <text x="64" y="188" fill="{t['muted']}" font-size="18" font-weight="400" letter-spacing="0.2" opacity="0">
      Computer Science · Texas A&amp;M University
      <animate attributeName="opacity" from="0" to="1" begin="1.2s" dur="0.7s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate" values="0,8; 0,0" begin="1.2s" dur="0.7s" fill="freeze"/>
    </text>
  </g>
  <!-- Focus chips -->
  <g font-family="{FONT_UI}" font-size="13" font-weight="500" opacity="0">
    <g>
      <rect x="64" y="220" width="158" height="28" rx="6" fill="{t['accent']}" fill-opacity="0.12" stroke="{t['accent']}" stroke-opacity="0.35" stroke-width="1"/>
      <text x="143" y="238" text-anchor="middle" fill="{t['ink']}">Artificial Intelligence</text>
    </g>
    <g>
      <rect x="234" y="220" width="152" height="28" rx="6" fill="{t['accent']}" fill-opacity="0.08" stroke="{t['circuit']}" stroke-width="1"/>
      <text x="310" y="238" text-anchor="middle" fill="{t['muted']}">Software Engineering</text>
    </g>
    <g>
      <rect x="398" y="220" width="78" height="28" rx="6" fill="{t['accent']}" fill-opacity="0.08" stroke="{t['circuit']}" stroke-width="1"/>
      <text x="437" y="238" text-anchor="middle" fill="{t['muted']}">Systems</text>
    </g>
    <g>
      <rect x="488" y="220" width="138" height="28" rx="6" fill="{t['accent']}" fill-opacity="0.08" stroke="{t['circuit']}" stroke-width="1"/>
      <text x="557" y="238" text-anchor="middle" fill="{t['muted']}">Machine Learning</text>
    </g>
    <animate attributeName="opacity" from="0" to="1" begin="1.9s" dur="0.8s" fill="freeze"/>
  </g>
  <!-- Accent measure -->
  <g opacity="0">
    <rect x="64" y="272" width="200" height="1.5" fill="{t['circuit']}" rx="1"/>
    <rect x="64" y="272" width="0" height="1.5" fill="{t['accent']}" rx="1">
      <animate attributeName="width" from="0" to="200" begin="2.5s" dur="1.2s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"/>
    </rect>
    <text x="64" y="296" fill="{t['faint']}" font-family="{FONT_MONO}" font-size="11" letter-spacing="1.5">ENGINEERING · RESEARCH · BUILD</text>
    <animate attributeName="opacity" from="0" to="1" begin="2.5s" dur="0.4s" fill="freeze"/>
  </g>
  <!-- Coordinate ticks -->
  <g font-family="{FONT_MONO}" font-size="9" fill="{t['faint']}" opacity="0.45">
    <text x="64" y="28">0,0</text>
    <text x="1220" y="28" text-anchor="end">1280</text>
    <text x="64" y="348">CS · TAMU</text>
    <text x="1220" y="348" text-anchor="end">v1</text>
  </g>
'''


def vignette(t: dict, height: int = 360) -> str:
    return f'''  <rect width="1280" height="{height}" fill="none" stroke="{t['vignette']}" stroke-width="48" opacity="0.45"/>
'''


def header_svg(theme: str) -> str:
    t = THEMES[theme]
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 360" width="1280" height="360" role="img" aria-labelledby="title desc">
  <title id="title">Cael Findley — Computer Science, Texas A&amp;M</title>
  <desc id="desc">Animated profile banner ({theme} mode): engineering grid, circuit traces, and typewriter introduction</desc>
{mesh_layer(t)}{grid_layer(t)}{particles_layer(t)}{streams_layer(t)}{neural_layer(t)}{circuit_layer(t)}{hero_text(t)}{vignette(t)}</svg>
'''


def footer_svg(theme: str) -> str:
    t = THEMES[theme]
    particles = PARTICLES[:36]
    lines = [
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 120" width="1280" height="120" role="img" aria-labelledby="ftitle">
  <title id="ftitle">Cael Findley — footer</title>
  <defs>
    <linearGradient id="fbg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t['bg0']}"/>
      <stop offset="100%" stop-color="{t['bg1']}"/>
    </linearGradient>
    <radialGradient id="fmesh" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{t['accent_soft']}" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="{t['bg0']}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1280" height="120" fill="url(#fbg)"/>
  <rect width="1280" height="120" fill="url(#fmesh)">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="12s" repeatCount="indefinite"/>
  </rect>
''']
    # Mini grid
    lines.append(f'  <g stroke="{t["grid_faint"]}" stroke-width="1" fill="none" opacity="0.5">')
    for x in range(0, 1281, 40):
        lines.append(f'    <line x1="{x}" y1="0" x2="{x}" y2="120"/>')
    for y in range(0, 121, 40):
        lines.append(f'    <line x1="0" y1="{y}" x2="1280" y2="{y}"/>')
    lines.append('  </g>')
    # Rule
    lines.append(f'''  <line x1="64" y1="28" x2="1216" y2="28" stroke="{t['circuit']}" stroke-width="1" opacity="0.6">
    <animate attributeName="opacity" values="0.35;0.7;0.35" dur="8s" repeatCount="indefinite"/>
  </line>
''')
    # Particles
    lines.append(f'  <g fill="{t["particle"]}">')
    for i, (x, y, r, op, dur, dx, dy, delay) in enumerate(particles):
        fy = 40 + (y % 50)
        lines.append(f'''    <circle cx="{x}" cy="{fy}" r="{r * 0.85:.2f}" opacity="{op * 0.8:.2f}">
      <animateTransform attributeName="transform" type="translate" values="0,0; {dx * 0.5:.0f},{dy * 0.3:.0f}; 0,0" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>
    </circle>''')
    lines.append('  </g>')
    # Mark + text
    lines.append(f'''  <circle cx="76" cy="68" r="4" fill="{t['accent']}">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite"/>
  </circle>
  <text x="92" y="73" fill="{t['ink']}" font-family="{FONT_UI}" font-size="15" font-weight="500">Cael Findley</text>
  <text x="1216" y="73" text-anchor="end" fill="{t['faint']}" font-family="{FONT_MONO}" font-size="11" letter-spacing="1">TEXAS A&amp;M · CS</text>
  <rect width="1280" height="120" fill="none" stroke="{t['vignette']}" stroke-width="32" opacity="0.35"/>
</svg>
''')
    return '\n'.join(lines)


def main():
    for theme in ("dark", "light"):
        (OUT / f"header-{theme}.svg").write_text(header_svg(theme), encoding="utf-8")
        (OUT / f"footer-{theme}.svg").write_text(footer_svg(theme), encoding="utf-8")
        h = (OUT / f"header-{theme}.svg").read_text(encoding="utf-8")
        f = (OUT / f"footer-{theme}.svg").read_text(encoding="utf-8")
        print(f"header-{theme}.svg: {len(h.splitlines())} lines, {len(h)} bytes")
        print(f"footer-{theme}.svg: {len(f.splitlines())} lines, {len(f)} bytes")


if __name__ == "__main__":
    main()
