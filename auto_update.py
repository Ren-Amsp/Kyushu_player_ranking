from modules.fetch import fetch_all_tournaments, filter_by_kyushu
from modules.points import calculate_player_points
from modules.export import export_csv, export_html

API_TOKEN = "e42465f39d2f9305a321e17732b39c10"
POINT_TABLE_PATH = "九州版JJPR_ポイント配分シート_参加賞対応版.xlsx"

def main():
    tournaments = fetch_all_tournaments(API_TOKEN)
    kyushu_tournaments = filter_by_kyushu(tournaments)
    ranking = calculate_player_points(kyushu_tournaments, POINT_TABLE_PATH)
    export_csv(ranking, "kyushu_player_ranking.csv")
    export_html(ranking, "kyushu_player_ranking.html")

if __name__ == "__main__":
    main()
