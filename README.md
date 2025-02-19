# strava
Interacting with Strava's API

Update universal.py with identifying information.


```python
import urllib3
from strava_class import Strava
from universal import ATHLETE_ID


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sa = Strava(athlete_id=ATHLETE_ID)
sa.get_athlete()
```