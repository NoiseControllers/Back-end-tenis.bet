import requests
from bs4 import BeautifulSoup
import re

from tenisbet.db.Model import MatchModel
from tenisbet.db.Model.TournamentModel import TournamentModel


class ForeTennis:
    def __init__(self):
        self.base_url = "https://www.foretennis.com/"
        self.tournaments_list = {
            "atp": "https://www.foretennis.com/tournaments/atp/2019",
            "wta": "https://www.foretennis.com/tournaments/wta/2019"
        }
        self.start = False
        self.tournaments = []
        self.matches = []

    def get_tournaments(self):

        for tournament in self.tournaments_list:

            r = requests.get(self.tournaments_list[tournament])
            dom = BeautifulSoup(r.content, "lxml")

            table = dom.find("table", {"id": "t01", "class": "preds"}).find_all("tr")

            for tr in table:
                if self.start is False:
                    self.start = True
                    continue
                date = tr.select_one("td:nth-child(1)").text
                link = tr.select_one("td:nth-child(2)").find("a")["href"]
                name = tr.select_one("td:nth-child(2)").find("a").text

                data = {"start_date": date.replace('/', '-'), "category": tournament, "link": link, "tournament": name}
                self.tournaments.append(data)
            self.start = False

        tournament_model = TournamentModel()
        tournament_model.inserts(self.tournaments)

    @staticmethod
    def get_id_match(url_match):
        return re.findall(r"(?!.*/).+", url_match)[0]

    def get_matches(self, url_tournament):
        r = requests.get(url_tournament)
        dom = BeautifulSoup(r.content, "lxml")

        table = dom.find("table", {"class": "preds"}).find_all("tr")

        for tr in table:
            if self.start is False:
                self.start = True
                continue
            try:
                match_round = tr.find("span", class_="largeOnly").text
                match_date = tr.find("div", class_="date_match").text
                match_url = tr.find("td", class_="lefted pnames").find("a")['href']
                match_id = self.get_id_match(match_url)
                p1 = tr.select_one("td:nth-child(2) > b > a > span:nth-child(1)").text
                p2 = tr.select_one("td:nth-child(2) > b > a > span:nth-child(3)").text
                tip = tr.select_one("td:nth-child(5)").text.strip()
            except AttributeError:
                continue

            data = {"tournament_id": "", "match_id": match_id, "match_round": match_round, "match_Date": match_date,
                    "player1": p1, "player2": p2, "tip": tip, "match_url": match_url, "match_result": ""}
            self.matches.append(data)

        if len(self.matches) > 0:
            match_model = MatchModel.MatchModel()
            match_model.inserts(self.matches)

    @staticmethod
    def get_result_match(match_url, tip):
        r = requests.get(match_url)
        dom = BeautifulSoup(r.content, "lxml")

        match_result = dom.select("td.centered.predict, span.predict_y, span.predict_n")
        try:
            if match_result[1]["class"][0] == "predict_y":
                if tip == int(match_result[0].text.strip()):
                    return "WIN"
                return "LOSS"
            elif match_result[1]["class"][0] == "predict_n":
                if tip == int(match_result[0].text.strip()):
                    return "LOSS"
                return "WIN"
            else:
                return "IN PROGRESS"
        except IndexError:
            return "IN PROGRESS"
