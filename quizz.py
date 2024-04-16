import requests
from bs4 import BeautifulSoup

class PlayerDataScraper:
    def __init__(self, name):
        self.name = name
        self.url = f"https://en.wikipedia.org/wiki/{name}"
        self.data = []
        self.int_name = "International career"
        self.pers_name = "Personal information"
        self.men_name = "Managerial career"

    def scrape_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'infobox vcard'})
        
        if table is None:
            print(f"Table not found on the page for {self.name}.")
            return

        for row in table.find_all('tr')[1:]:
            columns = row.find_all(['th', 'td'])
            row_data = [column.get_text(strip=True) for column in columns]
            self.data.append(row_data)
        
        # Check for specific information to determine section names
        for row in self.data:
            if "Date of death" in row or "Place of death" in row:
                self.int_name = "International career"
                break
            else:
                self.int_name = "International career‡"

        for row in self.data:
            if self.men_name not in self.data:
                self.men_name = "Signature"
            else:
                self.men_name = self.men_name




    def write_to_personal_information(self):
        start_index = self.data.index([f"{self.pers_name}"])
        end_index = self.data.index(["Senior career*"])

        with open(f"{self.name}.txt", "w") as file:
            file.write("Personal information\n")
            for club in self.data[start_index + 1: end_index]:
                line = " -> ".join(club) + "\n"
                file.write(line)


    def write_to_senior_career(self):
        start_index = self.data.index(["Senior career*"])
        end_index = self.data.index([f"{self.int_name}"])

        with open(f"{self.name}.txt", "a") as file:
            file.write("\nSenior career\n")
            for club in self.data[start_index + 1:end_index-1]:
                line = " -> ".join(club) + "\n"
                file.write(line)

    def write_to_international_career(self):
        start_index = self.data.index([f"{self.int_name}"])
        end_index = self.data.index([f"{self.men_name}"])

        with open(f"{self.name}.txt", "a") as file:
            file.write("\nInternational career\n")
            for club in self.data[start_index  + 1: end_index ]:
                line = " -> ".join(club) + "\n"
                file.write(line)

    def write_to_managerial_career(self):
        start_index = self.data.index(["Managerial career"])
        end_index = self.data.index(["*Club domestic league appearances and goals"])

        with open(f"{self.name}.txt", "a") as file:
            file.write("\nManagerial career\n")
            for club in self.data[start_index:end_index - 2]:
                line = " -> ".join(club) + "\n"
                file.write(line)



    

    
def main():
    player_scraper = PlayerDataScraper('Cristiano Ronaldo')
    player_scraper.scrape_data()
    player_scraper.write_to_personal_information()
    player_scraper.write_to_senior_career()
    #player_scraper.write_to_international_career()
    #player_scraper.write_to_managerial_career()

if __name__ == "__main__":
    main()
