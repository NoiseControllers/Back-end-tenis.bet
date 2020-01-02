from flask_restful import Resource
from tenisbet.db.data.RankingRepository import RankingRepository
ranking_model = RankingRepository()


class Rankings(Resource):
    def get(self):
        r = ranking_model.get_list_ranking()
        return r