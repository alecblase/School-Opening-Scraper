import json
import logging
import urllib
import pandas as pd
import re
from datetime import date
from datetime import datetime

#benvin example
def main():
    #logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO);
    df = pd.DataFrame(
        columns=['school', 'alt name', 'address', 'instructional delivery', 'week of', 'total positive cases',
                 'date scraped'])
    url = "https://services7.arcgis.com/4RQmZZ0yaZkGR1zy/arcgis/rest/services/alsde_c19_publish_PUBLIC/FeatureServer/0/query?f=json&where=WeekOf%3D7&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=SchoolSystem%20asc&outSR=102100&resultOffset=0&resultRecordCount=200&resultType=standard&cacheHint=true"
    open_url = urllib.request.urlopen(url)
    json_data = json.loads(open_url.read())
    #logging.info("Received Alabama Data", exc_info=False);
    for p in json_data["features"]:
        school_system = p["attributes"]["SchoolSystem"]
        alt_name = p["attributes"]["AltName"]
        address = p["attributes"]["Address"]
        instructional_delivery = p["attributes"]["InstructionalDelivery"]
        week_of = p["attributes"]["WeekOf"]
        total_pos_lbl = p["attributes"]["TotalPositive_lbl"]
        new_row = pd.Series(data={'school': school_system, 'alt name': alt_name, 'address': address,
                                  'instructional delivery': instructional_delivery, 'week of': week_of,
                                  'total positive cases': total_pos_lbl, 'date scraped': date.today()})
        df = df.append(new_row, ignore_index=True)
    
    url2 = 'https://www.arcgis.com/sharing/rest/content/items/c6909b3820ae4047b0317fa00abc46fc/data'
    open_url2 = urllib.request.urlopen(url2)
    page_html = json.loads(open_url2.read())

    subtitle = page_html['headerPanel']['subtitle'].split("|")[1].strip()
    df["last_updated"] = re.search('([a-zA-Z]+) (\d+)', subtitle).group(0)

    df.to_csv('out/AL_' + datetime.now().strftime('%Y%m%d') + '.csv', index=False)
    #logging.info("Wrote Alabama Data", exc_info=False);

#main()
