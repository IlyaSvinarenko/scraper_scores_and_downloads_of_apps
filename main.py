from market_scraper import scrape_google_play_app_data
import sql_table

writer = sql_table.TableWriter()


def scrap_and_write():
    with open('test_domains.txt', 'r') as file:
        text = file.readlines()[1::]  # Первая строка в текстовом файле не будет учитываться
        for row in text:
            domain, url = row.strip().split('\t')
            average, reviews, download, latest_update = scrape_google_play_app_data(url)
            writer.add_record(average, reviews, download, latest_update, domain)


if __name__ == "__main__":
    scrap_and_write()
