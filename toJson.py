
from typing import Tuple
import re

RE_ID = r"Id:\s*(.*)(?=\n)"
RE_ASIN = r"ASIN:\s*(.*)(?=\n)"
RE_TITLE = r"title: (.*)(?=\n)"
RE_GROUP = r"group: (.*)(?=\n)"
RE_SALESRANK = r"salesrank: (.*)(?=\n)"
RE_SIMILAR = r"similar: (.*)(?=\n)"
RE_TOTAL = r"total: (\d*)"
RE_DOWNLOADED = r"downloaded: (\d*)"
RE_AVG_RATING = r"avg rating: (\d*)"
RE_DISCONTINUED = r"(discontinued product)"
RE_DATE = r"([^\s]*)\s*cutomer:"
RE_CUSTOMER = r"cutomer:\s*([^\s]*)"
RE_RATING = r"rating:\s*(\d*)"
RE_VOTES = r"votes:\s*(\d*)"
RE_HELPFUL = r"helpful:\s*(\d*)"

PRODUCT_ID = "Product_id"
PRODUCT_ASIN = "Product_ASIN"
PRODUCT_TITLE = "Product_title"
PRODUCT_GROUP = "Product_group"
PRODUCT_SALESRANK = "Product_salesrank"
PRODUCT_SIMILAR = "Similar_products"
REVIEW_CUSTOMER = "Review_Customer"
PRODUCT_CATEGORIES = "Product_categories"
PRODUCT_REVIEWS = "Product_reviews"
PRODUCT_TOTAL_REVIEWS = "Review_total_count"
PRODUCT_DOWNLOADED_REVIEWS = "Review_downloaded_count"
PRODUCT_AVG_RATING = "Product_avg_rating"
REVIEW_RATING = "Review_rating"
REVIEW_VOTES = "Review_votes"
REVIEW_HELPFUL = "Review_votes_helpful"
PRODUCT_DISCONTINUED = "Product_discontinued"

def read_product_from_index(text: str, start_index: int) -> Tuple[dict, int]: # return dictionary of product and index of last line of product
    product = {}
    current_index = start_index
    while not text[current_index] == "":
        line = text[current_index]
        tokens = line.split("")

with open("amazon-meta.txt", mode="r") as input:
    text = input.read()
    lines = text.splitlines()[3:] # remove first 3 file information lines
    lines = [line.strip() for line in lines] # deal with indentations
    print(read_product_from_index(lines, 0))
