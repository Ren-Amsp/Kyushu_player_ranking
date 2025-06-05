import openpyxl

def get_rank(num_entrants):
    if num_entrants >= 256:
        return 'P'
    elif num_entrants >= 128:
        return 'S'
    elif num_entrants >= 96:
        return 'A+'
    elif num_entrants >= 64:
        return 'A'
    elif num_entrants >= 40:
        return 'B'
    elif num_entrants >= 24:
        return 'C'
    elif num_entrants >= 16:
        return 'D'
    return None

def load_points_table(filepath):
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active

    point_table = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        rank, placement, point = row
        if not rank:
            continue
        if rank not in point_table:
            point_table[rank] = {}
        point_table[rank][int(placement)] = float(point)
    return point_table

def calculate_player_points(tournaments, point_file):
    point_table = load_points_table(point_file)
    players = {}

    for t in tournaments:
        for event in t.get("events", []):
            num = event.get("numEntrants", 0)
            rank = get_rank(num)
            if not rank:
                continue

            for standing in event["standings"]["nodes"]:
                name = standing["entrant"]["name"]
                placement = standing["placement"]
                pts = point_table.get(rank, {}).get(placement, point_table.get(rank, {}).get("参加賞", 0))

                if name not in players:
                    players[name] = {"total": 0, "history": []}

                players[name]["total"] += pts
                players[name]["history"].append(f"{t['name']}（{placement}位：{pts}pt）")

    return sorted(
        [{"name": k, "points": round(v['total'], 2), "history": "\n".join(v['history'])} for k, v in players.items()],
        key=lambda x: x["points"],
        reverse=True
    )
