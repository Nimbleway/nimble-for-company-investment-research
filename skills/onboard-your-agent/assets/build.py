#!/usr/bin/env python3
"""Build the onboarding assets from one data source.

Writes, next to this script:
  benchmark-chart.svg  the benchmark scatter as static SVG (no JS, light/dark aware)
  onboarding.html      chart + five tiles, self-contained (no scripts, no CDN)
  onboarding.png       a screenshot of onboarding.html (needs Google Chrome)

Run after any change to the benchmark numbers or tile copy:
  python3 skills/onboard-your-agent/assets/build.py
The numbers must match benchmark/README.md and the table in ../SKILL.md.
"""
import html
import pathlib
import shutil
import subprocess

HERE = pathlib.Path(__file__).resolve().parent

TITLE = "Deep research task comparison for finance"
CAPTION = "Finance Use-Case Benchmark v2, 40 tasks, November 2026. Higher and further left is better."

# (provider, F1 accuracy + coverage, cost per run in USD). Nimble first = accent.
PROVIDERS = [
    ("Nimble", 0.594, 0.45),
    ("Claude Opus 5.5", 0.583, 0.79),
    ("GPT-6.1 Sol", 0.513, 0.64),
    ("Exa", 0.455, 0.48),
    ("Parallel", 0.418, 0.54),
    ("Firecrawl", 0.388, 0.36),
]

TILES = [
    ("Deep research", "Web Search Agents API",
     "13 hedge fund research agents (deep dive, catalysts, filing changes, red flags, credit, merger arb, channel checks) plus custom agents. Cited answers in about 5 to 15 minutes.",
     "Underwrite Duolingo long on paid subscriber growth."),
    ("Fast search", "Search + Extract APIs",
     "Answers in seconds from filings, IR pages, regulators and news, with dated primary-source citations.",
     "What did NVDA's latest 8-K disclose?"),
    ("Filings, PDFs & media", "Extract file parsing + Media API",
     "Turn 10-K exhibits, decks, credit and merger agreements into markdown; download files and webcasts to disk or S3.",
     "Pull the debt table from this credit agreement."),
    ("Alt data at scale", "Extract Templates + Jobs API",
     "Prices, reviews, jobs and store data from 800+ Extract Templates, run as batches or scheduled jobs into S3 or Databricks.",
     "Track Celsius prices at Walmart and Target daily."),
]
INTEGRATE_TITLE = "Try asking Nimble your most complex web research questions"
INTEGRATE_TEXT = "Once you're done testing, call the same APIs from your own apps and agents (MCP, SDK, CLI, & more):"
INTEGRATE_URL = "https://docs.nimbleway.com/integrations/overview"

# Plot geometry (viewBox units).
W, H = 640, 300
L, R, T, B = 64, 560, 16, 248
X_MAX = 0.9
Y_MIN, Y_MAX = 0.30, 0.65


def px(cost):
    return L + cost / X_MAX * (R - L)


def py(score):
    return B - (score - Y_MIN) / (Y_MAX - Y_MIN) * (B - T)


def chart_svg(standalone):
    e = html.escape
    out = []
    style = """
  .grid{stroke:#e1e0d9;stroke-width:1}
  .axis{stroke:#c3c2b7;stroke-width:1}
  .tick{fill:#898781;font-size:11px}
  .ttl{fill:#52514e;font-size:12px}
  .lbl{fill:#52514e;font-size:12px}
  .lbl.n{fill:#2a78d6;font-weight:600}
  .pt{fill:#888780;stroke:#fcfcfb;stroke-width:2}
  .pt.n{fill:#2a78d6}
  @media (prefers-color-scheme: dark){
    .grid{stroke:#2c2c2a}.axis{stroke:#383835}
    .ttl,.lbl{fill:#c3c2b7}.lbl.n,.pt.n{fill:#3987e5}.pt{stroke:#1a1a19}
  }"""
    ns = ' xmlns="http://www.w3.org/2000/svg"' if standalone else ""
    out.append(f'<svg{ns} viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="bc-title bc-desc" '
               f'font-family="system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif">')
    out.append(f'<title id="bc-title">{e(TITLE)}</title>')
    desc = "; ".join(f"{n} {s:.3f} at ${c:.2f}" for n, s, c in PROVIDERS)
    out.append(f'<desc id="bc-desc">F1 accuracy + coverage versus cost per run. {e(desc)}.</desc>')
    if standalone:
        out.append(f"<style>{style}\n</style>")
    for i in range(8):
        v = Y_MIN + i * 0.05
        y = py(v)
        out.append(f'<line class="{"axis" if i == 0 else "grid"}" x1="{L}" x2="{R}" y1="{y:.1f}" y2="{y:.1f}"/>')
        out.append(f'<text class="tick" x="{L - 8}" y="{y + 4:.1f}" text-anchor="end">{v:.2f}</text>')
    for i in range(7):
        v = i * 0.15
        x = px(v)
        out.append(f'<text class="tick" x="{x:.1f}" y="{B + 18}" text-anchor="middle">${v:.2f}</text>')
    out.append(f'<text class="ttl" x="{(L + R) / 2:.0f}" y="{H - 6}" text-anchor="middle">Cost per run (USD)</text>')
    out.append(f'<text class="ttl" transform="translate(14 {(T + B) / 2:.0f}) rotate(-90)" text-anchor="middle">F1 accuracy + coverage</text>')
    for i, (name, score, cost) in enumerate(PROVIDERS):
        x, y = px(cost), py(score)
        n = " n" if i == 0 else ""
        r = 7 if i == 0 else 5.5
        out.append(f'<circle class="pt{n}" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>')
        out.append(f'<text class="lbl{n}" x="{x + 11:.1f}" y="{y + 4:.1f}">{e(name)}</text>')
    out.append("</svg>")
    return "\n".join(out), style


