import logging
import os
import pandas as pd
import requests
from datetime import datetime


def main():
	georgia_url = "https://www.georgiainsights.com/uploads/1/2/2/2/122221993/arp_esser_data_06162021.xlsx"
	response = requests.get(georgia_url)

	with open("test.xlsx", "wb") as file:
		file.write(response.content)
	
	excel_data = pd.read_excel("test.xlsx")
	excel_data.to_csv("GA_" + datetime.now().strftime("%m%d%Y") + ".csv", index=False)
	os.remove("test.xlsx")


if __name__ == "__main__":
	main()