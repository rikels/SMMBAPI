<H1>SMMBAPI</H1>
<H2>Hosted API</H2>
I use OpenShift (By RedHat) and Flask (Python library) to create a hosted version for you to use without Python.<br />
<b>/api/course/<ID>	[GET]</b><br />
Example: http://smmbapi-rikels.rhcloud.com/api/course/A917-0000-00E3-0C15<br />
Returns: A JSON list with all the extracted information of the given course.<br />
<b>/api/course/recommended	[GET]</b><br />
Example: http://smmbapi-rikels.rhcloud.com/api/course/recommended<br />
Returns: A JSON list with 10 random Super Mario Maker courses.<br />
<br />
<b>/api/course/ranked	[GET] (Optional parameters: type,pagenum)</b><br />
Valid types:total_liked_count,weekly_liked_count,like_rate<br />
Valid pagenums:1-10<br />
Example: http://smmbapi-rikels.rhcloud.com/api/course/ranked?pagenum=2&type=total_liked_count<br />
Returns: A JSON list with 10 most liked courses from that page (page 1 is 1-10, page 2 is 11-20).<br />
<br />
<b>/api/makers/ranked	[GET] (Optional parameters: type,pagenum)</b><br />
Valid types:total_liked_count,weekly_liked_count<br />
Valid pagenums:1-5<br />
Example: http://smmbapi-rikels.rhcloud.com/api/makers/ranked?pagenum=2&type=total_liked_count<br />
Returns: A JSON list with 10 most liked makers from that page (page 1 is 1-10, page 2 is 11-20).<br />

The result will be JSON. It's a good practice to always check the statuscode 200 is good, the rest is not ;)<br />
<H2>Python API</H2>
This python script scrapes the info from courses via https://supermariomakerbookmark.nintendo.net it looks them up by ID.
<H2>How to use</H2>
Open a terminal and go to the directory you placed the script in. Open up Python and import smmbapi.<br />
In Python just run a command like this smmbapi.smmbapi(ID)<br />
<b>Example:</b> smmbapi.smmbapi("A917-0000-00E3-0C15")<br />
This will return a dictionary with all the information retrieved from the site. <br />
If the given ID isn't correct, the script will only return 404 (Not found).<br />
Here's a simple tree structure:<br />
```
Results
├── ID (String)
├── Header
│   ├── HeaderColor (String)
│	│	returned by Nintendo, mostly returned: "blue","pink","green"
│   ├── Rank (Int)
│	│	It's mostly not used, only when you request the Ranked page
│   ├── Difficulty(String)
│	│	Returned by Nintendo, depends on your country...
│	│	english: "Super Expert","Expert","Normal","Easy"
│	│	Dutch: "Supermoeilijk","Moeilijk","Normaal","Makkelijk"
│   ├── ClearRate(string, could make it a float...)
│
│
├── Body (main info of the course)
│	│
│	│
│   ├── CourseTitle (String)
│   ├── CourseImage (String,url)
│   ├── CourseStyle (String)
│	│	returns "SMB1", "SMB3", "SMW", "NSMBU"
│   ├── CreatedAt (String)
│   ├── CourseTag (String)
│   ├── Likes (Int)
│   ├── Plays (Int)
│   ├── Shared (Int)
│   ├── Tries (String)
│   ├── CourseFullImage (String, url)
│   ├── CreatorMiiImage (String, url)
│   ├── CreatorCountry (String, 2 letters)
│	│	Like: NL,DE,US
│   ├── CreatorMedals (String)
│	│	Like: "icon_coin0" till "icon_coin10" maybe more?
│   ├── CreatorName (String)
│
│
├── Records (Can also return empty, when none returned)
│	│
│	│
│   ├── RecordMiiImage (String,url)
│   ├── RecordCountry (String, 2 letters)
│   ├── RecordName (String)
│   ├── RecordTime (String)
│   ├── FirstMiiImage (String, url)
│   ├── FirstCountry (String, 2 letters)
│   ├── FirstName (String)
│
│
├── RecentPlayers (list with more dictionaries, as much as people returned)
│	│
│	│
│   ├── UserName (String)
│   ├── UserCountry (String, 2 letters)
│   ├── UserMii (String, url)
│
│
├── ClearedBy(list with more dictionaries, as much as people returned)
│	│
│	│
│   ├── UserName (String)
│   ├── UserCountry (String)
│   ├── UserMii (String, url)
│
│
├── LikedBy(list with more dictionaries, as much as people returned)
│	│
│	│
│   ├── UserName (String)
│   ├── UserCountry (String)
│   ├── UserMii (String, url)
│
│
├── Status
│	│
│	│
│   ├── StatusCode (Int,200,400 or 404)
│   ├── StatusExplantaion (String, tried to give the most accurate information)
```