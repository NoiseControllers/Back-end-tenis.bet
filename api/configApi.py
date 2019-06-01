from flask import Flask
from flask_restful import Api
from api.v1.tournament.Tournaments import TournamentsNext, TournamentsAtp, TournamentsWta


class ConfigApi(object):
    app = Flask(__name__)
    api = Api(app, "/v1")

    # API ROUTE TOURNAMENTS
    api.add_resource(TournamentsNext, '/tournaments/next')
    api.add_resource(TournamentsAtp, '/tournaments/atp')
    api.add_resource(TournamentsWta, '/tournaments/wta')
