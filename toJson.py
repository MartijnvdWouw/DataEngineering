
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
RE_RATING = r"(?<!avg )rating:\s*(\d*)"
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

def read_product_from_index(text: list[str], start_index: int) -> Tuple[dict, int]: # return dictionary of product and index of last line of product
    current_index = start_index
    product_text = []
    while not text[current_index] == "":
        product_text.append(text[current_index])
        current_index += 1
    product_text = "\n".join(product_text)
    product = {
        PRODUCT_ID: re.findall(RE_ID, product_text),
        PRODUCT_ASIN: re.findall(RE_ASIN, product_text),
        PRODUCT_TITLE: re.findall(RE_TITLE, product_text),
        PRODUCT_GROUP: re.findall(RE_GROUP, product_text),
        PRODUCT_SALESRANK: re.findall(RE_SALESRANK, product_text),
        PRODUCT_SIMILAR: re.findall(RE_SIMILAR, product_text),
        REVIEW_CUSTOMER: re.findall(RE_CUSTOMER, product_text),
        # PRODUCT_CATEGORIES = "Product_categories"
        # PRODUCT_REVIEWS = "Product_reviews"
        PRODUCT_TOTAL_REVIEWS: re.findall(RE_TOTAL, product_text),
        PRODUCT_DOWNLOADED_REVIEWS: re.findall(RE_DOWNLOADED, product_text),
        PRODUCT_AVG_RATING: re.findall(RE_AVG_RATING, product_text),
        REVIEW_RATING: re.findall(RE_RATING, product_text),
        REVIEW_VOTES: re.findall(RE_VOTES, product_text),
        REVIEW_HELPFUL: re.findall(RE_HELPFUL, product_text),
        PRODUCT_DISCONTINUED: [not re.findall(RE_DISCONTINUED, product_text) == []],

    }


    return {k:(v[0] if len(v) == 1 else v) for k, v in product.items() if not v is None and not v == []}

with open("amazon-meta.txt", mode="r") as input:
    text = input.read()
    lines = text.splitlines()[3:] # remove first 3 file information lines
    lines = [line.strip() for line in lines] # deal with indentations
    print(read_product_from_index(lines, 0))
    print(read_product_from_index(lines, 4))