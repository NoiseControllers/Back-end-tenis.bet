from tenisbet.db.Model import MatchModel
from tenisbet.db.Model.TournamentModel import TournamentModel
from tenisbet.foretennis.ForeTennis import ForeTennis
from tenisbet.utils.cron import _search_news_matches, _update_match, _tournaments_that_start


def main():
    run = ForeTennis()
    # run.get_tournaments()
    run.get_matches("https://www.foretennis.com/tournament/atp/rolandgarros/2019", None)
    # result_win = run.get_result_match("https://www.foretennis.com/matches/atp/auger-paire/160217", 1)

    # match_model = MatchModel.MatchModel()
    # r = match_model.get_match_id()
    #
    # for x in r:
    #     print(x)
    #     if x['match_id'] in '1602414':
    #         print("ENCONTRADO")
    #         return

    # tournament_model = TournamentModel()
    #
    # tournament_model.upcoming_tournaments()

    # _update_match()
    # _search_news_matches()
    # _update_match()
    _tournaments_that_start()

    # matches_id = match_model.get_match_id("5cfbcb873db9d040090e6e30")


if __name__ == '__main__':
    main()
