from flask_restful import Resource
from tenisbet.db.data.RankingRepository import RankingModel
ranking_model = RankingModel()


class Rankings(Resource):
    def get(self):
        r = ranking_model.get_list_ranking()
        return r