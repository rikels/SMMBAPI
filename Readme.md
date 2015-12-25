<H1>SMMBAPI</H1>
This python script scrapes the info from courses via https://supermariomakerbookmark.nintendo.net it looks them up by ID.
<H2>How to use</H2>
Open a terminal and go to the directory you placed the script in. Open up Python and import smmbapi.<br />
In Python just run a command like this smmbapi.smmbapi(ID)<br />
<b>Example:</b> smmbapi.smmbapi("A917-0000-00E3-0C15")<br />
This will return a dictionary with all the information retrieved from the site. Here's a simple tree structure:<br />
```
Results
├── Header
│   ├── HeaderColor (String)
│	│	returned by Nintendo, mostly returned: "blue","pink","green"
│   ├── RankNonprize (String)
│	│	something random, not seen on the site. at the moment it also doesn't realy work, returns to much :)
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
├── Records
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
```