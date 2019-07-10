import requests
from bs4 import BeautifulSoup
import re
from datetime import date, datetime

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
        self.current_date = date.today()
        self.match_model = MatchModel.MatchModel()
        self.rounds = ["R128", "R64", "R32", "R16", "QF", "SF", "FINAL"]

    def get_tournaments(self):

        for tournament in self.tournaments_list:

            r = requests.get(self.tournaments_list[tournament])
            dom = BeautifulSoup(r.content, "lxml")

            table = dom.find("table", {"id": "t01", "class": "preds"}).find_all("tr")

            for tr in table:
                if self.start is False:
                    self.start = True
                    continue

                ended = 0
                string_date = tr.select_one("td:nth-child(1)").text
                link = tr.select_one("td:nth-of-type(2)").find("a")["href"]
                name = tr.select_one("td:nth-of-type(2)").find("a").text
                start_date = datetime.strptime(string_date.replace('/', '-'), '%Y-%m-%d').date()
                pattern = name.lower().replace(" ", "")
                if start_date < self.current_date:
                    ended = 2

                data = {"start_date": str(start_date), "category": tournament, "link": link, "name": name,
                        "pattern": pattern, "ended": ended}
                self.tournaments.append(data)
            self.start = False

        tournament_model = TournamentModel()
        tournament_model.inserts(self.tournaments)

    @staticmethod
    def get_id_match(url_match):
        return re.findall(r"(?!.*/).+", url_match)[0]

    def get_matches(self, url_tournament, tournament_id):
        r = requests.get(url_tournament)
        dom = BeautifulSoup(r.content, "lxml")

        table = dom.find("table", {"class": "preds"}).find_all("tr")

        matches_id = self.match_model.get_match_id(tournament_id)

        for tr in table:
            if self.start is False:
                self.start = True
                continue
            try:
                match_round = tr.find("span", class_="largeOnly").text
                match_date = tr.find("div", class_="date_match").text
                match_url = tr.find("td", class_="lefted pnames").find("a")['href']
                match_id = self.get_id_match(match_url)
                p1 = tr.select_one("td:nth-of-type(2) > b > a > span:nth-of-type(1)").text
                p2 = tr.select_one("td:nth-of-type(2) > b > a > span:nth-of-type(2)").text
                prob = tr.select_one("td:nth-of-type(3)").text.strip() + "% - " + tr.select_one("td:nth-of-type(4)").text.strip() + "%"
                pred_set = tr.select_one("td:nth-of-type(6)").find_all("div")[0].text.strip() + " - " \
                           + tr.select_one("td:nth-of-type(6)").find_all("div")[1].text.strip()
                tip = tr.select_one("td:nth-of-type(5)").text.strip()
            except AttributeError:
                continue
            except IndexError:
                continue
            data = {"tournament_id": tournament_id, "match_id": match_id, "match_round": match_round,
                    "match_Date": match_date, "player1": p1, "player2": p2, "tip": tip, "match_url": match_url,
                    "prob": prob, "pred_set": pred_set, "match_result": "None"}

            if match_id not in matches_id and match_round in self.rounds:
                self.matches.append(data)

        if len(self.matches) > 0:
            self.match_model.inserts(self.matches)

    @staticmethod
    def get_result_match(match_url, tip):
        r = requests.get(match_url)
        dom = BeautifulSoup(r.content, "lxml")

        try:
            match_result = dom.select("td.centered.predict, span.predict_y, span.predict_n")
            match_round = dom.select("td.centered.tround")[0].text
        except IndexError:
            print(f"[DEBUG][IndexError] {match_url} ")
            pass

        try:
            if match_result[1]["class"][0] == "predict_y":
                if tip == int(match_result[0].text.strip()):
                    return "WIN", match_round
                return "LOSS", match_round
            elif match_result[1]["class"][0] == "predict_n":
                if tip == int(match_result[0].text.strip()):
                    return "LOSS", match_round
                return "WIN", match_round
            else:
                return "IN PROGRESS", match_round
        except IndexError:
            return "IN PROGRESS", match_round
