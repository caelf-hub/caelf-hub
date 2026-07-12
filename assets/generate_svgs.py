#!/usr/bin/env python3
"""Generate premium SMIL SVG header/footer pairs for caelf-hub profile."""

from pathlib import Path

OUT = Path(__file__).resolve().parent
FONT_UI = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
FONT_MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# Texas A&M Aggie Maroon (#500000) as primary brand signal
# bg0 matched to GitHub canvas so soft fades blend cleanly
THEMES = {
    "dark": {
        "bg0": "#0d1117",
        "bg1": "#161016",
        "grid": "#4a2428",
        "grid_faint": "#2a1618",
        "ink": "#faf7f7",
        "muted": "#c9b0b3",
        "faint": "#8f6e72",
        "accent": "#c45c6a",
        "accent_soft": "#500000",
        "circuit": "#6b3038",
        "node": "#e8b4ba",
        "stream": "#8b4a52",
        "mesh_a": "#2a1014",
        "mesh_b": "#1a0c10",
        "mesh_c": "#301018",
        "particle": "#e8c8cc",
        "cursor": "#e8b4ba",
        "vignette": "#0d1117",
        "rail": "#500000",
        "white": "#ffffff",
    },
    "light": {
        "bg0": "#ffffff",
        "bg1": "#f7f0f0",
        "grid": "#d4b8bc",
        "grid_faint": "#eadfe1",
        "ink": "#1a0808",
        "muted": "#5c3034",
        "faint": "#8a5a5e",
        "accent": "#500000",
        "accent_soft": "#6a2020",
        "circuit": "#b89094",
        "node": "#500000",
        "stream": "#8b5054",
        "mesh_a": "#f2e4e6",
        "mesh_b": "#f6ecee",
        "mesh_c": "#efe0e2",
        "particle": "#500000",
        "cursor": "#500000",
        "vignette": "#ffffff",
        "rail": "#500000",
        "white": "#ffffff",
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
      <stop offset="0%" stop-color="{t['accent_soft']}" stop-opacity="0.55"/>
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
    <!-- Soft blend into GitHub page background -->
    <linearGradient id="edgeFadeY" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="white" stop-opacity="0"/>
      <stop offset="8%" stop-color="white" stop-opacity="1"/>
      <stop offset="72%" stop-color="white" stop-opacity="1"/>
      <stop offset="100%" stop-color="white" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="edgeFadeX" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="white" stop-opacity="0.15"/>
      <stop offset="4%" stop-color="white" stop-opacity="1"/>
      <stop offset="96%" stop-color="white" stop-opacity="1"/>
      <stop offset="100%" stop-color="white" stop-opacity="0.15"/>
    </linearGradient>
    <mask id="pageBlend" maskUnits="userSpaceOnUse" x="0" y="0" width="1280" height="360">
      <rect width="1280" height="360" fill="url(#edgeFadeY)"/>
    </mask>
  </defs>
  <g mask="url(#pageBlend)">
  <rect width="1280" height="360" fill="url(#bgGrad)"/>
  <rect width="1280" height="360" fill="url(#mesh1)">
    <animate attributeName="opacity" values="0.7;1;0.7" dur="14s" repeatCount="indefinite"/>
  </rect>
  <rect width="1280" height="360" fill="url(#mesh2)">
    <animate attributeName="opacity" values="0.6;0.95;0.6" dur="16s" begin="1s" repeatCount="indefinite"/>
  </rect>
  <rect width="1280" height="360" fill="url(#mesh3)" opacity="0.8"/>
'''


def vignette(t: dict, height: int = 360) -> str:
    # Close the mask group opened in mesh_layer; no hard box edge
    return "  </g>\n"


def header_svg(theme: str) -> str:
    t = THEMES[theme]
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 360" width="1280" height="360" role="img" aria-labelledby="title desc">
  <title id="title">Cael Findley — Computer Science, Texas A&amp;M</title>
  <desc id="desc">Animated profile banner ({theme} mode): engineering grid, circuit traces, and typewriter introduction</desc>
{mesh_layer(t)}{grid_layer(t)}{particles_layer(t)}{streams_layer(t)}{neural_layer(t)}{circuit_layer(t)}{brand_rail(t)}{hero_text(t)}{vignette(t)}</svg>
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


def brand_rail(t: dict, height: int = 360) -> str:
    return f'''  <!-- Aggie maroon brand rail -->
  <rect x="0" y="0" width="8" height="{height}" fill="{t['rail']}">
    <animate attributeName="opacity" values="0.85;1;0.85" dur="6s" repeatCount="indefinite"/>
  </rect>
  <rect x="8" y="0" width="2" height="{height}" fill="{t['white']}" opacity="0.55"/>
'''


def hero_text(t: dict) -> str:
    return f'''  <!-- Hero typography -->
  <g font-family="{FONT_UI}">
    <text x="64" y="56" fill="{t['accent']}" font-family="{FONT_MONO}" font-size="11" font-weight="600" letter-spacing="2.5" opacity="0">
      TEXAS A&amp;M UNIVERSITY
      <animate attributeName="opacity" from="0" to="1" begin="0.1s" dur="0.5s" fill="freeze"/>
    </text>
    <text x="64" y="148" fill="{t['ink']}" font-size="52" font-weight="600" letter-spacing="-0.8" opacity="0">
      Cael Findley
      <animate attributeName="opacity" from="0" to="1" begin="0.3s" dur="0.8s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate" values="0,10; 0,0" begin="0.3s" dur="0.8s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.2 0.8 0.2 1"/>
    </text>
    <rect x="400" y="112" width="2.5" height="42" fill="{t['cursor']}" opacity="0" rx="0.5">
      <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.18;0.19;0.48;0.49;1" dur="1.1s" begin="1.0s" repeatCount="indefinite"/>
      <animate attributeName="x" values="64;400" dur="1.4s" begin="0.3s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"/>
    </rect>
    <text x="64" y="188" fill="{t['muted']}" font-size="18" font-weight="500" letter-spacing="0.2" opacity="0">
      Computer Science  ·  College Station, TX
      <animate attributeName="opacity" from="0" to="1" begin="1.2s" dur="0.7s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate" values="0,8; 0,0" begin="1.2s" dur="0.7s" fill="freeze"/>
    </text>
  </g>
  <!-- Focus chips — maroon framed -->
  <g font-family="{FONT_UI}" font-size="13" font-weight="500" opacity="0">
    <g>
      <rect x="64" y="220" width="158" height="28" rx="6" fill="{t['accent']}" fill-opacity="0.18" stroke="{t['accent']}" stroke-opacity="0.75" stroke-width="1.25"/>
      <text x="143" y="238" text-anchor="middle" fill="{t['ink']}">Artificial Intelligence</text>
    </g>
    <g>
      <rect x="234" y="220" width="152" height="28" rx="6" fill="{t['accent']}" fill-opacity="0.12" stroke="{t['accent']}" stroke-opacity="0.55" stroke-width="1.25"/>
      <text x="310" y="238" text-anchor="middle" fill="{t['ink']}">Software Engineering</text>
    </g>
    <g>
      <rect x="398" y="220" width="78" height="28" rx="6" fill="{t['accent']}" fill-opacity="0.12" stroke="{t['accent']}" stroke-opacity="0.55" stroke-width="1.25"/>
      <text x="437" y="238" text-anchor="middle" fill="{t['ink']}">Systems</text>
    </g>
    <g>
      <rect x="488" y="220" width="138" height="28" rx="6" fill="{t['accent']}" fill-opacity="0.12" stroke="{t['accent']}" stroke-opacity="0.55" stroke-width="1.25"/>
      <text x="557" y="238" text-anchor="middle" fill="{t['ink']}">Machine Learning</text>
    </g>
    <animate attributeName="opacity" from="0" to="1" begin="1.9s" dur="0.8s" fill="freeze"/>
  </g>
  <!-- Accent measure -->
  <g opacity="0">
    <rect x="64" y="272" width="240" height="2" fill="{t['circuit']}" rx="1"/>
    <rect x="64" y="272" width="0" height="2" fill="{t['rail']}" rx="1">
      <animate attributeName="width" from="0" to="240" begin="2.5s" dur="1.2s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"/>
    </rect>
    <text x="64" y="296" fill="{t['accent']}" font-family="{FONT_MONO}" font-size="11" font-weight="600" letter-spacing="2">GIG &apos;EM  ·  ENGINEERING  ·  RESEARCH</text>
    <animate attributeName="opacity" from="0" to="1" begin="2.5s" dur="0.4s" fill="freeze"/>
  </g>
  <!-- Brand ticks -->
  <g font-family="{FONT_MONO}" font-size="9" fill="{t['accent']}" opacity="0.55">
    <text x="64" y="28">AGGIE</text>
    <text x="1220" y="28" text-anchor="end">MAROON #500000</text>
    <text x="64" y="318">CS · TEXAS A&amp;M</text>
    <text x="1220" y="318" text-anchor="end">COLLEGE STATION</text>
  </g>
'''


def footer_svg(theme: str) -> str:
    t = THEMES[theme]
    particles = PARTICLES[:36]
    body = []
    body.append(f'  <g stroke="{t["grid_faint"]}" stroke-width="1" fill="none" opacity="0.45">')
    for x in range(0, 1281, 40):
        body.append(f'    <line x1="{x}" y1="0" x2="{x}" y2="120"/>')
    for y in range(0, 121, 40):
        body.append(f'    <line x1="0" y1="{y}" x2="1280" y2="{y}"/>')
    body.append('  </g>')
    body.append(f'''  <line x1="64" y1="28" x2="1216" y2="28" stroke="{t['accent']}" stroke-width="1.25" opacity="0.55">
    <animate attributeName="opacity" values="0.35;0.8;0.35" dur="8s" repeatCount="indefinite"/>
  </line>
''')
    body.append(f'  <g fill="{t["particle"]}">')
    for i, (x, y, r, op, dur, dx, dy, delay) in enumerate(particles):
        fy = 40 + (y % 50)
        body.append(f'''    <circle cx="{x}" cy="{fy}" r="{r * 0.85:.2f}" opacity="{op * 0.8:.2f}">
      <animateTransform attributeName="transform" type="translate" values="0,0; {dx * 0.5:.0f},{dy * 0.3:.0f}; 0,0" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>
    </circle>''')
    body.append('  </g>')
    body.append(f'''  <circle cx="76" cy="68" r="4" fill="{t['accent']}">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite"/>
  </circle>
  <text x="92" y="68" fill="{t['ink']}" font-family="{FONT_UI}" font-size="15" font-weight="600">Cael Findley</text>
  <text x="92" y="86" fill="{t['accent']}" font-family="{FONT_MONO}" font-size="10" letter-spacing="1.5">GIG &apos;EM</text>
  <text x="1216" y="68" text-anchor="end" fill="{t['accent']}" font-family="{FONT_MONO}" font-size="11" font-weight="600" letter-spacing="1.5">TEXAS A&amp;M UNIVERSITY</text>
  <text x="1216" y="86" text-anchor="end" fill="{t['faint']}" font-family="{FONT_MONO}" font-size="10" letter-spacing="1">COMPUTER SCIENCE</text>
''')
    inner = "\n".join(body)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 120" width="1280" height="120" role="img" aria-labelledby="ftitle">
  <title id="ftitle">Cael Findley — footer</title>
  <defs>
    <linearGradient id="fbg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t['bg0']}"/>
      <stop offset="100%" stop-color="{t['bg1']}"/>
    </linearGradient>
    <radialGradient id="fmesh" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{t['accent_soft']}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{t['bg0']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="ffade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="white" stop-opacity="0"/>
      <stop offset="28%" stop-color="white" stop-opacity="1"/>
      <stop offset="100%" stop-color="white" stop-opacity="1"/>
    </linearGradient>
    <mask id="ffadeMask" maskUnits="userSpaceOnUse" x="0" y="0" width="1280" height="120">
      <rect width="1280" height="120" fill="url(#ffade)"/>
    </mask>
  </defs>
  <g mask="url(#ffadeMask)">
  <rect width="1280" height="120" fill="url(#fbg)"/>
  <rect width="1280" height="120" fill="url(#fmesh)">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="12s" repeatCount="indefinite"/>
  </rect>
  <rect x="0" y="0" width="8" height="120" fill="{t['rail']}"/>
  <rect x="8" y="0" width="2" height="120" fill="{t['white']}" opacity="0.55"/>
{inner}
  </g>
</svg>
'''


def divider_svg(theme: str) -> str:
    """Legacy alias — pulse node (used as about accent)."""
    return accent_about(theme)


def bridge_svg(theme: str) -> str:
    """After hero: soft falling particles."""
    t = THEMES[theme]
    dots = []
    for i in range(18):
        x = 80 + i * 64
        delay = i * 0.22
        dots.append(f'''  <circle cx="{x}" cy="20" r="1.6" fill="{t['accent']}" opacity="0.2">
    <animate attributeName="cy" values="8;40;8" dur="3.6s" begin="{delay}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.1;0.7;0.1" dur="3.6s" begin="{delay}s" repeatCount="indefinite"/>
  </circle>''')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 48" width="1280" height="48" role="img" aria-hidden="true">
  <path d="M200,24 H1080" fill="none" stroke="{t['accent']}" stroke-width="1" stroke-dasharray="2 12" opacity="0.35">
    <animate attributeName="stroke-dashoffset" from="0" to="-56" dur="5s" repeatCount="indefinite"/>
  </path>
{chr(10).join(dots)}
</svg>
'''


def accent_about(theme: str) -> str:
    """Breathing dual rings around a maroon core."""
    t = THEMES[theme]
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 56" width="1280" height="56" role="img" aria-hidden="true">
  <line x1="200" y1="28" x2="560" y2="28" stroke="{t['circuit']}" stroke-width="1" opacity="0.45"/>
  <line x1="720" y1="28" x2="1080" y2="28" stroke="{t['circuit']}" stroke-width="1" opacity="0.45"/>
  <circle cx="640" cy="28" r="4" fill="{t['accent']}">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite"/>
  </circle>
  <circle cx="640" cy="28" r="12" fill="none" stroke="{t['accent']}" stroke-width="1" opacity="0.4">
    <animate attributeName="r" values="10;16;10" dur="3s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.45;0.1;0.45" dur="3s" repeatCount="indefinite"/>
  </circle>
  <circle cx="640" cy="28" r="20" fill="none" stroke="{t['accent']}" stroke-width="1" opacity="0.2">
    <animate attributeName="r" values="16;24;16" dur="3s" begin="0.4s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.3;0.05;0.3" dur="3s" begin="0.4s" repeatCount="indefinite"/>
  </circle>
</svg>
'''


def accent_focus(theme: str) -> str:
    """Four nodes lighting in sequence — one per focus area."""
    t = THEMES[theme]
    xs = [400, 520, 640, 760]
    parts = []
    for i, x in enumerate(xs):
        parts.append(f'''  <circle cx="{x}" cy="28" r="5" fill="{t['accent']}" opacity="0.25">
    <animate attributeName="opacity" values="0.2;1;0.2" dur="3.2s" begin="{i * 0.8}s" repeatCount="indefinite"/>
    <animate attributeName="r" values="4;6.5;4" dur="3.2s" begin="{i * 0.8}s" repeatCount="indefinite"/>
  </circle>''')
        if i < len(xs) - 1:
            x2 = xs[i + 1]
            parts.append(f'''  <line x1="{x + 8}" y1="28" x2="{x2 - 8}" y2="28" stroke="{t['circuit']}" stroke-width="1.25" opacity="0.35">
    <animate attributeName="opacity" values="0.2;0.7;0.2" dur="3.2s" begin="{i * 0.8 + 0.3}s" repeatCount="indefinite"/>
  </line>''')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 56" width="1280" height="56" role="img" aria-hidden="true">
{chr(10).join(parts)}
</svg>
'''


def accent_projects(theme: str) -> str:
    """Circuit path drawing left to right."""
    t = THEMES[theme]
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 56" width="1280" height="56" role="img" aria-hidden="true">
  <path d="M260,28 H520 V18 H640 V38 H760 V28 H1020" fill="none" stroke="{t['accent']}" stroke-width="1.5" stroke-linecap="square" stroke-dasharray="900" stroke-dashoffset="900" opacity="0.85">
    <animate attributeName="stroke-dashoffset" values="900;0;0;900" keyTimes="0;0.45;0.7;1" dur="6s" repeatCount="indefinite"/>
  </path>
  <circle cx="520" cy="18" r="2.5" fill="{t['node']}">
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.2;0.75;1" dur="6s" repeatCount="indefinite"/>
  </circle>
  <circle cx="640" cy="38" r="2.5" fill="{t['node']}">
    <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.25;0.35;0.75;1" dur="6s" repeatCount="indefinite"/>
  </circle>
  <circle cx="760" cy="28" r="2.5" fill="{t['node']}">
    <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.35;0.45;0.75;1" dur="6s" repeatCount="indefinite"/>
  </circle>
</svg>
'''


def accent_research(theme: str) -> str:
    """Neural constellation — three hubs with pulsing links."""
    t = THEMES[theme]
    hubs = [(520, 18), (640, 38), (760, 18), (580, 40), (700, 14)]
    lines = [
        (0, 1), (1, 2), (0, 3), (1, 3), (1, 4), (2, 4),
    ]
    parts = []
    for i, (a, b) in enumerate(lines):
        x1, y1 = hubs[a]
        x2, y2 = hubs[b]
        parts.append(f'''  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t['circuit']}" stroke-width="1" opacity="0.25">
    <animate attributeName="opacity" values="0.15;0.65;0.15" dur="4s" begin="{i * 0.35}s" repeatCount="indefinite"/>
  </line>''')
    for i, (x, y) in enumerate(hubs):
        parts.append(f'''  <circle cx="{x}" cy="{y}" r="3" fill="{t['accent']}" opacity="0.5">
    <animate attributeName="opacity" values="0.3;1;0.3" dur="2.8s" begin="{i * 0.25}s" repeatCount="indefinite"/>
  </circle>''')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 56" width="1280" height="56" role="img" aria-hidden="true">
{chr(10).join(parts)}
</svg>
'''


def accent_stack(theme: str) -> str:
    """Rising bars — tech stack energy."""
    t = THEMES[theme]
    bars = []
    heights = [10, 18, 14, 24, 16, 22, 12, 20]
    for i, h in enumerate(heights):
        x = 480 + i * 40
        y = 40 - h
        bars.append(f'''  <rect x="{x}" y="{y}" width="14" height="{h}" rx="2" fill="{t['accent']}" opacity="0.35">
    <animate attributeName="height" values="{max(6, h-8)};{h};{max(6, h-8)}" dur="{2.4 + i * 0.15:.2f}s" begin="{i * 0.12}s" repeatCount="indefinite"/>
    <animate attributeName="y" values="{40 - max(6, h-8)};{y};{40 - max(6, h-8)}" dur="{2.4 + i * 0.15:.2f}s" begin="{i * 0.12}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.25;0.85;0.25" dur="{2.4 + i * 0.15:.2f}s" begin="{i * 0.12}s" repeatCount="indefinite"/>
  </rect>''')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 56" width="1280" height="56" role="img" aria-hidden="true">
  <line x1="460" y1="42" x2="820" y2="42" stroke="{t['circuit']}" stroke-width="1" opacity="0.4"/>
{chr(10).join(bars)}
</svg>
'''


def accent_experience(theme: str) -> str:
    """Chevron / arrow marching forward."""
    t = THEMES[theme]
    chevs = []
    for i in range(5):
        x = 480 + i * 70
        chevs.append(f'''  <polyline points="{x},16 {x + 18},28 {x},40" fill="none" stroke="{t['accent']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity="0.2">
    <animate attributeName="opacity" values="0.15;1;0.15" dur="2.5s" begin="{i * 0.35}s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0,0; 8,0; 0,0" dur="2.5s" begin="{i * 0.35}s" repeatCount="indefinite"/>
  </polyline>''')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 56" width="1280" height="56" role="img" aria-hidden="true">
{chr(10).join(chevs)}
</svg>
'''


def accent_opensource(theme: str) -> str:
    """Git-style branch fork animation."""
    t = THEMES[theme]
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 56" width="1280" height="56" role="img" aria-hidden="true">
  <path d="M560,28 H640" fill="none" stroke="{t['circuit']}" stroke-width="1.5" opacity="0.5"/>
  <path d="M640,28 Q700,28 740,16" fill="none" stroke="{t['accent']}" stroke-width="1.5" stroke-dasharray="120" stroke-dashoffset="120">
    <animate attributeName="stroke-dashoffset" values="120;0;0;120" keyTimes="0;0.4;0.7;1" dur="5s" repeatCount="indefinite"/>
  </path>
  <path d="M640,28 Q700,28 740,40" fill="none" stroke="{t['accent']}" stroke-width="1.5" stroke-dasharray="120" stroke-dashoffset="120">
    <animate attributeName="stroke-dashoffset" values="120;0;0;120" keyTimes="0;0.4;0.7;1" dur="5s" begin="0.35s" repeatCount="indefinite"/>
  </path>
  <circle cx="560" cy="28" r="4" fill="{t['accent']}">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="640" cy="28" r="3.5" fill="{t['node']}"/>
  <circle cx="740" cy="16" r="3.5" fill="{t['accent']}" opacity="0">
    <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.35;0.45;0.8;1" dur="5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="740" cy="40" r="3.5" fill="{t['accent']}" opacity="0">
    <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.4;0.5;0.8;1" dur="5s" begin="0.35s" repeatCount="indefinite"/>
  </circle>
</svg>
'''


def accent_education(theme: str) -> str:
    """Rotating diamond / academic mark."""
    t = THEMES[theme]
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 56" width="1280" height="56" role="img" aria-hidden="true">
  <line x1="220" y1="28" x2="580" y2="28" stroke="{t['circuit']}" stroke-width="1" opacity="0.4"/>
  <line x1="700" y1="28" x2="1060" y2="28" stroke="{t['circuit']}" stroke-width="1" opacity="0.4"/>
  <g transform="translate(640,28)">
    <polygon points="0,-12 12,0 0,12 -12,0" fill="none" stroke="{t['accent']}" stroke-width="1.5" opacity="0.85">
      <animateTransform attributeName="transform" type="rotate" values="0;360" dur="12s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.5;1;0.5" dur="4s" repeatCount="indefinite"/>
    </polygon>
    <circle cx="0" cy="0" r="3" fill="{t['accent']}">
      <animate attributeName="r" values="2.5;4;2.5" dur="2.5s" repeatCount="indefinite"/>
    </circle>
  </g>
</svg>
'''


def accent_stats(theme: str) -> str:
    """Contribution-graph style squares pulsing."""
    t = THEMES[theme]
    cells = []
    pattern = [0.2, 0.45, 0.7, 0.35, 0.9, 0.25, 0.55, 0.8, 0.4, 0.65, 0.3, 0.95, 0.5, 0.75, 0.35]
    for i, base in enumerate(pattern):
        x = 500 + (i % 15) * 18
        y = 16 + (i // 15) * 18
        # two rows
        row = i // 8
        col = i % 8
        x = 560 + col * 20
        y = 12 + row * 20
        if i >= 16:
            break
        cells.append(f'''  <rect x="{x}" y="{y}" width="14" height="14" rx="2" fill="{t['accent']}" opacity="{base}">
    <animate attributeName="opacity" values="{base};{min(1, base + 0.35):.2f};{base}" dur="{2.2 + (i % 5) * 0.3:.1f}s" begin="{i * 0.12}s" repeatCount="indefinite"/>
  </rect>''')
    # rebuild clean 2x8
    cells = []
    for row in range(2):
        for col in range(8):
            i = row * 8 + col
            base = 0.2 + ((i * 37) % 70) / 100
            x = 560 + col * 20
            y = 12 + row * 18
            cells.append(f'''  <rect x="{x}" y="{y}" width="14" height="14" rx="2" fill="{t['accent']}" opacity="{base:.2f}">
    <animate attributeName="opacity" values="{base:.2f};{min(1.0, base + 0.4):.2f};{base:.2f}" dur="{2.0 + (i % 4) * 0.35:.2f}s" begin="{i * 0.1}s" repeatCount="indefinite"/>
  </rect>''')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 56" width="1280" height="56" role="img" aria-hidden="true">
{chr(10).join(cells)}
</svg>
'''


def accent_connect(theme: str) -> str:
    """Two nodes drawing a link toward each other."""
    t = THEMES[theme]
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 56" width="1280" height="56" role="img" aria-hidden="true">
  <circle cx="520" cy="28" r="5" fill="{t['accent']}">
    <animate attributeName="cx" values="500;520;500" dur="4s" repeatCount="indefinite"/>
  </circle>
  <circle cx="760" cy="28" r="5" fill="{t['accent']}">
    <animate attributeName="cx" values="780;760;780" dur="4s" repeatCount="indefinite"/>
  </circle>
  <line x1="530" y1="28" x2="750" y2="28" stroke="{t['accent']}" stroke-width="1.5" stroke-dasharray="8 8" opacity="0.55">
    <animate attributeName="stroke-dashoffset" from="0" to="-32" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.3;0.85;0.3" dur="4s" repeatCount="indefinite"/>
  </line>
  <circle cx="640" cy="28" r="2.5" fill="{t['node']}">
    <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/>
  </circle>
</svg>
'''


ACCENTS = {
    "bridge": bridge_svg,
    "about": accent_about,
    "focus": accent_focus,
    "projects": accent_projects,
    "research": accent_research,
    "stack": accent_stack,
    "experience": accent_experience,
    "opensource": accent_opensource,
    "education": accent_education,
    "stats": accent_stats,
    "connect": accent_connect,
}


def main():
    accents_dir = OUT / "accents"
    accents_dir.mkdir(exist_ok=True)
    for theme in ("dark", "light"):
        (OUT / f"header-{theme}.svg").write_text(header_svg(theme), encoding="utf-8")
        (OUT / f"footer-{theme}.svg").write_text(footer_svg(theme), encoding="utf-8")
        # keep root bridge/divider for backwards compatibility
        (OUT / f"bridge-{theme}.svg").write_text(bridge_svg(theme), encoding="utf-8")
        (OUT / f"divider-{theme}.svg").write_text(accent_about(theme), encoding="utf-8")
        for name, fn in ACCENTS.items():
            path = accents_dir / f"{name}-{theme}.svg"
            path.write_text(fn(theme), encoding="utf-8")
            text = path.read_text(encoding="utf-8")
            print(f"{path.relative_to(OUT.parent)}: {len(text.splitlines())} lines")


if __name__ == "__main__":
    main()
