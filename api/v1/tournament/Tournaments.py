from flask_restful import Resource
from tenisbet.db.Model.TournamentModel import TournamentModel

tournament_model = TournamentModel()


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
