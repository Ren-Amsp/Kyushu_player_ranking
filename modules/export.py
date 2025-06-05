import csv

def export_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "points", "history"])
        writer.writeheader()
        writer.writerows(data)

def export_html(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>Kyushu Smash Ultimate Ranking</title>
  <link rel="stylesheet" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css">
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
  <style>
    body { font-family: sans-serif; padding: 20px; }
    table { width: 100%; }
    pre { white-space: pre-wrap; }
  </style>
</head>
<body>
  <h1>Kyushu Player Ranking</h1>
  <table id="ranking">
    <thead>
      <tr><th>順位</th><th>プレイヤー</th><th>ポイント</th><th>順位履歴</th></tr>
    </thead>
    <tbody>
""")
        for i, row in enumerate(data, 1):
            f.write(f"<tr><td>{i}</td><td>{row['name']}</td><td>{row['points']}</td><td><pre>{row['history']}</pre></td></tr>\n")
        f.write("""</tbody>
  </table>
  <script>
    $(document).ready(function () {
      $('#ranking').DataTable({
        language: {
          search: "検索:",
          lengthMenu: "表示 _MENU_ 件",
          info: "_TOTAL_ 件中 _START_ から _END_ を表示",
          paginate: { next: "次", previous: "前" }
        }
      });
    });
  </script>
</body>
</html>""")
