import requests

cookies = {
    "session": "765942ff-79d7-4837-b5aa-bda91ba049b4",
    "session.sig": "GFsaERJI2hfGAlAYSb9FTRwV_Qo"
}

headers = {
    "Content-Type": "application/json",
    "Referer": "https://congdong.ff.garena.vn/tinh-diem",
    "Origin": "https://congdong.ff.garena.vn"
}

uid = input("Nhập UID: ")

payload = {
    "accountId": uid,
    "startTime": 1781582400,
    "endTime": 1782115200
}

url = "https://congdong.ff.garena.vn/league-score-api/player/find-match"

r = requests.post(
    url,
    json=payload,
    headers=headers,
    cookies=cookies
)

data = r.json()

print("\n===== DANH SÁCH TRẬN =====")

for match in data["matches"]:
    print(match["id"])