from tenisbet.foretennis.ForeTennis import ForeTennis
from tenisbet.tenniscom.Ranking import Ranking
from tenisbet.utils.cron import _search_news_matches, _update_match, _tournaments_that_start
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--searchMatches', action='store_true')
    parser.add_argument('--searchTournament', action='store_true')
    parser.add_argument('--tournamentActive', action='store_true')
    parser.add_argument('--updateResultMatch', action='store_true')
    parser.add_argument('--rankings', action='store_true')
    args = parser.parse_args()

    if args.searchMatches:
        _search_news_matches()

    elif args.searchTournament:
        run = ForeTennis()
        run.get_tournaments()

    elif args.tournamentActive:
        _tournaments_that_start()

    elif args.updateResultMatch:
        _update_match()

    elif args.rankings:
        run = Ranking()
        run.execute()


if __name__ == '__main__':
    main()
