import csv
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class BaicInfoSpider:

    def __init__(self) -> None:
        pass

    def setup_driver(self, driver_path):
        """
            Set up the WebDriver with desired options.
        """

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        service = Service(driver_path)
        return webdriver.Chrome(service=service, options=chrome_options)

    def fetch_player_data(self, driver, letter):
        """
            Fetch player data for a given letter from basketball-reference.
        """

        url = f'https://www.basketball-reference.com/players/{letter}/'
        driver.get(url)

        # Wait for dynamic content to load
        time.sleep(5)

        try:
            # Find the table element
            table_element = driver.find_element(By.ID, 'all_players')
            rows = table_element.find_elements(By.TAG_NAME, 'tr')

            # Extract data from each row
            player_data = []
            for row in rows:
                header_cells = row.find_elements(By.TAG_NAME, 'th')
                data_cells = row.find_elements(By.TAG_NAME, 'td')

                player = header_cells[0].text.strip() if header_cells else ""
                position = data_cells[2].text.strip() if len(
                    data_cells) > 0 else ""
                height = data_cells[3].text.strip() if len(
                    data_cells) > 1 else ""
                weight = data_cells[4].text.strip() if len(
                    data_cells) > 2 else ""

                if player and position and height and weight:
                    player_data.append([player, position, height, weight])
            return player_data
        except Exception as e:
            print(f"Error fetching data for letter {letter}: {e}")
            return []

    def write_to_csv(self, filename, data):
        """
            Write player data to a CSV file.
        """

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Player", "Pos", "Ht", "Wt"])  # Write header
            writer.writerows(data)

    def crawl_basic_info(self, driver_path, output_file):
        """
            Main function to scrape player data from basketball-reference.
        """

        driver = self.setup_driver(driver_path)
        all_player_data = []

        try:
            for letter in string.ascii_lowercase:
                print(f"Processing letter: {letter}")
                player_data = self.fetch_player_data(driver, letter)
                all_player_data.extend(player_data)
                print(f"Finished letter: {letter}")
        finally:
            driver.quit()

        # Write all data to CSV
        self.write_to_csv(output_file, all_player_data)
    