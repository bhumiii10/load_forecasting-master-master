import requests
import csv
import os
from bs4 import BeautifulSoup
url = 'https://www.wunderground.com/history/airport/VIDP/%d/%d/%d/DailyHistory.html'

day_range = list(range(1, 32)) # days, 1 to 31

# months, Aug to Dec for 2017, and Jan for 2018
month_range = {
				2022: list(range(8, 13)),
				2023: [1]
				}

year_range = [2022, 2023]

if not os.path.exists('Whether_Data'):
	    os.makedirs('Whether_Data')



for year in year_range:
	for month in month_range[year]:
		month_dir = 'Whether_Data/%d/%02d/' %(year, month)
		if not os.path.exists(month_dir): os.makedirs(month_dir)
		# ... (previous code)

		for day in day_range:
			try:
				date = '%02d/%02d/%d' % (day, month, year)
				print('Scraping', date)
				current_url = url % (year, month, day)
				resp = requests.get(current_url)
				soup = BeautifulSoup(resp.text, 'lxml')

				table = soup.find('table', {'id': 'obsTable'})

				if table:
					trs = table.find_all('tr')

					if len(trs[1:]) != 0:
						csv_filename = month_dir + '%s.csv' % date.replace('/', '-')

						if os.path.exists(csv_filename):
							os.remove(csv_filename)

						with open(csv_filename, 'a') as f:
							writer = csv.writer(f)
							columns = [th.text for th in trs[0].find_all('th')]
							writer.writerow(columns)

							for tr in trs[1:]:
								row = []
								tds = tr.find_all('td')

								for td in tds:
									span = td.find_all('span', {'class': 'wx-value'})

									if span:
										row.append(span[0].text.strip())
									else:
										row.append(td.text.strip())

								assert len(row) == len(columns)
								writer.writerow(row)
			except Exception as e:
				print('Exception', e)
				print(date)
				print(current_url)
