"""Fetch NVIDIA pages with curl and save readable text to reference_text/nvidia_pages/.
Usage: python3 -I tools/scrape.py URL [URL ...]   (skips pages already saved)"""
import html, re, subprocess, sys, pathlib, time
from html.parser import HTMLParser

OUT = pathlib.Path(__file__).resolve().parent.parent / "reference_text" / "nvidia_pages"

class Text(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "nav", "footer", "header"}
    BLOCK = {"p", "div", "li", "h1", "h2", "h3", "h4", "tr", "br", "section", "td", "th"}
    def __init__(self):
        super().__init__(); self.out = []; self.skip = 0
    def handle_starttag(self, t, a):
        if t in self.SKIP: self.skip += 1
        if t in self.BLOCK: self.out.append("\n")
        if t in ("h1", "h2", "h3"): self.out.append("## ")
    def handle_endtag(self, t):
        if t in self.SKIP and self.skip: self.skip -= 1
    def handle_data(self, d):
        if not self.skip: self.out.append(d)

def slug(u):
    return re.sub(r"[^a-z0-9]+", "_", u.split("//", 1)[1].lower()).strip("_")[:120] + ".md"

for u in sys.argv[1:]:
    f = OUT / slug(u)
    if f.exists():
        print("skip", u); continue
    r = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", "Mozilla/5.0 (Macintosh) research-fetch", "-w", "\n%{http_code}", u],
                       capture_output=True, text=True, errors="replace")
    body, code = r.stdout.rsplit("\n", 1)
    p = Text(); p.feed(body)
    text = re.sub(r"[ \t\xa0]+", " ", html.unescape("".join(p.out)))
    text = re.sub(r"\n\s*\n+", "\n\n", text).strip()
    f.write_text(f"Source: {u}\nFetched: {time.strftime('%Y-%m-%d')}\nHTTP: {code}\n\n{text}\n")
    print(code, len(text), u)
    time.sleep(1)
