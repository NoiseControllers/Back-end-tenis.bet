from datetime import date
import requests
from bs4 import BeautifulSoup
from tenisbet.db.data import RankingRepository


class Ranking:
    def __init__(self):
        self.ranking_model = RankingRepository.RankingModel()
        self.list_ranking = {"ATP": "http://www.tennis.com/rankings/ATP/", "WTA": "http://www.tennis.com/rankings/WTA/"}
        self.current_date = date.today()
        self.ranking_atp = []
        self.ranking_wta = []
        self.temp_status = None

    def execute(self):
        for x in self.list_ranking:
            self.temp_status = x
            r = requests.get(self.list_ranking[x])
            dom = BeautifulSoup(r.content, "lxml")

            table = dom.find("table", {"id": "atpRanking"}).find("tbody").findAll("tr")

            for tr in table:
                x = {
                    "current_rank": tr.find("td", class_="current-rank").text,
                    "prev_rank": tr.find("td", class_="prev-rank").text,
                    "player_name": tr.find("td", class_="player-name").text.strip(),
                    "player_points": tr.find("td", class_="player-points").text
                }

                if self.temp_status == "ATP":
                    self.ranking_atp.append(x)
                elif self.temp_status == "WTA":
                    self.ranking_wta.append(x)

        output = {"record_date": str(self.current_date), "ATP": self.ranking_atp,
                  "WTA": self.ranking_wta}
        self.ranking_model.inserts(output)
