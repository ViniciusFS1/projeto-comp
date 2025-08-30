from crawler import multi_page_search
from utils import *

if __name__ == "__main__":
    target = "example"
    search_patterns = txt_to_list("search_patterns.txt")

    results = multi_page_search(target, search_patterns, page_limit=2)

    for res in results:
        print(f" - {res}")