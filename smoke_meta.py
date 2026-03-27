from scraper_meta import scrape_page, _wait_for_combos, _get_pagination_info
from playwright.sync_api import sync_playwright

combos = []
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 900}, locale="en-US")
    page = ctx.new_page()
    page.route("**/*.{png,jpg,jpeg,gif,webp,svg,woff,woff2,ttf}", lambda r: r.abort())
    page.goto(
        "https://beybladexmeta.com/analytics?page=1&sort=score&order=desc&season=All+Time",
        timeout=20000,
        wait_until="domcontentloaded",
    )
    _wait_for_combos(page)
    cur, tot = _get_pagination_info(page)
    print(f"Pagination: page {cur} of {tot}")
    combos = scrape_page(page, 1, "All Time")
    browser.close()

print(f"Combos on page 1: {len(combos)}")
for c in combos[:5]:
    print(f"  rank={c.rank:3d}  blade={c.blade:20s}  {c.ratchet:5s}  {c.bit:12s}  score={c.score:7d}  1st={c.placements_1st}  win={c.win_rate}  podium={c.podium_rate}")
