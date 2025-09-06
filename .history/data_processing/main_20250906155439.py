from crawler import collect_complaints
from utils import *


if __name__ == "__main__":
    # path to your chromedriver executable
    chromedriver_path = "C:/Users/Lior Lerner/Downloads/chromedriver-win64/chromedriver.exe"
    # path to save the Excel file
    excel_path = "mercado_livre_complaints.xlsx"
    collect_complaints("mercado-livre", excel_path, chromedriver_path)