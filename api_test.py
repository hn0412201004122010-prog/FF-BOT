import requests

url = "https://congdong.ff.garena.vn/league-score-api/player/find-match"

payload = {
    "accountId": "382563336",
    "startTime": 1781582400,
    "endTime": 1782115200
}

cookies = {
    "session": "765942ff-79d7-4837-b5aa-bda91ba049b4",
    "session.sig": "GFsaERJI2hfGAlAYSb9FTRwV_Qo"
}

r = requests.post(
    url,
    json=payload,
    cookies=cookies
)

print(r.status_code)
print(r.text)