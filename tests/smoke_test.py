from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")

required = [
    '<canvas id="game"></canvas>',
    'id="stock"',
    'id="won"',
    'id="drop"',
    'id="restart"',
    'requestAnimationFrame(loop)',
]

missing = [item for item in required if item not in html]
if missing:
    raise SystemExit(f"Missing required game markers: {missing}")

scripts = re.findall(r"<script>(.*?)</script>", html, flags=re.S)
if len(scripts) != 1:
    raise SystemExit(f"Expected exactly one inline script, found {len(scripts)}")

with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as f:
    f.write(scripts[0])
    js_path = f.name

result = subprocess.run(["node", "--check", js_path], capture_output=True, text=True)
if result.returncode != 0:
    raise SystemExit(result.stderr)

print("Coin pusher smoke test passed")
