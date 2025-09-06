from crawler import multi_page_search
from utils import *

if __name__ == "__main__":
    target = "teste"
    search_patterns = load_patterns("search_patterns.txt")

    if not search_patterns:
        print("[WARNING] No patterns loaded. Example pattern:")
        print("https://pt.wikipedia.org/wiki/{target}?page={page}")

    results = multi_page_search(target, search_patterns, page_limit=2)

    print("\n[RESULTS]")
    for res in results:
        print(f" - {res}")