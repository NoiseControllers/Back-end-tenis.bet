from bson import ObjectId

from tenisbet.db.Model import MatchModel
from tenisbet.db.MongoDB import MongoDB
from datetime import date, timedelta


class TournamentModel:
    def __init__(self):
        self.db = MongoDB.db
        self.tournaments = self.db.tournaments
        self.match_model = MatchModel.MatchModel()

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

    def get_tournaments_by_type(self, category_type):
        data = []
        query = {"category": category_type}
        r = self.tournaments.find(query, {"_id": 0, "category": 0, "link": 0})

        for x in r:
            data.append(x)

        return data

    def get_tournaments_with_match(self):
        result = []
        tournaments = self.get_tournaments_by_ended(1)

        for tournament in tournaments:
            x = []
            matches = self.match_model.get_matches_by_tournament_id(tournament['_id'])
            for match in matches:
                x.append(match)
            t = {"id": tournament['_id'], "category": tournament['category'], "name": tournament['name'],
                 "start_date": tournament['start_date'], "matches": x}
            result.append(t)

        return result

    # 0 = Proximamente, 1 = actualmente, 2 = Finalizado

    def get_tournaments_by_ended(self, ended_type):
        result = []
        query = [{"$match": {"ended": ended_type}}, {"$addFields": {"_id": {"$toString": "$_id"}}}]
        r = self.tournaments.aggregate(pipeline=query)
        for x in r:
            result.append(x)

        return result

    def set_ended(self, tournament_id, ended_type):
        query = {"_id": ObjectId(tournament_id)}
        update = {"$set": {"ended": ended_type}}

        x = self.tournaments.update_one(query, update)

        return x.modified_count
