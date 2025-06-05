import requests
import time
from datetime import datetime
import pytz

japan_tz = pytz.timezone('Asia/Tokyo')
kyushu_prefectures = ["福岡", "佐賀", "長崎", "熊本", "大分", "宮崎", "鹿児島", "沖縄"]
AFTER_DATE = int(japan_tz.localize(datetime(2025, 1, 1, 9)).timestamp())
BEFORE_DATE = int(japan_tz.localize(datetime(2025, 6, 1, 9)).timestamp())

def fetch_tournaments(token, page=1, per_page=25):
    query = f"""
    query {{
      tournaments(query: {{
        perPage: {per_page}
        page: {page}
        sortBy: "startAt desc"
        filter: {{
          videogameIds: [1386]
          afterDate: {AFTER_DATE}
          beforeDate: {BEFORE_DATE}
          countryCode: "JP"
        }}
      }}) {{
        nodes {{
          id
          name
          startAt
          city
          events {{
            name
            numEntrants
            standings(query: {{ perPage: 500 }}) {{
              nodes {{
                placement
                entrant {{ name }}
              }}
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        "https://api.start.gg/gql/alpha",
        json={"query": query},
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    return response.json()["data"]["tournaments"]["nodes"]

def fetch_all_tournaments(token):
    page = 1
    all_data = []
    while True:
        print(f"Fetching page {page}...")
        data = fetch_tournaments(token, page)
        if not data:
            break
        all_data.extend(data)
        if len(data) < 25:
            break
        page += 1
        time.sleep(1)
    return all_data

def filter_by_kyushu(tournaments):
    return [t for t in tournaments if t.get("city") and any(p in t["city"] for p in kyushu_prefectures)]
