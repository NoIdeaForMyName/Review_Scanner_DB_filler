from generators import *
from generators_settings import *

def main():
    print("Filling users...")
    users(USERS_NB)
    print("Users filled")

    print("Filling shops...")
    shops(SHOPS_NB)
    print("Shops filled")

    print("Filling products...")
    products(PRODUCTS_NB)
    print("Products filled")

    print("Filling scan history...")
    scan_histories(SCAN_HISTORY_NB)
    print("Scan history filled")

    print("Filling reviews...")
    reviews(REVIEWS_NB)
    print("Reviews filled")

    print("Filling reviews media...")
    reviews_media(REVIEWS_MEDIA_NB)
    print("Reviews media filled")


if __name__ == '__main__':
    main()
