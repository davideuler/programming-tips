

```
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright_stealth import stealth_async

URL = "https://www.etsy.com/listing/1658800956/derby-skate-straps"
OUT = "etsy_listing.png"
PROFILE_DIR = Path("pw-chrome-profile")  # fresh profile → no extensions/adblock

BLOCK_STRINGS = (
    "please enable js and disable any ad blocker",
    "please enable javascript and disable any ad blocker",
    "press & hold",
    "press and hold",
    "are you a human",
    "unusual traffic",
)

async def accept_consent_if_present(page):
    """Dismiss common GDPR/cookie walls so content can render."""
    selectors = [
        'button:has-text("Accept all")',
        'button:has-text("Accept")',
        'button:has-text("I agree")',
        '[data-gdpr-single-choice-accept]',
        'button[aria-label="Accept"]',
    ]
    for sel in selectors:
        try:
            await page.locator(sel).first.click(timeout=5500)
            await page.wait_for_timeout(4500)
            break
        except Exception:
            pass

async def looks_blocked(page) -> bool:
    """Heuristic for Etsy's anti-bot page."""
    try:
        html = (await page.content() or "") + " " + (await page.title() or "")
        text = html.lower()
        return any(s in text for s in BLOCK_STRINGS)
    except Exception:
        return False

async def launch_persistent_chrome(pw, use_channel=True):
    """Launch a clean, persistent Chrome context (no extensions)."""
    PROFILE_DIR.mkdir(exist_ok=True)
    kwargs = dict(
        user_data_dir=str(PROFILE_DIR),
        headless=False,
        java_script_enabled=True,
        viewport={"width": 1380, "height": 900},
        locale="en-US",
        timezone_id="UTC",
    )
    if use_channel:
        kwargs["channel"] = "chrome"  # real Chrome if installed
    try:
        return await pw.chromium.launch_persistent_context(**kwargs)
    except Exception:
        # Fallback to bundled Chromium if Chrome channel isn't available
        if use_channel:
            return await launch_persistent_chrome(pw, use_channel=False)
        raise

async def try_with_chrome(pw, url, out_path, use_stealth=False) -> bool:
    context = await launch_persistent_chrome(pw)
    page = await context.new_page()
    try:
        if use_stealth:
            try:
                await stealth_async(page)
            except Exception:
                pass  # Stealth isn't critical; continue without it

        await page.goto(url, wait_until="domcontentloaded", timeout=5000)
        await accept_consent_if_present(page)
        # Allow late scripts/ads to settle; Etsy is JS-heavy
        #await page.wait_for_load_state("networkidle")
        if await looks_blocked(page):
            return False

        await page.wait_for_timeout(3000)
        await page.screenshot(path=out_path, full_page=True)
        return True
    finally:
        await context.close()

async def try_with_webkit(pw, url, out_path) -> bool:
    browser = await pw.webkit.launch(headless=False)
    context = await browser.new_context(
        java_script_enabled=True,
        viewport={"width": 1380, "height": 900},
        locale="en-US",
        timezone_id="UTC",
    )
    page = await context.new_page()
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=5000)
        await accept_consent_if_present(page)
        await page.wait_for_load_state("networkidle")
        if await looks_blocked(page):
            return False

        await page.screenshot(path=out_path, full_page=True)
        return True
    finally:
        await context.close()
        await browser.close()

async def main():
    async with async_playwright() as pw:
        out = OUT

        # 1) Chrome, clean profile, without stealth
        print("1. Trying with chrome...")
        ok = await try_with_chrome(pw, URL, out, use_stealth=False)

        # 2) Retry with stealth (sometimes helps, sometimes hurts)
        if not ok:
            print("2. Failed, Retrying with stealth...")
            ok = await try_with_chrome(pw, URL, out, use_stealth=True)

        # 3) Fallback: WebKit
        if not ok:
            print("3. Failed, Retrying with webkit...")
            ok = await try_with_webkit(pw, URL, out)

        # 4) Last resort: let you solve any human check once, then capture
        if not ok:
            print("4. Failed, Retrying with chrome...")
            context = await launch_persistent_chrome(pw)
            page = await context.new_page()
            await page.goto(URL)
            print(
                "\nIf you see a human check or the 'enable JS' page, solve/continue in the browser window."
            )
            input("Press ENTER here when the listing is visible to capture the screenshot...")
            await page.screenshot(path=out, full_page=True)
            await context.close()

        print(f"Saved {out}")

if __name__ == "__main__":
    asyncio.run(main())


```
