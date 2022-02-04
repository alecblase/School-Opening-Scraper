from tableauscraper import TableauScraper as TS
from datetime import datetime
import os
import logging
import requests
import pandas as pd

def main1():
    #logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)

    url="https://public.tableau.com/views/COVIDPlanningTool-Embed700px/SimpleDashboard?:embed=y&amp;:showVizHome=no&amp;:host_url=https%3A%2F%2Fpublic.tableau.com%2F&amp;:embed_code_version=3&amp;:tabs=no&amp;:toolbar=yes&amp;:animate_transition=yes&amp;:display_static_image=no&amp;:display_spinner=no&amp;:display_overlay=yes&amp;:display_count=yes&amp;:language=en&amp;publish=yes&amp;:loadOrderID=0"
    ts = TS()
    ts.loads(url)
    #logging.info("Received Hawaii Data", exc_info=False);

    ws = ts.getWorksheet("CDC Map")
    ws.data.to_csv("out/HI_" + datetime.now().strftime('%Y%m%d') + ".csv")
    #logging.info("Wrote Hawaii Data", exc_info=False);


def main():
    download_excel_file()
    ppe_cleaning_supplies()
    classroom_ventilation()
    social_distancing()
    device_gap()
    connectivity_gap()
    distance_learning()
    main1()
    os.remove("test.xlsx")    


# downloads excel file and all the sheets
def download_excel_file():
    download_url = "https://www.hawaiipublicschools.org/DOE%20Forms/BOE%20Metrics%20Q4_RAW_DATA_DOWNLOAD.xlsx?Web=1"
    response = requests.get(download_url)

    with open("test.xlsx", "wb") as file:
        file.write(response.content)


# https://stackoverflow.com/questions/17977540/pandas-looking-up-the-list-of-sheets-in-an-excel-file
# make code for specific sheets (each sheet is structured differently after all)
def pandas_test():
    xl = pd.ExcelFile('test.xlsx')
    print(xl.sheet_names)
    #xl = pd.read_excel('test.xlsx')
    #xl.keys()  # see all sheet names
    #print(xl.keys())


def ppe_cleaning_supplies():
    column_names = []
    excel_data = pd.read_excel("test.xlsx", sheet_name="Metric 1")

    dict1 = {}
    df = pd.DataFrame(columns=column_names)

    for i in range(0, len(excel_data["Complex Area"])):
        dict1[i] = {}

        # complex and school info
        dict1[i]["Complex Area"] = excel_data["Complex Area"].iloc[i]
        dict1[i]["Complex"] = excel_data["Complex"].iloc[i]
        dict1[i]["Pull Date"] = excel_data["Data Pull Date"].iloc[i]
        dict1[i]["School Name"] = excel_data["School Name"].iloc[i]
        dict1[i]["School Code"] = excel_data["School Code"].iloc[i]

        # ppe statistics
        dict1[i]["PPE Y or N"] = excel_data["PPE Y or N"].iloc[i]
        dict1[i]["PPE%"] = float(excel_data["PPE%"].iloc[i]) * 100
        dict1[i]["PPE Total"] = excel_data["PPE Total"].iloc[i]
        dict1[i]["PPE Denominator"] = excel_data["PPE Denominator"].iloc[i]
        dict1[i]["Needs Face Shields"] = excel_data["Needs Face Shields"].iloc[i]
        dict1[i]["Needs Gloves"] = excel_data["Needs Gloves"].iloc[i]
        dict1[i]["Needs Gowns"] = excel_data["Needs Gowns"].iloc[i]
        dict1[i]["Needs KN95"] = excel_data["Needs KN95"].iloc[i]
        dict1[i]["Needs Masks"] = excel_data["Needs Masks"].iloc[i]
        dict1[i]["Needs SSW"] = excel_data["Needs SSW"].iloc[i]


    for row in dict1:
        df = df.append(dict1[row], ignore_index=True)
    
    df.to_csv("out/hawaii_ppe_" + datetime.now().strftime('%Y%m%d') + ".csv", index=False)


# complex areas are disjointed
def classroom_ventilation():
    column_names = ["Complex Area", "Pull Date", "Total Classrooms", "Ventilated Classrooms", "Classrooms Lacking Ventilation"]
    excel_data = pd.read_excel("test.xlsx", sheet_name="Metric 3")

    dict1 = {}
    df = pd.DataFrame(columns=column_names)

    # loop through and combine complex areas
    for i in range(0, len(excel_data["Complex Area"])):
        dict1[i] = {}
                  
        dict1[i]["Complex Area"] = excel_data["Complex Area"].iloc[i]
        dict1[i]["Ventilated Classrooms"] = excel_data["M3 Ventilated Classrooms"].iloc[i]
        dict1[i]["Classrooms Lacking Ventilation"] = excel_data["M3 Ventilation Gap"].iloc[i]
        dict1[i]["Total Classrooms"] = excel_data["M3 Total Classrooms"].iloc[i]

    # append to pandas dataframe
    for row in dict1:
        df = df.append(dict1[row], ignore_index=True)
    
    df.to_csv("out/hawaii_ventilation_" + datetime.now().strftime('%Y%m%d') + ".csv", index=False)


