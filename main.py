from lib.crawl import BaicInfoSpider

# Path to your ChromeDriver
driver_path = "D:\\write_code_every_day\\nba-reference\\webdriver\\chromedriver.exe"
output_file = "basic_info.csv"

if __name__ == "__main__":
    spider = BaicInfoSpider()  # Create an instance of BaicInfoSpider
    spider.crawl_basic_info(driver_path, output_file)  # Call the method on the instance
    