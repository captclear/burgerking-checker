from math import fabs
from unittest import result
import requests
import json
import re

# captcha api config on https://www.clearcaptcha.com 
clearcaptcha_recaptcha_api="http://api.clearcaptcha.com/captcha/recaptcha_enterprise_v2v3";
token = 'd7897e0ac82d47909af94a4a9b30test'
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

session = requests.Session()

headers={
        "Host": "bk.wgiftcard.com",
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Connection": "keep-alive",
    }

response = session.get("https://bk.wgiftcard.com/responsive/personalize_responsive/chooseDesign/burgerking/1",headers=headers,verify=False)

response = session.get("https://bk.wgiftcard.com/responsive/personalize_responsive/reload/burgerking",headers=headers,verify=False)
result_text=response.text
if "RELOAD YOUR BK CROWN CARD - Step 1" in result_text:
    site_key = re.search(r'data-sitekey="(.*?)"', result_text).group(1)
    post_data =  {
        "token": token,
        "sitekey": site_key,
        "referer":"https://bk.wgiftcard.com/responsive/personalize_responsive/reload/burgerking",
        "recaptcha_anchor_size":"normal",
        "page_title":"Burger King | eGift Card | Reload Card",
     }
    response = requests.post(clearcaptcha_recaptcha_api, data=post_data)
    response_data = response.json()
    recaptcha_token=response_data["data"]["recaptcha_token"]
    
    post_data =  {
        "action": "verify",
        "gc_number": "6006491584438400343",
        "g-recaptcha-response":recaptcha_token,
    }
    headers["Content-Type"]="application/x-www-form-urlencoded"
    response = session.post("https://bk.wgiftcard.com/responsive/personalize_responsive/reload/burgerking", data=post_data,headers=headers,verify=False)
    result_text=response.text
    if "currently has a balance" in result_text:
        balance = re.search(r'currently has a balance of (.*?)\.', result_text).group(1);
        print(f"balance:{balance}")
    elif "Please check your gift card number" in result_text:
         print("Invalid Number")
    else:
        response_data={
            "error": "api error",
            "status_code": response.status_code,
        }
else:
    print(f"The page for entering the card number is wrongly loaded")

