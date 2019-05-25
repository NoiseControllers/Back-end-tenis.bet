from tenisbet.db.MongoDB import MongoDB


class MatchModel:
    def __init__(self):
        self.db = MongoDB.db
        self.matches = self.db.matches

    def inserts(self, matches):
        self.db.matches.insert_many(matches)

    def get_match_id(self):
        matches_id = []
        r = self.db.matches.find({}, {"_id": 0, "match_id": 1})

        for x in r:
            matches_id.append(x)

        return matches_id
