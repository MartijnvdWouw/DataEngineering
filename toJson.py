
from typing import Tuple

TOKEN_MAP = {
    "Id:": "Product_id",
    "ASIN:": "Product_ASIN",
    "title:": "Product_title",
    "group:": "Product_group",
    "salesrank:": "Product_salesrank",
    "similar:": "Similar_products",
    "cutomer:": "Customer",
    "categories:": "Product_categories",
    "reviews:": "Product_reviews",
    "rating:": "Review_rating",
    "votes:" : "Review_votes",
    "helpful:": "Review_votes_helpful",
    "discontinued product": "Product_discontinued",
}

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
