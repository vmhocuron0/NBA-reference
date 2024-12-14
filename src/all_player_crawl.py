import csv
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class AllPlayerSpider:

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

    def fetch_basic_info(self, driver, letter):
        """
        Fetch player data for a given letter from table under All NBA & ABA Players.
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
                
                # Check if the <strong> tag is present
                active = "no"
                if header_cells:
                    try:
                        strong_tag = header_cells[0].find_element(By.TAG_NAME, 'strong')
                        active = "yes"
                    except:
                        active = "no"

                position = data_cells[2].text.strip() if len(data_cells) > 2 else ""
                height = data_cells[3].text.strip() if len(data_cells) > 3 else ""
                weight = data_cells[4].text.strip() if len(data_cells) > 4 else ""

                if player and position and height and weight:
                    player_data.append([player, position, height, weight, active])
            return player_data
        except Exception as e:
            print(f"Error fetching data for letter {letter}: {e}")
            return []

    def basic_info_to_csv(self, file_path, data):
        """
        Write player data to a CSV file.
        """

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Player", "Pos", "Ht", "Wt", "Active"])  # Write header
            writer.writerows(data)

        print(f"Data saved to {file_path}")

    def crawl_basic_info(self, driver_path, output_path):
        """
        Main function to scrape player data from basketball-reference.
        """

        driver = self.setup_driver(driver_path)
        all_player_data = []

        try:
            for letter in string.ascii_lowercase:
                print(f"Processing letter: {letter}")
                player_data = self.fetch_basic_info(driver, letter)
                all_player_data.extend(player_data)
                print(f"Finished letter: {letter}")
        finally:
            driver.quit()

        # Write all data to CSV
        self.basic_info_to_csv(output_path, all_player_data)


    def fetch_career_summary(self, driver, url):
        """
        Fetch career stats (G, PTS, TRB, AST) for a player from their profile page.
        """

        try:
            driver.get(url)
            time.sleep(2)  # Wait for the page to load

            # Extract player's name (assuming it's in the page's header or title)
            player_name_element = driver.find_element(By.TAG_NAME, 'h1')
            player_name = player_name_element.text.strip()
            stats_pullout = driver.find_element(By.CLASS_NAME, "stats_pullout")
            stats = stats_pullout.find_elements(By.TAG_NAME, "div")

            # Extract required stats
            g = stats[3].find_elements(By.TAG_NAME, "p")[1].text.strip()
            pts = stats[4].find_elements(By.TAG_NAME, "p")[1].text.strip()
            trb = stats[5].find_elements(By.TAG_NAME, "p")[1].text.strip()
            ast = stats[6].find_elements(By.TAG_NAME, "p")[1].text.strip()

            # Include the player's name in the returned list
            return [player_name, g, pts, trb, ast]
        except Exception as e:
            print(f"Error fetching details from {url}: {e}")
            return None

    def fetch_player_url(self, driver, letter):
        """
        Fetch player links for a given letter from Player column.
        """

        url = f'https://www.basketball-reference.com/players/{letter}/'
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        try:
            # Find the table element
            table_element = driver.find_element(By.ID, 'players')
            rows = table_element.find_elements(By.TAG_NAME, 'tr')
            player_links = []
            for row in rows[1:]:
                header_cells = row.find_elements(By.TAG_NAME, 'th')
                if header_cells:
                    player_name = header_cells[0].text.strip()
                    if player_name != "Player":  # Ignore redundant headers
                        link_element = header_cells[0].find_element(
                            By.TAG_NAME, 'a')
                        player_link = link_element.get_attribute('href')
                        player_links.append(player_link)
            return player_links
        except Exception as e:
            print(f"Error fetching data for letter {letter}: {e}")
            return []

    def crawl_career_summary(self, driver_path, output_path):
        """
        Main function to scrape player stats from basketball-reference, saving results per letter.
        """

        driver = self.setup_driver(driver_path)

        try:
            # 要重跑某些字母 改這個 string.ascii_lowercase
            for letter in string.ascii_lowercase:
                print(f"Processing letter: {letter}")
                player_urls = self.fetch_player_url(driver, letter)
                player_data_each_letter = []

                for url in player_urls:
                    print(f"Fetching details for {url}")
                    player_data = self.fetch_career_summary(driver, url)
                    if player_data:
                        player_data_each_letter.append(player_data)

                # Write data for this letter to a separate CSV file
                output_file = f"{output_path}\\career_summary_{letter}.csv"
                self.career_summary_to_csv(
                    output_file, player_data_each_letter)

                print(
                    f"Finished letter: {letter}. Data saved to {output_file}")
        finally:
            driver.quit()

    def career_summary_to_csv(self, filename, data):
        """
        Write player data to a CSV file.
        """

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Player", "G", "PTS", "TRB", "AST"])
            writer.writerows(data)
