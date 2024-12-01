from lib.all_player_crawl import AllPlayerSpider
from lib.csv_combine import CombineCSV
import pymysql


# Path to your ChromeDriver
driver_path = "D:\\write_code_every_day\\NBA-reference\\webdriver\\chromedriver.exe"
basic_info_output = "D:\\write_code_every_day\\NBA-reference\\output\\basic_info.csv"
career_summary_output = "D:\\write_code_every_day\\NBA-reference\\output\\career_summary_a_to_z"

# Specify the directory of CSVs and the output file path
career_summary_all_csv = "D:\\write_code_every_day\\NBA-reference\\output\\career_summary_a_to_z"
career_summary_combined = "D:\\write_code_every_day\\NBA-reference\\output\\career_summary.csv"

if __name__ == "__main__":
    spider = AllPlayerSpider()

    # 這個大概5分鐘
    spider.crawl_basic_info(driver_path, basic_info_output)

    # 這個跑了一整晚
    spider.crawl_career_summary(driver_path, career_summary_output)

    # 最後合併
    combiner = CombineCSV(career_summary_all_csv, career_summary_combined)
    combiner.combine_career_summary()
