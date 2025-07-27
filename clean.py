from bs4 import BeautifulSoup
import re

def clean_rss_content():
    with open("page.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    rss_div = soup.find("div", {"id": "webkit-xml-viewer-source-xml"})
    if not rss_div:
        return

    rss_xml = rss_div.decode_contents()
    rss_soup = BeautifulSoup(rss_xml, "xml")
    channel = rss_soup.find("channel")

    if channel:
        main_link = channel.find("link")
        if main_link and not main_link.get_text().strip():
            next_text = main_link.next_sibling
            if next_text and isinstance(next_text, str) and next_text.strip().startswith("http"):
                main_link.string = next_text.strip()
                next_text.extract()

        items = channel.find_all("item")
        for item in items:
            link_tag = item.find("link")
            if link_tag and not link_tag.get_text().strip():
                next_sibling = link_tag.next_sibling
                while next_sibling:
                    if isinstance(next_sibling, str):
                        text = next_sibling.strip()
                        if text.startswith("http"):
                            link_tag.string = text
                            next_sibling.extract()
                            break
                    next_sibling = next_sibling.next_sibling

            pubdate_tag = item.find("pubdate")
            if pubdate_tag:
                pubdate_tag.name = "pubDate"

        pubdate_tag = channel.find("pubdate")
        if pubdate_tag:
            pubdate_tag.name = "pubDate"
        lastbuild_tag = channel.find("lastbuilddate")
        if lastbuild_tag:
            lastbuild_tag.name = "lastBuildDate"

    cleaned_xml = str(rss_soup)
    cleaned_xml = re.sub(r'\n\s*\n', '\n', cleaned_xml)
    cleaned_xml = re.sub(r'>\s+<', '><', cleaned_xml)

    with open("rss.xml", "w", encoding="utf-8") as out:
        out.write(cleaned_xml)

if __name__ == "__main__":
    clean_rss_content()