from datetime import datetime, date

from tenisbet.db.Model.MatchModel import MatchModel
from tenisbet.db.Model.TournamentModel import TournamentModel
from tenisbet.foretennis.ForeTennis import ForeTennis

match_model = MatchModel()
tournament_model = TournamentModel()
run = ForeTennis()


def _update_match():
    matches = match_model.get_matches_not_started()

    for match in matches:
        try:
            result, match_round = run.get_result_match(match['match_url'], match['tip'])
        except TypeError:
            continue

        if match_round == "FINAL" and result == "WIN" or match_round == "FINAL" and result == "LOSS":
            tournament_model.set_ended(match["tournament_id"], 2)

        match_model.update_match(match["match_id"], result)


def _tournaments_that_start():
    current_date = date.today()
    tournaments = tournament_model.get_tournaments_by_ended(0)

    for tournament in tournaments:
        start_date = datetime.strptime(tournament['start_date'], '%Y-%m-%d').date()

        if current_date == start_date:
            tournament_model.set_ended(tournament['_id'], 1)


def _search_news_matches():
    tournaments = tournament_model.get_tournaments_by_ended(1)

    for tournament in tournaments:
        run.get_matches(tournament['link'], tournament['_id'])
