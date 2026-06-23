import json
import os
import requests
from datetime import datetime, timedelta

selected_uid = None
selected_time = None

time_slots = {
    "1": "13h - 15h",
    "2": "15h - 17h",
    "3": "17h - 19h",
    "4": "20h - 21h30",
    "5": "21h40 - 23h",
    "6": "23h30 - 1h",
    "7": "1h - 3h",
    "8": "10h - 12h"
}

cookies = {
    "session": "765942ff-79d7-4837-b5aa-bda91ba049b4",
    "session.sig": "GFsaERJI2hfGAlAYSb9FTRwV_Qo"
}

if os.path.exists("data.json"):
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {
        "uid": None,
        "time": None
    }

print("=" * 40)
print("🏆 BOT TÍNH ĐIỂM FREE FIRE")
print("=" * 40)
print("Gõ .td UID để bắt đầu")

while True:

    command = input("\nNhập lệnh: ").strip()

    if command == ".exit":
        print("👋 Tạm biệt")
        break

    elif command.startswith(".td"):

        parts = command.split()

        if len(parts) != 2:
            print("Ví dụ: .td 382563336")
            continue

        selected_uid = parts[1]

        print(f"\nUID đã chọn: {selected_uid}")

        print("""
1. 13h - 15h
2. 15h - 17h
3. 17h - 19h
4. 20h - 21h30
5. 21h40 - 23h
6. 23h30 - 1h
7. 1h - 3h
8. 10h - 12h
""")

    elif command in time_slots:

        if selected_uid is None:
            print("❌ Hãy nhập .td UID trước")
            continue

        selected_time = time_slots[command]

        data["uid"] = selected_uid
        data["time"] = selected_time

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

        today = datetime.now()

        year = today.year
        month = today.month
        day = today.day

        if command == "1":
            start_time = int(datetime(year, month, day, 13, 0, 0).timestamp())
            end_time = int(datetime(year, month, day, 15, 0, 0).timestamp())

        elif command == "2":
            start_time = int(datetime(year, month, day, 15, 0, 0).timestamp())
            end_time = int(datetime(year, month, day, 17, 0, 0).timestamp())

        elif command == "3":
            start_time = int(datetime(year, month, day, 17, 0, 0).timestamp())
            end_time = int(datetime(year, month, day, 19, 0, 0).timestamp())

        elif command == "4":
            start_time = int(datetime(year, month, day, 20, 0, 0).timestamp())
            end_time = int(datetime(year, month, day, 21, 30, 0).timestamp())

        elif command == "5":
            start_time = int(datetime(year, month, day, 21, 40, 0).timestamp())
            end_time = int(datetime(year, month, day, 23, 0, 0).timestamp())

        elif command == "6":
            start_time = int(datetime(year, month, day, 23, 30, 0).timestamp())

            tomorrow = today + timedelta(days=1)

            end_time = int(
                datetime(
                    tomorrow.year,
                    tomorrow.month,
                    tomorrow.day,
                    1,
                    0,
                    0
                ).timestamp()
            )

        elif command == "7":
            start_time = int(datetime(year, month, day, 1, 0, 0).timestamp())
            end_time = int(datetime(year, month, day, 3, 0, 0).timestamp())

        elif command == "8":
            start_time = int(datetime(year, month, day, 10, 0, 0).timestamp())
            end_time = int(datetime(year, month, day, 12, 0, 0).timestamp())

        print("\n====================")
        print("🎮 UID:", selected_uid)
        print("🕒 Khung giờ:", selected_time)
        print("====================")

        url = "https://congdong.ff.garena.vn/league-score-api/player/find-match"

        payload = {
            "accountId": selected_uid,
            "startTime": start_time,
            "endTime": end_time
        }

        print("\nPayload gửi lên:")
        print(payload)

        headers = {
            "Content-Type": "application/json",
            "Referer": "https://congdong.ff.garena.vn/tinh-diem",
            "Origin": "https://congdong.ff.garena.vn"
        }

        try:

            r = requests.post(
                url,
                json=payload,
                headers=headers,
                cookies=cookies
            )

            print("\nStatus:", r.status_code)

            if r.status_code != 200:
                print("❌ Không lấy được dữ liệu")
                print(r.text)
                continue

            result = r.json()

            matches = result.get("matches", [])

            print(
                f"\n✅ Tìm thấy {len(matches)} trận trong khung giờ này\n"
            )
            teams = {}
            for i, match in enumerate(matches, start=1):

                print("\n====================")
                print(f"🎮 Trận {i}")

                print(json.dumps(match, ensure_ascii=False, indent=4))

                match_id = match["id"]

                detail_url = "https://congdong.ff.garena.vn/league-score-api/match"

                detail_payload = {
                    "matchId": match_id
                }

                print("\nPayload detail:")
                print(detail_payload)

                detail_response = requests.post(
                    detail_url,
                    json=detail_payload,
                    headers=headers,
                    cookies=cookies
                )

                print("Status detail:", detail_response.status_code)

                if detail_response.status_code != 200:
                    print(detail_response.text)
                    continue

                detail_data = detail_response.json()
                ranks = detail_data["match"]["ranks"]

                for rank_data in ranks:

                    team_name = rank_data["accountNames"][0]

                    kills = rank_data["kill"]

                    rank = rank_data["rank"]

                    rank_points = {
                        1: 12,
                        2: 9,
                        3: 8,
                        4: 7,
                        5: 6,
                        6: 5,
                        7: 4,
                        8: 3,
                        9: 2,
                        10: 1
                    }

                    score = rank_points.get(rank, 0) + kills

                    if team_name not in teams:
                        teams[team_name] = {
                            "kills": 0,
                            "points": 0,
                            "matches": 0
                        }

                    teams[team_name]["kills"] += kills
                    teams[team_name]["points"] += score
                    teams[team_name]["matches"] += 1
                    print("\n")
                    print("=" * 70)
                    print("🏆 BẢNG XẾP HẠNG TỔNG")
                    print("=" * 70)

                    sorted_teams = sorted(
                        teams.items(),
                        key=lambda x: x[1]["points"],
                        reverse=True
                    )

                    for stt, (team_name, info) in enumerate(sorted_teams, start=1):

                        print(
                            f"{stt:>2}. "
                            f"{team_name:<20} | "
                            f"Trận: {info['matches']:<2} | "
                            f"Kill: {info['kills']:<3} | "
                            f"Điểm: {info['points']}"
                        )

        except Exception as e:
            print("❌ Lỗi:", e)
            
    elif command == ".info":

        print(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=4
            )
        )

    elif command == ".reset":

        data = {
            "uid": None,
            "time": None
        }

        with open(
            "data.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

        print("✅ Đã reset dữ liệu")

    else:
        print("❌ Lệnh không hợp lệ")
