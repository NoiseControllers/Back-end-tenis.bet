from tenisbet.db.MongoDB import MongoDB


class RankingModel:
    def __init__(self):
        self.db = MongoDB.db
        self.ranking = self.db.rankings

    def inserts(self, rankings):
        self.ranking.insert_one(rankings)

    def get_list_ranking(self):
        result = []
        r = self.ranking.find({}, {"_id": 0})
        for x in r:
            result.append(x)

        return result
