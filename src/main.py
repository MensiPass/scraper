from pathlib import Path
from bs4 import BeautifulSoup
import requests
from time import sleep
from urllib.parse import urljoin

#request site and download first page
page1 = "https://books.toscrape.com/catalogue/page-1.html"
timeout = 10
delay=0.5
#user-agent explaining who we are
header = {
    "User-Agent": "FlyRankInternshipA9/1.0(https://github.com/MensiPass/scraper)"
}


#function to make request, get books, save data to folder in cache  and check ststus code
def download_books(url: str) -> str:
    
    # get the page filename from the URL,split from the end by / then take last
    filename = url.rstrip("/").split("/")[-1]

    # create the cache path for every url
    page_cache_path = (
        Path(__file__).resolve().parent.parent
        / "cache"
        / filename
    )

    # check if already exist in cache
    if page_cache_path.exists():
        print(f"CACHE HIT")
        return page_cache_path.read_text(encoding="utf-8")

    # request the website from url
    print(f"FETCH: {url}")

    response = requests.get(
        url,
        headers=header,
        timeout=timeout,
    )

    print(f"HTTP status: {response.status_code}")

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to download page: HTTP {response.status_code}"
        )

    # create cache folder
    page_cache_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # save and return HTML
    page_cache_path.write_text(
        response.text,
        encoding="utf-8",
    )

    #print(f"Saved cache: {page_cache_path}")

    return response.text

#page processing, for html and page url parse and collect links and next url and return two values(in form of tuple)
def parse_catalogue_page(
    html: str,
    page_url: str,
) -> tuple[list[str], str | None]:

    # parse html
    soup = BeautifulSoup(html, "html.parser")

    book_links = []

    #find article tag with product_pod class and inside h3 a
    for article in soup.select("article.product_pod"):
        link = article.select_one("h3 a")

        #if link exist take href atribute 
        if link and link.get("href"):
            href = link["href"]

            #create absolute url
            absolute_url = urljoin(page_url, href)

            #add link to book links
            book_links.append(absolute_url)

    # inside same htnl find li with class next and select a tag
    next_link = soup.select_one("li.next a")

    next_url = None
    # take content of href and create url for next page
    if next_link and next_link.get("href"):
        next_url = urljoin(page_url, next_link["href"])

    #return two values
    return book_links, next_url


#collect links from every page
def collect_links() -> list[str]:
    all_links = []
    #start with page one
    current_url = page1

    #we want 3 pages, range gives us 1,2,3
    for page_number in range(1, 4):

        html = download_books(current_url)

        links, next_url = parse_catalogue_page(
            html,
            current_url,
        )

        all_links.extend(links)

        # Stop after page 3
        if page_number == 3:
            break

        if next_url is None:
            raise RuntimeError(
                f"Page {page_number} has no next link"
            )
        #url for next page to process
        current_url = next_url

    # Remove duplicates while keeping original order
    unique_links = list(dict.fromkeys(all_links))

    # print(f"Total links: {len(all_links)}")
    # print(f"Unique links: {len(unique_links)}")

    return unique_links

#main function to call
def main()->None:
    links = collect_links()
    file_num =0
    cache_path = (
            Path(__file__).resolve().parent.parent
            / "cache"
        )
    if cache_path.exists():
        file_num = sum(1 for item in cache_path.iterdir() if item.is_file())
    print(f"catalogue_pages={file_num} discovered= {len(links)} unique_urls={len(links)}")


if __name__ == "__main__":
    main()