import requests
import csv
from datetime import datetime

# https://insights.nd.gov/Education/MapSearch
# srch parameter based on glossary
# need to create time to get updated list
# "%Y%m%d%H%M%S"
def main():
	current_timestamp = datetime.now().strftime("%Y%m%d")
	district_url = f"https://insights.nd.gov/CsvHandler.ashx?csv=K12BrowseDistricts&s=undefined&d=undefined&ver={current_timestamp}&srch=ABCDEFGHIJKLMNOPQRSTUVWXYZ"

	response = requests.get(district_url)
	district_line_info = response.text.split("\r\n")
	header = True

	with open("out/ND_" + datetime.now().strftime("%m%d%Y") + ".csv", "w", newline="") as file:
		district_writer = csv.writer(file, delimiter=",")
		for line in district_line_info:
			columns = line.split(",")

			if header:
				header = False
			else:
				columns[-1] = columns[-1] + "%"

			district_writer.writerow(columns)


if __name__ == "__main__":
	main()