def page_html(svg, svg_style):
    e = html.escape
    tiles = "\n".join(
        f'''    <div class="tile">
      <p class="t">{e(t)}</p>
      <p class="api">{e(api)}</p>
      <p class="d">{e(d)}</p>
      <p class="ex">&ldquo;{e(ex)}&rdquo;</p>
    </div>''' for t, api, d, ex in TILES)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nimble for investment research</title>
<style>
  :root{{--bg:#ffffff;--card:#ffffff;--soft:#f6f5f2;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;--line:rgba(11,11,11,.12);--accent:#2a78d6}}
  @media (prefers-color-scheme: dark){{:root{{--bg:#1a1a19;--card:#232321;--soft:#2a2a28;--ink:#f0efec;--ink2:#c3c2b7;--muted:#898781;--line:rgba(255,255,255,.12);--accent:#3987e5}}}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif}}
  main{{max-width:720px;margin:0 auto;padding:20px 16px 24px}}
  h1{{font-size:17px;font-weight:600;margin:0 0 4px}}
  .cap{{font-size:12px;color:var(--muted);margin:2px 0 20px}}
  h2{{font-size:15px;font-weight:600;margin:0 0 10px}}
  .grid4{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}}
  @media (max-width:560px){{.grid4{{grid-template-columns:1fr}}}}
  .tile{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px}}
  .tile p{{margin:0}}
  .t{{font-weight:600;font-size:14px}}
  .api{{font-size:12px;color:var(--accent);margin:2px 0 6px!important}}
  .d{{font-size:13px;color:var(--ink2);margin-bottom:6px!important}}
  .ex{{font-size:12px;color:var(--muted);font-style:italic}}
  .wide{{background:var(--soft);border-radius:12px;padding:12px 14px;margin-top:10px;font-size:13px}}
  .wide p{{margin:0}}
  .wide a{{color:var(--accent)}}
  {svg_style}
</style>
</head>
<body>
<main>
  <h1>{e(TITLE)}</h1>
  {svg}
  <p class="cap">{e(CAPTION)}</p>
  <h2>Test Nimble's APIs on these use cases, right here in your AI.</h2>
  <div class="grid4">
{tiles}
  </div>
  <div class="wide">
    <p><strong>{e(INTEGRATE_TITLE)}</strong></p>
    <p style="color:var(--ink2)">{e(INTEGRATE_TEXT)} <a href="{INTEGRATE_URL}">{INTEGRATE_URL.removeprefix("https://")}</a></p>
  </div>
</main>
</body>
</html>
'''


def main():
    svg, style = chart_svg(standalone=True)
    (HERE / "benchmark-chart.svg").write_text(svg + "\n")
    inline_svg, _ = chart_svg(standalone=False)
    (HERE / "onboarding.html").write_text(page_html(inline_svg, style))
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or \
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if pathlib.Path(chrome).exists():
        subprocess.run([chrome, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=2",
                        "--window-size=720,920", f"--screenshot={HERE / 'onboarding.png'}",
                        (HERE / "onboarding.html").as_uri()], check=True, capture_output=True)
    else:
        print("Chrome not found; onboarding.png not rebuilt")
    print("built", ", ".join(p.name for p in sorted(HERE.glob("*")) if p.suffix in {".svg", ".html", ".png"}))


if __name__ == "__main__":
    main()
