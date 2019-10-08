import requests

url ="https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1592023&showMyProfs=true"
headers = {
                "authority": "www.ratemyprofessors.com",
                "method": "GET",
                "path": "/ShowRatings.jsp?tid=2183841&showMyProfs=true",
                "scheme": "https",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9",
                "cache-control": "no-cache",
                "cookie": "notice=true; previousSchoolID=1232; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22187ba890-4e49-4ce9-8467-58604bfa0f58%22; _ga=GA1.2.1090600566.1570246267; _gid=GA1.2.478891723.1570246267; promotionIndex=0; ad_blocker_overlay_2019=true; trc_cookie_storage=taboola%2520global%253Auser-id%3D7b913cb6-22a0-4cda-b540-adecfc61f9ad-tuct429455b; showTeacherPopout=true",
                "pragma": "no-cache",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"            }
response = requests.get(url, headers=headers)
print(response.text)