# Can Accomodate 20-21 Enrollment (full time schedule)?
def social_distancing():
    column_names = []
    excel_data = pd.read_excel("test.xlsx", sheet_name="Metric 2")

    df = pd.DataFrame(columns=column_names)

    for i in range(0, len(excel_data["Complex Area"])):
        row = {"Complex Area": excel_data["Complex Area"].iloc[i], 
                "Complex": excel_data["Complex"].iloc[i], 
                "School Code": excel_data["School Code"].iloc[i], 
                "Name": excel_data["Name"].iloc[i], 
                "Pull Date": excel_data["Pull Date"].iloc[i], 
                "Can Accomodate Social Distancing?": excel_data["Can Accomodate 20-21 Enrollment (full time schedule)?"].iloc[i]}
        df = df.append(row, ignore_index=True)

    df.to_csv("out/hawaii_social_distancing_" + datetime.now().strftime('%Y%m%d') + ".csv", index=False)


def device_gap():
    column_names = []
    excel_data = pd.read_excel("test.xlsx", sheet_name="Metric 11")

    dict1 = {}
    df = pd.DataFrame(columns=column_names)

    # loop through and combine complex areas
    for i in range(0, len(excel_data["Complex Area"])):
        dict1[i] = {}

        dict1[i]["Complex Area"] = excel_data["Complex Area"].iloc[i]
        dict1[i]["Pull Date"] = excel_data["Pull Date"].iloc[i]
        dict1[i]["Number of Devices For Learning"] = excel_data["Metric 11 Enrl"].iloc[i]
        dict1[i]["Device Gap / Lacking"] = excel_data["Metric 11 Device Gap"].iloc[i]

    # append to pandas dataframe
    for row in dict1:
        df = df.append(dict1[row], ignore_index=True)

    df.to_csv("out/hawaii_device_gap_" + datetime.now().strftime('%Y%m%d') + ".csv", index=False)


def connectivity_gap():
    column_names = []
    excel_data = pd.read_excel("test.xlsx", sheet_name="Metric 12")
    print(excel_data.keys())

    dict1 = {}
    df = pd.DataFrame(columns=column_names)

    for i in range(0, len(excel_data["Complex Area"])):
        complex_area = excel_data["Complex Area"].iloc[i]

        if complex_area not in dict1:
            dict1[complex_area] = {}
            dict1[complex_area]["Number Devices"] = 0
            dict1[complex_area]["Device Gap"] = 0

        dict1[complex_area]["Complex Area"] = excel_data["Complex Area"].iloc[i]
        dict1[complex_area]["Pull Date"] = excel_data["Pull Date"].iloc[i]
        dict1[complex_area]["Number Devices"] += int(excel_data["Metric 12 Enrl"].iloc[i])
        dict1[complex_area]["Device Gap"] += int(excel_data["Internet Gap"].iloc[i])

    for row in dict1:
        df = df.append(dict1[row], ignore_index=True)

    df.to_csv("out/hawaii_connectivity_gap_" + datetime.now().strftime('%Y%m%d') + ".csv", index=False)


def distance_learning():
    column_names = []
    excel_data = pd.read_excel("test.xlsx", sheet_name="Metric 13")

    dict1 = {}
    df = pd.DataFrame(columns=column_names)

    for i in range(0, len(excel_data["Complex Area"])):
        complex_area = excel_data["Complex Area"].iloc[i]

        if complex_area not in dict1:
            dict1[complex_area] = {}
            dict1[complex_area]["# Schools That Can Support Distance Learning"] = 0
            dict1[complex_area]["# Schools That Cannot Support Distance Learning"] = 0

        dict1[complex_area]["Complex Area"] = excel_data["Complex Area"].iloc[i]
        dict1[complex_area]["Pull Date"] = excel_data["Pull Date"].iloc[i]
        if excel_data["Metric 13"].iloc[i] == "YES":
            dict1[complex_area]["# Schools That Can Support Distance Learning"] += 1
        else:
            dict1[complex_area]["# Schools That Cannot Support Distance Learning"] += 1

    for row in dict1:
        df = df.append(dict1[row], ignore_index=True)

    df.to_csv("out/hawaii_distance_learning_" + datetime.now().strftime('%Y%m%d') + ".csv", index=False)


# TODO: solve disjointed complex area values
if __name__ == "__main__":
    #pandas_test()
    #download_excel_file()
    #ppe_cleaning_supplies()
    #classroom_ventilation()
    #social_distancing()
    #device_gap()
    #connectivity_gap()
    #distance_learning()
    #main1()
    main()
    pass


# main()
