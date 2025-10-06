import requests
from curl_cffi import Session,requests as curl_requests
from secrets import token_hex
from uuid import uuid4
import random , string
from fake_useragent import UserAgent
class Monitor:
    def __init__(self , username:str):
        self.username = username
        self.session = Session()
        self.ua = UserAgent()
        self.csrf = token_hex(22)
        self.UUID1 = str(uuid4())
        self.mid = self.generate_mid()
        self.session.headers.update(self.getHeader())
        self.session.cookies.update(self.getCookies())
    def generate_mid(self):
        first = ''.join(random.choices(string.ascii_letters + string.digits , k=3))
        secondpart = ''.join(random.choices(string.ascii_letters + string.digits , k=25))
        return first + '-' + secondpart
    def getHeader(self):
        headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.7',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': self.ua.random,
        'x-asbd-id': '359341',
        'x-csrftoken': self.csrf,
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': '0',
        'x-requested-with': 'XMLHttpRequest',
        'x-web-session-id': 'l2jhsk:umz2iv:bufkx2',
}
        return headers
    def getCookies(self):
        cookies = {
    'csrftoken': self.csrf,
    'datr': 'bf7jaG3N_ke0XCIXkFUreyZX',
    'ig_did': self.UUID1,
    'dpr': '1.5',
    'mid': self.mid,
    'wd': '725x557',
    'ig_nrcb': '1',
}
        return cookies


    def check2(self):
        data = {
            'email': 'vexekon769@aupvs.com',
            'failed_birthday_year_count': '{}',
            'first_name': '',
            'username': self.username,
            'opt_into_one_tap': 'false',
            'use_new_suggested_user_name': 'true',
            'jazoest': '22179',
        }

        response = self.session.post(
            'https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/',
            data=data,
            impersonate=random.choice(["chrome","firefox","edge","safari"]),
        )
        if 'username_is_taken' in response.text:
            return 'Banned'
        elif 'error_type' not in response.text:
            return 'Not Banned'
        else:
            return 'Unknown'
    def check(self):
        params = {
            'username': self.username,
        }

        response = self.session.get(
            'https://www.instagram.com/api/v1/users/web_profile_info/',
            params=params,
            impersonate=random.choice(["chrome","firefox","edge","safari"]),
        )
        if 'Page Not Found' in response.text or '<!DOCTYPE html>' in response.text:
            check = self.check2()
            if check == 'Banned':
                return {
                    "status" : "Banned",
                    "message" :"User Is Banned",
                }
            elif check == 'Not Banned':
                return {
                    "status" : "found",
                    "message" :"User Is Alive",
                }
            else:
                if self.username.startswith('.') or self.username.endswith('.') or self.username.isnumeric():
                    return {
                        "status" : "invalid",
                        "message" :"Invalid Username",
                    }
                return {
                    "status" : "unknown",
                    "message" : response.text[:200],
                }
        try:
            response.raise_for_status()
            if 'status' in response.json():
                if response.json()['status'] == 'ok' and response.text.__contains__('user'):
                    print(response.text)
                    return {
                        "status" : "found",
                        "message" :"User Is Alive",
                    }
                else:
                    return { 
                        "status" : "Banned",
                        "message" :"User Is Banned",
                    }
            else:
                return { 
                        "status" : "Banned",
                        "message" :"User Is Banned",
                    }
        except requests.exceptions.RequestException as e:
            return {
                "status" : "error",
                "message" : str(e)
            }
            
    def run(self):
        data = {
            'email_or_username': self.username,
            'jazoest': '22179',
        }

        response = self.session.post(
            'https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/',
            impersonate=random.choice(["chrome","firefox","edge","safari"]),
            data=data,
        )
        try:
            response.raise_for_status()
            if 'No users found' in response.text:
                return self.check()
            elif 'recovery_method' in response.text or response.json().get('status') == 'ok':
                return {
                    "status" : "found",
                    "message" :"User Is Alive",
                }
            else:
                return self.check()
        except requests.exceptions.RequestException as e:
            return {
                "status" : "error",
                "message" : str(e)
            }
if __name__ == "__main__":
    username = input("Enter Username : ")
    monitor = Monitor(username)
    result = monitor.run()
    print(result)
