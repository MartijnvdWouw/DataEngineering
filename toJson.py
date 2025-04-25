
from typing import Tuple
import re
import json

RE_ID = r"Id:\s*(.*)(?=\n)"
RE_ASIN = r"ASIN:\s*(.*)(?=\n)"
RE_TITLE = r"title: (.*)(?=\n)"
RE_GROUP = r"\s+group: (.*)(?=\n)"
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
RE_CATEGORIES = r"categories: (\d*)"

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
REVIEW_DATE = "Review_date"
PRODUCT_DISCONTINUED = "Product_discontinued"

def get_reviews_from_product(text: str) -> list[dict[str, str]]:
    result = []
    for downloaded_review_match in re.finditer(RE_DOWNLOADED, text):
        char_pos = downloaded_review_match.start()
        line_num = text.count('\n', 0, char_pos)
        amount = int(downloaded_review_match.group(1))
        lines = text.splitlines()
        for i in range(line_num + 1, line_num + amount + 1):
            review = {
                REVIEW_RATING: re.findall(RE_RATING, lines[i]),
                REVIEW_VOTES: re.findall(RE_VOTES, lines[i]),
                REVIEW_HELPFUL: re.findall(RE_HELPFUL, lines[i]),
                REVIEW_CUSTOMER: re.findall(RE_CUSTOMER, lines[i]),
                REVIEW_DATE: re.findall(RE_DATE, lines[i]),
            }
            result.append({k:(v[0] if len(v) == 1 else v) for k, v in review.items() if not v is None and not v == []})
        break
    return result

def read_product_from_index(text: list[str], start_index: int) -> Tuple[dict, int]: # return dictionary of product and index of last line of product
    current_index = start_index
    product_text = []
    while not text[current_index] == "":
        product_text.append(text[current_index])
        current_index += 1
    product_text = "\n".join(product_text)
    categories = []
    for categories_match in re.finditer(RE_CATEGORIES, product_text):
        char_pos = categories_match.start()
        line_num = product_text.count('\n', 0, char_pos)
        amount = int(categories_match.group(1))
        categories = text[start_index + line_num + 1: start_index + line_num + amount + 1]
        break

    product = {
        PRODUCT_ID: re.findall(RE_ID, product_text),
        PRODUCT_ASIN: re.findall(RE_ASIN, product_text),
        PRODUCT_TITLE: re.findall(RE_TITLE, product_text),
        PRODUCT_GROUP: re.findall(RE_GROUP, product_text),
        PRODUCT_SALESRANK: re.findall(RE_SALESRANK, product_text),
        PRODUCT_SIMILAR: re.findall(RE_SIMILAR, product_text),
        PRODUCT_CATEGORIES: categories,
        PRODUCT_REVIEWS: get_reviews_from_product(product_text),
        PRODUCT_TOTAL_REVIEWS: re.findall(RE_TOTAL, product_text),
        PRODUCT_DOWNLOADED_REVIEWS: re.findall(RE_DOWNLOADED, product_text),
        PRODUCT_AVG_RATING: re.findall(RE_AVG_RATING, product_text),
        PRODUCT_DISCONTINUED: [not re.findall(RE_DISCONTINUED, product_text) == []],
    }

    return ({k:(v[0] if len(v) == 1 and not k == PRODUCT_REVIEWS and not k == PRODUCT_CATEGORIES else v) for k, v in product.items() if not v is None and not v == []}, current_index)

with open("amazon-meta.txt", mode="r") as input:
    text = input.read()
    lines = text.splitlines()[3:] # remove first 3 file information lines
    lines = [line.strip() for line in lines] # deal with indentations

index = 0
with open("result.jsonl", "a") as file:
    while index < len(lines):
        product, end_index = read_product_from_index(lines, index)
        file.write(f"{json.dumps(product)}\n")
        index = end_index + 1

        