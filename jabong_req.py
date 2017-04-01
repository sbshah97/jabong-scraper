from bs4 import BeautifulSoup
import requests
import re
import sys
import csv
import time

count = 0
process = 0
start_time = time.time()

with open('jabong.csv', 'w') as csvfile:
    jabongwriter = csv.writer(csvfile, delimiter=',')
    jabongwriter.writerow(['ID', 'Title', 'Original Price', 'Discounted Price', 'URL'])
    csvfile.flush()
    for i in range(1,300):
        r = requests.get('http://www.jabong.com/men/clothing/polos-tshirts/?sort=popularity&dir=desc&source=topnav_men&page='+str(i))
        data = r.text
        soup = BeautifulSoup(data, "lxml")

        items = soup.find_all("section", class_="row search-product animate-products")

        products = soup.find_all("div", class_="product-info")
        link = "http://www.jabong.com/men/clothing/polos-tshirts/"

        process_start = time.time()
        
        for product in products:

            title = product.find('div', class_='h4')
#     id        print title.text
            title_list = title.text
            title_list = unicode(title_list).encode('utf-8')

            price = product.find('div', class_="price")
            parent = price.find_all('span')
            standard_price = product.find_all('span', class_='standard-price')
            mrp_price = ""
            discounted_price = "" 
            if len(standard_price) != 0:
#                 print standard_price[0].string
				mrp_price = standard_price[0].string
				mrp_price = unicode(mrp_price).encode('utf-8')
				if len(standard_price) == 2:
#                     print standard_price[1].string
					discounted_price = standard_price[1].string
					discounted_price = unicode(discounted_price).encode('utf-8')
				else:
				#                     print "None"
				    discounted_price = standard_price[0].string
				    discounted_price = unicode(discounted_price).encode('utf-8')
				count += 1		

#             print(link + str(product.parent.get('href')))
				url_link = link + str(product.parent.get('href'))
				url_link = unicode(url_link).encode('utf-8')
				# print("count = " + str(count))

				id_item = product.parent.parent.get('data-product-id')
				id_item = unicode(id_item).encode('utf-8')
#             print(str(id_item))
            
				if id_item == None:
				    continue
				else:
				    jabongwriter.writerow([id_item, title_list, mrp_price, discounted_price, url_link])
				    csvfile.flush()

				process_end = time.time()

				if count == 10000:
				    end_time = time.time()
				    print end_time-start_time
				    sys.exit(0)

		process += process_end - process_start
        print("Process time:" + str(process_end - process_start))

end_time = time.time()
print("Total of " + str(count) + "items taken")
print("Process Time is: " + str(process))
print("Total time is: " + str(end_time-start_time))