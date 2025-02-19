import json
import requests
from dataclasses import dataclass
from universal import CLIENT_ID, CLIENT_SECRET, REFRESH, BASE_URL, ACTIVITY_UPDATES


def _get_header() -> dict:
    payload = {'client_id': CLIENT_ID,
               'client_secret': CLIENT_SECRET,
               'refresh_token': REFRESH,
               'grant_type': "refresh_token",
               'f': 'json'}
    r = requests.post(f"{BASE_URL}oauth/token", data=payload, verify=False)
    
    if r.status_code == 200:
        return {'Authorization': f"Bearer {r.json().get('access_token')}", 'Content-Type': 'application/json'}
    else:
        raise ValueError(f"Request ({str(r.request).split('[')[1].split(']')[0]}) was not successful.")


@dataclass
class Strava:
    
    def __init__(self, athlete_id: int) -> None:
        self.athlete_id = athlete_id
        self.headers = _get_header()


    def get_athlete(self) -> dict:
        r = requests.get(f"{BASE_URL}api/v3/athlete", headers=self.headers)
        
        if r.status_code == 200:
            return r.json()
        else:
            raise ValueError(f"Request ({str(r.request).split('[')[1].split(']')[0]}) was not successful.")


    def get_athlete_stats(self, ath_id: int = None) -> dict:
        if not ath_id:
            ath_id = self.athlete_id  
        r = requests.get(f"{BASE_URL}api/v3/athletes/{ath_id}/stats", headers=self.headers)
        
        if r.status_code == 200:
            return r.json()
        else:
            raise ValueError(f"Request ({str(r.request).split('[')[1].split(']')[0]}) was not successful.")


    def get_athlete_routes(self, ath_id: int = None) -> list:
        if not ath_id:
            ath_id = self.athlete_id
            
        page, lst = 1, []
        while True:
            r = requests.get(f"{BASE_URL}api/v3/athletes/{ath_id}/routes", headers=self.headers, params={'per_page': 50, 'page': page})
            if r.status_code == 200:
                r = r.json()
                page += 1
                if r:
                    lst.extend(r)
                    if len(r) < 50:
                        break
            else:
                raise ValueError(f"Request ({str(r.request).split('[')[1].split(']')[0]}) was not successful.")
        return lst


    def get_activities(self) -> list:
        page, lst = 1, []
        while True:
            r = requests.get(f"{BASE_URL}api/v3/athlete/activities", headers=self.headers, params={'per_page': 200, 'page': page})
            if r.status_code == 200:
                r = r.json()
                page += 1
                if r:
                    lst.extend(r)
                    if len(r) < 200:
                        break
            else:
                raise ValueError(f"Request ({str(r.request).split('[')[1].split(']')[0]}) was not successful.")
        return lst
    
    
    def get_activity_details(self, act_id: int) -> dict:
        r = requests.get(f"{BASE_URL}api/v3/activities/{act_id}?include_all_efforts=True", headers=self.headers)
        
        if r.status_code == 200:
            return r.json()
        else:
            raise ValueError(f"Request ({str(r.request).split('[')[1].split(']')[0]}) was not successful.")


    def update_activity(self, act_id: int, data: dict) -> dict:
        dct = {}
        for k, v in data.items():
            if ACTIVITY_UPDATES.get(k) and isinstance(v, ACTIVITY_UPDATES.get(k)):
                dct[k] = v
            else:
                raise KeyError(f"({k}) is either not in ({str(ACTIVITY_UPDATES.keys())}) or the value is not the correct data type.")
        
        r = requests.put(f"{BASE_URL}api/v3/activities/{act_id}", data=json.dumps(dct), headers=self.headers)
        
        if r.status_code == 200:
            return r.json()
        else:
            raise ValueError(f"Request ({str(r.request).split('[')[1].split(']')[0]}) was not successful.")
