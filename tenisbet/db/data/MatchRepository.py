from bson import ObjectId

from tenisbet.db.MongoDB import MongoDB


class MatchRepository:
    def __init__(self):
        self.db = MongoDB.db
        self.matches = self.db.matches

    def inserts(self, matches):
        self.db.matches.insert_many(matches)

    def get_match_id(self, tournament_id):
        matches_id = []
        r = self.db.matches.find({"tournament_id": tournament_id}, {"_id": 0, "match_id": 1})

        for x in r:
            matches_id.append(x['match_id'])

        return matches_id

    def get_matches_not_started(self):
        matches = []
        query = {"match_result": {"$in": ["None", "IN PROGRESS"]}}
        r = self.db.matches.find(query)
        for x in r:
            matches.append(x)

        return matches

    def update_match(self, match_id, match_result):
        query = {"match_id": match_id}
        update = {"$set": {"match_result": match_result}}

        x = self.matches.update_one(query, update)

        return x.modified_count

    def get_matches_by_tournament_id(self, tournament_id):

        r = self.db.matches.find({"tournament_id": tournament_id}, {"_id": 0}).sort([("match_id", -1)]).limit(5)
        return r
