"""
main.py: třetí projekt do Engeto Online Python Akademie

author:  Kateřina Stanevová
email:   KStanevova@seznam.cz
"""

import sys
import requests
import urllib3
from urllib.parse import urljoin
import argparse
from bs4 import BeautifulSoup as bs
import json
import csv


# Some sites block default Python requests so add headers to mimic a browser !!!
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def parser():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Scrape HTML page and save parsed data to CSV",
        usage="python %(prog)s -l <URL> -o <CSVFILE>"
    )

    # First positional argument: HTML link
    parser.add_argument("-l", "--link", dest="url", required=True, help="Input HTML link")

    # Second positional argument: Output CSV filename
    parser.add_argument("-o", "--output", dest="output", required=True, help="Output CSV file (e.g., filename.csv)")

    args = parser.parse_args()
    print(f"URL: {args.url}")
    print(f"Output file: {args.output}")
    return args

def get_links(url):
    """Get basic info from url (code, name, link) 
        for all towns in the district.

    Args:
        url (_type_): district link

    Returns:
        _type_: list of dictionaries (code, name, link)
    """
    links = []
    response = requests.get(url, headers=headers, verify=False)

    # Parse HTML
    soup = bs(response.text, "html.parser")

    # Get table data
    table = soup.find("table")
    rows = table.find_all("tr")
    
    for row in rows:
        item = []
        for col in row.find_all("td"):
            item.append(col.get_text(strip=True))            
            if col.get("class") and "cislo" in col.get("class"):
                link = col.find("a")
                item.append(urljoin(url, link["href"]))
            else:
                item.append("")
        if item:
            links.append({"code": item[0], "name": item[2], "link": item[1]})
    return links
    
def get_votes(item:dict):    
    """ Get extended info for each town (votes, envelopes, etc.)

    Args:
        item (dict): extended dictionary with more election data
    """
    data = item
    response = requests.get(item["link"], headers=headers, verify=False)
    
    # Parse HTML
    soup = bs(response.text, "html.parser")

    cols = soup.find_all("td")
        
    for col in cols:
        # Get "votes_in_list"
        if (col.get("class") == ["cislo"] and col.get("headers") == ["sa2"] and col.get("data-rel") == "L1"):
            data["votes_in_list"] = int(col.get_text(strip=True).replace("\xa0", ""))
        # Get "issued_envelopes"
        elif (col.get("class") == ["cislo"] and  col.get("headers") == ["sa3"] and col.get("data-rel") == "L1"):
            data["issued_envelopes"] = int(col.get_text(strip=True).replace("\xa0", ""))
        # Get "valid_votes"
        elif (col.get("class") == ["cislo"] and  col.get("headers") == ["sa6"] and col.get("data-rel") == "L1"):
            data["valid_votes"] = int(col.get_text(strip=True).replace("\xa0", ""))
    
    # Get candidates
    candidates = soup.find("div", class_="t2_470").find("table")    
    for row in candidates.find_all("tr"):
        cols = row.find_all("td")
        name, votes = None, None
        for col in cols:
            if (col.get("class") == ["overflow_name"] and  col.get("headers") == ["t1sa1","t1sb2"]):
                name = col.get_text(strip=True)
            
            if (col.get("class") == ["cislo"] and  col.get("headers") == ["t1sa2","t1sb3"]):
                votes = int(col.get_text(strip=True).replace("\xa0", ""))

            if name and votes:
                data[name] = votes
    # print(json.dumps(data, ensure_ascii=False, indent=4))        
    return(data)        
        
def export(file_name:str, dict_data:list):
    """ Write list of dicts to .csv file

    Args:
        file_name (str): name of the file in format "filename.csv"
        dict_data (list): data as list of dictionaries
    """
    with open(file_name, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=dict_data[0].keys())
        writer.writeheader()
        writer.writerows(dict_data)
    
def main():
    urllib3.disable_warnings() # Disable warnings
    
    args = parser() # Parse arguments

    links = get_links(args.url) # Get villages
    
    # ------------------------------------------------
    results = []
    for link in links:
        results.append(get_votes(link))

    # Export to .csv file
    export(args.output, results)
    
if __name__ == "__main__":
    main()