import logging
import pandas as pd
import requests
from datetime import date
from datetime import datetime


# Arkansas offers 2 datasets we are interested in: co-ops (2 or more school districts) and individual schools
# can't find address to download excel file from


# Instruction choices: 0 is no value, 1 is onsite, 2 is virtual, 3 is hybrid, 4 is n/a
def collect_school_data():
	school_url = "https://insight.ade.arkansas.gov/api/ondemand/AR/instructionalOptions"
	response_data = requests.get(school_url)

	# holds all the school data
	all_school_data = []

	# school record records how many students are doing a particular learning modality
	indiv_school = {"lea": "", "onSite": 0, "virtual": 0, "hybrid": 0, "n/a": 0, "no value": 0}
	
	for school_info in response_data.json():
		# initialize the first entry (lea)
		if not indiv_school["lea"]:
			indiv_school["lea"] = school_info["lea"]
		
		# stop filling up dictionary if new lea shows up
		if school_info["lea"] != indiv_school["lea"]:
			all_school_data.append(indiv_school)
			indiv_school = {"lea": school_info["lea"], "onSite": 0, "virtual": 0, "hybrid": 0, "n/a": 0, "no value": 0}
		
		instruction_mode = school_info["instructionalChoice"]
		students_num = school_info["studentCount"]

		# determines which entry in response_data corresponds to which learning modality
		if instruction_mode == 0:
			indiv_school["no value"] += students_num
		elif instruction_mode == 1:
			indiv_school["onSite"] += students_num
		elif instruction_mode == 2:
			indiv_school["virtual"] += students_num
		elif instruction_mode == 3:
			indiv_school["hybrid"] += students_num
		elif instruction_mode == 4:
			indiv_school["n/a"] += students_num
	
	# ensures last lea entry is added since condition to add lea is if new lea / school appears in response_data
	all_school_data.append(indiv_school)
	
	schools_dataframe = pd.DataFrame(all_school_data)
	schools_dataframe.to_csv("out/AR_schools_" + datetime.now().strftime("%m%d%Y") + ".csv", index=False)


# group: 0 is no value, 1 is onsite, 2 is virtual, 3 is hybrid, 4 is n/a
# fiscalyear 32 = 2021, fiscalyear 31 = 2020
def collect_coop_data():
	coop_url = "https://insight.ade.arkansas.gov/api/ondemand/AR/metricSnapshots/instructionalOptions"
	response_data = requests.get(coop_url)

	# holds all data for the co-ops and the student learning modality counts
	all_coop_data = []
	indiv_coop = {"lea": "", "date": "", "onSite": 0, "virtual": 0, "hybrid": 0, "n/a": 0, "no value": 0}

	for coop_info in response_data.json():
		if not indiv_coop["lea"]:
			indiv_coop["lea"] = coop_info["lea"]
			indiv_coop["date"] = coop_info["snapshotDate"]
		
		# stop filling up dictionary if new lea shows up
		if coop_info["lea"] != indiv_coop["lea"]:
			all_coop_data.append(indiv_coop)
			indiv_coop = {"lea": coop_info["lea"], "date": coop_info["snapshotDate"], "onSite": 0, "virtual": 0, "hybrid": 0, "n/a": 0, "no value": 0}
		
		group = int(coop_info["group"])
		student_count = coop_info["studentCount"]

		if group == 0:
			indiv_coop["no value"] += student_count
		elif group == 1:
			indiv_coop["onSite"] += student_count
		elif group == 2:
			indiv_coop["virtual"] += student_count
		elif group == 3:
			indiv_coop["hybrid"] += student_count
		elif group == 4:
			indiv_coop["n/a"] += student_count
	
	all_coop_data.append(indiv_coop)

	coop_df = pd.DataFrame(all_coop_data) 
	coop_df.to_csv("out/AR_coop_" + datetime.now().strftime("%m%d%Y") + ".csv", index=False)


def main():
	collect_school_data()
	collect_coop_data()


if __name__ == "__main__":
	main()