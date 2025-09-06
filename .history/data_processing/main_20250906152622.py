from crawler import collect_complaints
from utils import *


if __name__ == "__main__":
        #path to your chromedriver.exe
        chromedriver_path = "C:/Users/Lior Lerner/Downloads/chromedriver-win64/chromedriver.exe"
        #path to save the excel file
        excel_path = "santander_complaints.xlsx"

        collect_complaints("santander", excel_path, chromedriver_path)