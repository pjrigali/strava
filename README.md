# strava
Interacting with Strava's API


```python
import urllib3
import configparser
from strava_class import Strava

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
config = configparser.ConfigParser()

CLIENT_ID = config["STRAVA"]["STRAVA_CLIENT_ID"]
CLIENT_SECRET = config["STRAVA"]["STRAVA_CLIENT_SECRET"]
REFRESH = config["STRAVA"]["STRAVA_REFRESH"]
ATHLETE_ID = int(config["STRAVA"]["STRAVA_ATHLETE_ID"])

sa = Strava(athlete_id=ATHLETE_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, refresh_token=REFRESH)
sa.get_athlete()
```