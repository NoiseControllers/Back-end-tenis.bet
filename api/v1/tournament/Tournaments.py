from flask_restful import Resource

from tenisbet.db.data.TournamentRepository import TournamentRepository
from bson.json_util import dumps
tournament_model = TournamentRepository()


class Tournaments(Resource):
    def get(self):
        r = tournament_model.get_tournaments_with_match()
        return r, 200


class TournamentsCurrent(Resource):
    def get(self):
        # r = tournament_model.get_tournaments_by_ended(1)
        r = tournament_model.get_tournaments_with_match()
        return r, 200


class TournamentsNext(Resource):
    def get(self):
        r = tournament_model.upcoming_tournaments()
        return r


class TournamentsAtp(Resource):
    def get(self):
        r = tournament_model.get_tournaments_by_type('atp')

        if 0 == len(r):
            return {"message": "No se encontraron torneos disponibles"}, 404

        return r


class TournamentsWta(Resource):
    def get(self):
        r = tournament_model.get_tournaments_by_type('wta')
        return r


class TournamentSearch(Resource):
    def get(self, category, name, year):
        r = tournament_model.search_mathes_by_tournament(category, name, year)
        return r, 200
