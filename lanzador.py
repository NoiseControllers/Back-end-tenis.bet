from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from api.v1.tournament.Tournaments import TournamentsNext, TournamentsAtp, TournamentsWta, Tournaments, TournamentsCurrent, TournamentSearch
from api.v1.rankings.Rankings import Rankings


app = Flask(__name__)
api = Api(app, "/v1")
CORS(app)

# API ROUTE TOURNAMENTS
api.add_resource(Tournaments, '/tournaments/matches')
api.add_resource(TournamentsCurrent, '/tournaments/current')
api.add_resource(TournamentsNext, '/tournaments/next')
api.add_resource(TournamentsAtp, '/tournaments/atp')
api.add_resource(TournamentsWta, '/tournaments/wta')
api.add_resource(TournamentSearch, '/tournament/<string:category>/<string:name>/<int:year>')

# API RANKINGS
api.add_resource(Rankings, '/rankings')

app.run(debug=True)
