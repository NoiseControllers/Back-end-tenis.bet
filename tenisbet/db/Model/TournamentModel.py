from tenisbet.db.MongoDB import MongoDB
from datetime import date, timedelta


class TournamentModel:
    def __init__(self):
        self.db = MongoDB.db
        self.tournaments = self.db.tournaments

    def inserts(self, tournaments):
        self.tournaments.insert_many(tournaments)

    def upcoming_tournaments(self):
        data = []
        current_date = date.today().isoformat()
        after_date = (date.today()+timedelta(days=15)).isoformat()

        query = [{"$match": {"$or": [{"start_date": {"$gte": current_date, "$lte": after_date}}]}},
                 {"$addFields": {"_id": {"$toString": "$_id"}}}]

        r = self.tournaments.aggregate(pipeline=query)

        for x in r:
            data.append(x)
        return data

    def get_tournaments_by_type(self, type):
        data = []
        query = {"category": type}
        r = self.tournaments.find(query, {"_id": 0, "category": 0, "link": 0})

        for x in r:
            data.append(x)

        return data
