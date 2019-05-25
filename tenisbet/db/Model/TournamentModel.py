from tenisbet.db.MongoDB import MongoDB
from datetime import date, timedelta


class TournamentModel:
    def __init__(self):
        self.db = MongoDB.db
        self.tournaments = self.db.tournaments

    def inserts(self, tournaments):
        self.tournaments.insert_many(tournaments)

    def upcoming_tournaments(self):
        current_date = date.today().isoformat()
        after_date = (date.today()+timedelta(days=15)).isoformat()

        query = {"start_date": {"$gte": current_date, "$lte": after_date}}
        r = self.tournaments.find(query)

        for x in r:
            print(x)
