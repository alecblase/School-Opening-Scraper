from _csv import reader
from bs4 import BeautifulSoup
import requests
import lxml
import csv
from datetime import date, datetime


def main():
    for school in ["hi"]:
        url = "https://wvde.us/covid19/schooloutbreaks/"
        page = requests.get(url)

        school_names = []
        school_cities = []
        last_updates = []
        cases = []

        school_names_close = []
        reason = []
        date_closed = []
        mask = []

        schoolinfo = {}  # (str_name, str_status)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'lxml')

            #school cases
            school_panel = soup.find(class_="row-hover")
            temp_school_names = school_panel.find_all(class_="column-1")
            temp_school_cities = school_panel.find_all(class_="column-2")
            temp_last_updates = school_panel.find_all(class_="column-3")
            temp_cases = school_panel.find_all(class_="column-4")
            for x in range(0, len(temp_school_names)):
                school_names.append(temp_school_names[x].get_text())
                school_cities.append(temp_school_cities[x].get_text())
                last_updates.append(temp_last_updates[x].get_text())
                cases.append(temp_cases[x].get_text())

            school_panel = soup.find_all(class_="row-hover")[1]
            temp_school_names_close = school_panel.find_all(class_="column-1")
            temp_reason = school_panel.find_all(class_="column-2")
            temp_date_closed = school_panel.find_all(class_="column-3")
            temp_mask = school_panel.find_all(class_="column-4")
            for x in range(0, len(temp_school_names_close)):
                school_names_close.append(temp_school_names_close[x].get_text())
                reason.append(temp_reason[x].get_text())
                date_closed.append(temp_date_closed[x].get_text())
                mask.append(temp_mask[x].get_text())


        csv_columns = ['School Name', 'School City', 'Update Date', 'Cases']

        with open("out/WV_" + datetime.now().strftime('%Y%m%d') + ".csv", 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(csv_columns)
            for x in range(0, len(school_names)):
               writer.writerow([school_names[x], school_cities[x], last_updates[x], cases[x]])
        csv_file.close()

        csv_columns = ['School Name', 'Reason', 'Closure Date', 'Mask Mandate']

        with open("out/WV_CLOSE_" + datetime.now().strftime('%Y%m%d') + ".csv", 'w') as csv_file:
            writer_two = csv.writer(csv_file)
            writer_two.writerow(csv_columns)
            for x in range(0, len(school_names_close)):
                writer_two.writerow([school_names_close[x], reason[x], date_closed[x], mask[x]])


main()
