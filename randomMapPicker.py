import requests
from bs4 import BeautifulSoup as soup
import json
import os

class randomPicker:

    def __init__(self,setting):

        self.min_length = 120
        self.max_length = 300
        self.tb_min_length = 300
        self.tb_max_length = 420
        self.ar = (0.00,10.00)

        if setting == "gs" or setting == "group stage":

            self.nm_rate = (5.00,5.30)
            self.dt_rate = (3.50,3.80)
            self.tb_rate = (5.10,5.40)
            self.dt_ar = (0.00,8.00)

            self.message = "Group Stage settings applied"

        elif setting == "ro16" or setting == "round of 16":

            self.nm_rate = (5.30,5.50)
            self.dt_rate = (3.80,3.90)
            self.tb_rate = (5.40,5.60)
            self.dt_ar = (0.00,8.00)

            self.message = "Round of 16 settings applied"

        elif setting == "qf" or setting == "quarterfinals":

            self.nm_rate = (5.50,5.80)
            self.dt_rate = (3.90,4.10)
            self.tb_rate = (5.60,5.90)
            self.dt_ar = (0.00,8.50)

            self.message = "Quarterfinals settings applied"
        
        elif setting == "sf" or setting == "semifinals":

            self.nm_rate = (5.80,6.00)
            self.dt_rate = (4.10,4.20)
            self.tb_rate = (5.90,6.10)
            self.dt_ar = (0.00,8.50)

            self.message = "Semifinals settings applied"

        elif setting == "finals" or setting == "finals":

            self.nm_rate = (6.00,6.30)
            self.dt_rate = (4.20,4.30)
            self.tb_rate = (6.10,6.40)
            self.dt_ar = (0.00,9.00)

            self.message = "Finals settings applied"

        elif setting == "gf" or setting == "grand finals":
            
            self.nm_rate = (6.10,6.50)
            self.dt_rate = (4.20,4.50)
            self.tb_rate = (6.10,6.60)
            self.dt_ar = (0.00,9.00)

            self.message = "Grand Final settings applied"
            
        else:

            raise ValueError('Invalid Stage')
        

    def randomMapId(self,command):
    
        if command == "!f2":
            
            final_max_length = self.max_length
            final_min_length = self.min_length
            final_star_rate = self.nm_rate
            final_approach_rate = self.ar

        elif command == "dt":

            final_max_length = self.max_length
            final_min_length = self.min_length
            final_star_rate = self.dt_rate
            final_approach_rate = self.dt_ar

        elif command == "tb":

            final_max_length = self.tb_max_length
            final_min_length = self.tb_min_length
            final_star_rate = self.tb_rate
            final_approach_rate = self.ar

        else:
            raise ValueError('Invalid mod settings')

        url = f"https://osusearch.com/random/?statuses=Ranked&modes=Standard&min_length={final_min_length}&max_length={final_max_length}&star={final_star_rate}&ar={final_approach_rate}"
        r = requests.get(url).text
        html = soup(r,'html.parser')

        star_difficulty = html.tr.find_all('td')[3].text
        mapsetID = html.a.text

        api_key = os.environ['OSU_API_KEY'] 

        api_url = f"https://osu.ppy.sh/api/get_beatmaps?k={api_key}&s={mapsetID}"
        r = requests.get(api_url)
        difficulties = json.loads(r.text)

        for difficulty in difficulties:

            if str(difficulty["difficultyrating"])[0:5] == str(star_difficulty)[0:5]:
                return difficulty["beatmap_id"]
