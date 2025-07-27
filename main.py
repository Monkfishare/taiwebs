from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "https://en.taiwebs.com/sitemap/index.rss"
    sb.activate_cdp_mode(url)
    sb.sleep(5)
    sb.uc_gui_click_captcha()
    sb.sleep(10)
    sb.uc_gui_click_captcha()
    sb.sleep(10)

    page_content = sb.get_page_source()
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(page_content)
    print("Page source saved as page.html")