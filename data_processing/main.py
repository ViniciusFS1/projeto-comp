from crawler import collect_complaints
from utils import *


if __name__ == "__main__":
    # path to your chromedriver executable
    chromedriver_path = ""
    # path to save the Excel file
    excel_path = "santander_complaints.xlsx"
    target_company = "santander"
    collect_complaints(target_company, excel_path, chromedriver_path,pages=2)