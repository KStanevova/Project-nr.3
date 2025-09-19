# Elections Scraper (PS 2017)

Scraper of the 2017 Czech parliamentary election results from the website volby.cz.
It downloads results for all municipalities within the selected administrative district (okres) and saves them to a CSV file.

Autor: Kateřina Stanevová
E‑mail: KStanevova@seznam.cz

## Requirements
First, create a virtual environment using the following command:
```bash
python -m venv .venv
```

Then activate this environment:
`
. .venv/bin/activate   # Windows: .venv\\Scripts\\activate
`

This project requires several third-party libraries. The steps below describe how to install them and generate the requirements.txt file:
```bash
# first update pip to latest version
python -m pip install --upgrade pip

# then install all dependencies
pip install requests urllib3 beautifulsoup4

# then generate requirements.txt
pip freeze > requirements.txt

# You can later use this file to install dependencies in another environment using
pip install -r requirements.txt

```

---

## Input parameters
- \- l / --link => url address for scraping
- \- o / --output => name of the output file (with .csv extension)
- \--help => help info with usage and program parameters

Run the script:
```bash
python main.py -l "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" -o test.csv
```

For help:
```
python main.py --help
```
![alt text](./scr/usage.png)

---

## 1. step - Get links
function `get_links`

As the first step, the script scrapes data from the first page (url from parameter 1) and get following information:
1. village code
2. village name
3. link for votes and other elections data

This information is scraped for all towns in the particular district and stored in the list of dictionaries.

![alt text](./scr/get_links.png)

---

## 2. step - Get votes and other elections data
function `get_votes`

This function expects town dictionary data as input (code, name and link), get this link and scrape additional data (votes, issued_envelopes, valid_votes) for this town.

![alt text](./scr/get_votes.png)

---

## 3. step - Export to csv
function `export`

This function expects output file name and result data as list of dictionaries save it as CSV with headers.

![alt text](./scr/export.png)

---
