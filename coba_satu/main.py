from creep import Scraper

if __name__ == "__main__":
    scraper = Scraper()

    datas = scraper.get_data()
    index = 1

    for data in datas:
        index += 1
