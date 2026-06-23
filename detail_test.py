import requests

match_id = "2068985323499370496"

url = "URL_DETAIL_API_CỦA_BẠN"

payload = {
"matchId": match_id
}

headers = {
"Content-Type": "application/json"
}

cookies = {
"session": "..."
}

r = requests.post(
url,
json=payload,
headers=headers,
cookies=cookies
)

print(r.json())
