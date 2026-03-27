"""Debug script — intercept network requests to find the combo data API endpoint."""
from playwright.sync_api import sync_playwright
import time, json, re

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 900}, locale="en-US")
    page = ctx.new_page()

    # Capture all network requests
    all_requests = []
    page.on("request", lambda req: all_requests.append({
        "url": req.url, "method": req.method, "type": req.resource_type
    }))

    page.goto(
        "https://beybladexmeta.com/analytics?page=1&sort=score&order=desc&season=All+Time",
        timeout=25000, wait_until="networkidle",
    )

    # Show all fetch/XHR and /_next/data requests
    api_reqs = [r for r in all_requests if r["type"] in ("fetch", "xhr")]
    next_data_reqs = [r for r in all_requests if "_next/data" in r["url"]]
    print(f"Total requests: {len(all_requests)}")
    print(f"Fetch/XHR: {len(api_reqs)}")
    for r in api_reqs:
        print(f"  [{r['method']}] {r['url'][:150]}")
    print(f"\n_next/data requests: {len(next_data_reqs)}")
    for r in next_data_reqs:
        print(f"  [{r['method']}] {r['url'][:150]}")

    # Check __NEXT_DATA__
    next_data = page.evaluate("() => JSON.stringify(window.__NEXT_DATA__ || null)")
    if next_data and next_data != "null":
        d = json.loads(next_data)
        print(f"\n__NEXT_DATA__ keys: {list(d.keys())}")
        if "props" in d and "pageProps" in d["props"]:
            pp = d["props"]["pageProps"]
            print(f"  pageProps keys: {list(pp.keys())}")
            print(f"  pageProps preview: {json.dumps(pp)[:600]}")
    else:
        print("\n__NEXT_DATA__ is empty/absent (App Router or no SSR data)")

    # Try clicking the next-page button by locating it near the "Pagina" text  
    page.evaluate("document.querySelector('[class*=pagina], [class*=Pagina]')")
    pag_count = page.locator("text=/Pagina \\d+ di \\d+/").count()
    print(f"\nPagination text elements: {pag_count}")
    if pag_count:
        pag_el = page.locator("text=/Pagina \\d+ di \\d+/").first
        parent_html = pag_el.evaluate("el => el.closest('div').outerHTML")
        print(f"Pagination parent:\n{parent_html[:1000]}")

    browser.close()
