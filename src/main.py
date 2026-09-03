from pathlib import Path

import requests

#request site and download first page
site_url = "https://books.toscrape.com/catalogue/page-1.html"
timeout = 10

#user-agent explaining who we are
header = {
    "User-Agent": "FlyRankInternshipA9/1.0(https://github.com/MensiPass/scraper)"
}
#where to chache data folder, inside parent folder create cache and html file
cache_path = Path(__file__).resolve().parent.parent / "cache" / "catalogue-page-1.html"

#function to make request, get books, save data to folder in cache  and check ststus code
def download_books() -> None:
    #create cche folder if it doesnt exist where the data is saved
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Requesting: {site_url}")

    # First run: fetch from the website with Request library
    print("FETCH")
    response = requests.get(
        site_url,
        headers=header,
        timeout=timeout,
    )

    #show status code after request
    print(f"HTTP status: {response.status_code}")

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to download catalogue page: HTTP {response.status_code}"
        )
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(response.text, encoding="utf-8")

    print(f"Saved cache: {cache_path}")

#main function to call
def main():
    # main logic and code
    #first check if cache already exist and html inside, if not then call function to fetch data
    if cache_path.exists():
        html = cache_path.read_text(encoding="utf-8")
        print("CACHE HIT")
        print(f"response size: {len(html.encode('utf-8'))} bytes")
    else:
        download_books()

if __name__ == "__main__":
    main()