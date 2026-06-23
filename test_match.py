import requests

match_id = "2069073908323923968"

url = "https://congdong.ff.garena.vn/league-score-api/match/detail"

payload = {
"matchId": match_id
}

headers = {
"Content-Type": "application/json",
"Referer": "https://congdong.ff.garena.vn/tinh-diem",
"Origin": "https://congdong.ff.garena.vn"
}

cookies = {
"session": "765942ff-79d7-4837-b5aa-bda91ba049b4",
"session.sig": "GFsaERJI2hfGAlAYSb9FTRwV_Qo"
}

r = requests.post(
url,
json=payload,
headers=headers,
cookies=cookies
)

print("Status:", r.status_code)
print(r.text)
