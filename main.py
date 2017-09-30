import requests, csv
from bs4 import BeautifulSoup

stores_to_pull = [
    'venice-grind-los-angeles',
    'accomplice-bar-los-angeles',
    'little-fatty-los-angeles',
    'tattoo-lounge-mar-vista',
    'timewarp-records-los-angeles',
    'floyds-99-barbershop-los-angeles-3',
    'grand-view-market-los-angeles-2',
    'vintage-on-venice-los-angeles'
]

url = "https://www.yelp.com/biz/{}?sort_by=date_desc"
url_to_go = url


output_csv = open("YelpScraped.csv", 'w', newline = '')
csv_writer = csv.writer(output_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
csv_writer.writerow(['Shop', 'Address', 'Reviewer', 'Date', 'Rating'])

for store in stores_to_pull:
    page = requests.get(url.format(store))
    soup = BeautifulSoup(page.content, 'html.parser')

    header = soup.find(class_='biz-page-header')
    num_reviews = header.find(class_='review-count').get_text()
    num_reviews = num_reviews.strip()
    num_reviews = int(num_reviews[0:num_reviews.find(' ')].strip())
    num_pages = int(num_reviews / 20) + 1

    shop_name = header.find('h1', class_= 'biz-page-title').get_text()
    shop_address = soup.find('address').get_text()
    shop_name = shop_name.strip()
    shop_address = shop_address.strip().replace('Los Angeles', ' Los Angeles')

    print('Pulling {} reviews for {} across {} pages...'.format(num_reviews, shop_name, num_pages))

    pg_num = 1
    for pg_num in range(1, num_pages + 1):
        print('Page {}...'.format(pg_num))
        if pg_num > 1:
            url_to_go = url.format(store) + '&start={}'.format((pg_num - 1) * 20)
            page = requests.get(url_to_go)
            soup = BeautifulSoup(page.content, 'html.parser')

        review_list = soup.find_all(class_= 'review-list')[0]
        reviews = review_list.find_all(class_= 'review--with-sidebar')

        for review in reviews:
            if not 'war-widget--compose' in review['class']:
                username = review.find(class_ = 'user-display-name').get_text()
                date = review.find(class_ = 'rating-qualifier').get_text()
                rating = review.find(class_ = 'i-stars')['title']

                username = username.strip()
                date = date.strip()
                rating = rating.strip()

                if date.find('Updated review') > -1:
                    date = date[0:10].strip()

                csv_writer.writerow([shop_name, shop_address, username, date, rating])

print('Finished scraping reviews.')
