try:
	import requests
except:
	SystemExit("can\'t find reuqests, please install it via \"pip install requests\"")

try:
	from BeautifulSoup import BeautifulSoup
except:
	try:
		from bs4 import BeautifulSoup
	except:
		SystemExit("can\'t find BeautifulSoup, please install it via \"pip install BeautifulSoup\"")

import re

IDRegex = "([0-9a-fA-F]{4})(?: ?[\-_ ]? ?)?([0-9a-fA-F]{4})(?: ?[\-_ ]? ?)([0-9a-fA-F]{4})(?: ?[\-_ ]? ?)([0-9a-fA-F]{4})"

def ConvertSVGtoText(text):
	if text == "percent":
		return("%")
	elif text == "minute":
		return(":")
	elif text == "second":
		return(".")
	elif text == "slash":
		return("/")
	elif text == "hyphen":
		return("-")
	else:
		return(text)

def CourseStyleConverter(text):
	if text == "sb3":
		return("SMB3")
	elif text == "sb":
		return("SMB1")
	elif text == "sw":
		return("SMW")
	elif text == "sbu":
		return("NSMBU")

def ExtractCourseHeaderInfo(bs):
	#Extracting all the info of the header
	#Creating a temporary variable and re-using it as it uses less memory (that's what I think, please prove me wrong when I am :) )
	Temp = bs.find("div", {"class" : re.compile("course-header.*")})
	HeaderColor = re.match(".*course-header.*bg-(\w+).*",str(Temp.attrs)).group(1)
	Temp2 = Temp.find("div", {"class" : "rank"})
	Rank = ""
	for tag in Temp2.findAll("div",{"class" : re.compile("typography.*")}):
		#the percent is called "percent" and a dot is called "second", so we have to convert these kinds of things
		Rank += ConvertSVGtoText(re.match(".*typography.*typography-(\w+).*",str(tag.attrs)).group(1))
	if Rank != "":
		Rank = int(Rank)
	else:
		Rank = 0
	#Removing the rank nonprize element, as it will put the value in front of the difficulty
	[tag.extract() for tag in Temp.find("div",{"class":"rank"})]
	Difficulty = Temp.getText().strip()
	#Recreate the header to only include the "clear-rate" tag
	Temp = Temp.find("div", {"class" : "clear-rate"})
	ClearRate = ""
	#each number is placed in it's own tag, so we are going off all tags in the clear-rate tag
	for tag in Temp.findAll("div",{"class" : re.compile("typography.*")}):
		#the percent is called "percent" and a dot is called "second", so we have to convert these kinds of things
		ClearRate += ConvertSVGtoText(re.match(".*typography.*typography-(\w+).*",str(tag.attrs)).group(1))
	return({"HeaderColor":HeaderColor,"Difficulty":Difficulty,"ClearRate":ClearRate,"Rank":Rank})

def ExtractMakerHeaderInfo(bs):
	#Extracting all the info of the header
	#Creating a temporary variable and re-using it as it uses less memory (that's what I think, please prove me wrong when I am :) )
	Temp = bs.find("div", {"class" : re.compile("creator-header.*")})
	HeaderColor = re.match(".*creator-header.*bg-(\w+).*",str(Temp.attrs)).group(1)
	Temp2 = Temp.find("div", {"class" : "rank"})
	Rank = ""
	for tag in Temp2.findAll("div",{"class" : re.compile("typography.*")}):
		#the percent is called "percent" and a dot is called "second", so we have to convert these kinds of things
		Rank += ConvertSVGtoText(re.match(".*typography.*typography-(\w+).*",str(tag.attrs)).group(1))
	if Rank != "":
		Rank = int(Rank)
	else:
		Rank = 0
	return({"HeaderColor":HeaderColor,"Rank":Rank})

def ExtractMakerInfo(bs):
	#Extracting the Maker info
	Temp = bs.find("a", {"id" : "mii"})
	MakerMiiImage = Temp.find("img")["src"]
	Temp = bs.find("div", {"class" : re.compile("creator-info.*")}).findChildren("div")
	#I could just do it by first = flag, second = Medals, but that will probably break sooner or later.
	for child in Temp:
		if re.match(".*flag.*",str(child.get("class"))):
			MakerCountry = re.match(".*flag.*(\w{2}).*",str(child.get("class"))).group(1)
		elif re.match(".*medals.*",str(child.get("class"))):
			MakerMedals = ""
			for tag in child.findAll("div",{"class" : re.compile("typography.*")}):
				MakerMedals += ConvertSVGtoText(re.match(".*typography.*typography-(\w+).*",str(tag.attrs)).group(1))
		elif re.match(".*name.*",str(child.get("class"))):
			MakerName = child.text.strip()
	return({"MakerName":MakerName,"MakerCountry":MakerCountry,"MakerMedals":MakerMedals,"MakerMiiImage":MakerMiiImage})

def ExtractCourseBodyInfo(bs):
	#Extracting all the info from the "course-info"
	Temp = bs.find("div", {"class" : re.compile("course-info.*")})
	CourseTitle = Temp.find("div", { "class" : "course-title"}).getText().strip()
	CourseImage = Temp.find("div", { "class" : "course-image"}).find("img")["src"]
	CourseStyle = CourseStyleConverter(re.match(".*gameskin.*common_gs_(\w+).*",str(Temp.find("div", { "class" : "gameskin-wrapper"}).findAll("div")[0].attrs)).group(1))
	CreatedAt = Temp.find("div", { "class" : "gameskin-wrapper"}).findAll("div")[1].getText()
	CourseTag = Temp.find("div", { "class" : re.compile("course-tag.*")}).getText()
	#Extracting the Like,Play and share counters
	Temp2 = Temp.find("div", {"class" : re.compile("course-stats-wrapper.*")})
	Temp3 = Temp2.find("div", {"class" : re.compile("liked-count.*")})
	Likes = ""
	for tag in Temp3.findAll("div",{"class" : re.compile("typography.*")}):
		Likes += ConvertSVGtoText(re.match(".*typography.*typography-(\w+).*",str(tag.attrs)).group(1))
	Likes = int(Likes)
	Temp3 = Temp2.find("div", {"class" : re.compile("played-count.*")})
	Plays = ""
	for tag in Temp3.findAll("div",{"class" : re.compile("typography.*")}):
		Plays += ConvertSVGtoText(re.match(".*typography.*typography-(\w+).*",str(tag.attrs)).group(1))
	Plays = int(Plays)
	Temp3 = Temp2.find("div", {"class" : re.compile("shared-count.*")})
	Shared = ""
	for tag in Temp3.findAll("div",{"class" : re.compile("typography.*")}):
		Shared += ConvertSVGtoText(re.match(".*typography.*typography-(\w+).*",str(tag.attrs)).group(1))
	Shared = int(Shared)
	#Exctracting the try count
	Temp2 = Temp.find("div", {"class" : re.compile("tried-count.*")})
	Tries = ""
	for tag in Temp2.findAll("div",{"class" : re.compile("typography.*")}):
		Tries += ConvertSVGtoText(re.match(".*typography.*typography-(\w+).*",str(tag.attrs)).group(1))
	#extracting the source image for full level overview
	Temp2 = Temp.find("div", {"class" : re.compile("course-image-full-wrapper.*")})
	CourseFullImage = Temp2.find("img", { "class" : "course-image-full"})["src"]
	Temp2 = Temp.find("div", {"class" : re.compile("course-detail-wrapper.*")})
	MakerInfo = ExtractMakerInfo(Temp2)
	MakerName = MakerInfo["MakerName"]
	MakerCountry = MakerInfo["MakerCountry"]
	MakerMedals = MakerInfo["MakerMedals"]
	MakerMiiImage = MakerInfo["MakerMiiImage"]
	return({"CourseTitle":CourseTitle,"CourseImage":CourseImage,"CourseStyle":CourseStyle,"CreatedAt":CreatedAt,"CourseTag":CourseTag,"Likes":Likes,"Plays":Plays,"Shared":Shared,"Tries":Tries,"CourseFullImage":CourseFullImage,"MakerMiiImage":MakerMiiImage,"MakerCountry":MakerCountry,"MakerMedals":MakerMedals,"MakerName":MakerName})

def ExtractCourseRecords(bs):
	#Extracting the worldrecord and first completed
	Temp = bs.find("div", {"class" : re.compile("two-column-wrapper.*")})
	#Record
	Temp2 = Temp.find("div", {"class" : re.compile(".*fastest-user.*")})
	if not Temp2.find("div", {"class" : "no-users-message"}):
		Temp3 = Temp2.find("div", {"class" : "user-wrapper"})
		#If there isn't a record, Nintendo doesn't return "no-users-message" like they do with first completed by
		#but I left it in as an extra check, most of the time if there isn't a record the Mii icon will be "Dummy"
		if not Temp3.find("a", {"class" : "icon-dummy-mii"}):
			RecordMiiImage = Temp3.find("div", {"class" : "mii-wrapper"}).find("a",{"id" : "mii"}).find("img")["src"]
		else:
			RecordMiiImage = ""
		for child in Temp3.findChildren("div"):
			#If there isn't a record, the flag will remain empty, so we check with .+ (as this isn't true when empty)
			if re.match(".*flag .+",str(child.get("class"))):
				RecordCountry = re.match(".*flag.*(\w{2}).*",str(child.get("class"))).group(1)
			else:
				RecordCountry = ""
			if re.match(".*name.*",str(child.get("class"))):
				RecordName = child.text.strip()
			else:
				RecordName = ""
		Temp3 = Temp2.find("div", {"class" : "clear-time"})
		RecordTime = ""
		for tag in Temp2.findAll("div",{"class" : re.compile("typography.*")}):
			RecordTime += ConvertSVGtoText(re.match(".*typography.*typography-(\w+).*",str(tag.attrs)).group(1))
	else:
		RecordMiiImage = ""
		RecordCountry = ""
		RecordName = ""
		RecordTime = ""
	#First
	Temp2 = Temp.find("div", {"class" : re.compile(".*first-user.*")})
	if not Temp2.find("div", {"class" : "no-users-message"}):
		Temp3 = Temp2.find("div", {"class" : "user-wrapper"})
		FirstMiiImage = Temp3.find("div", {"class" : "mii-wrapper"}).find("a",{"id" : "mii"}).find("img")["src"]
		for child in Temp3.findChildren("div"):
			if re.match(".*flag.*",str(child.get("class"))):
				FirstCountry = re.match(".*flag.*(\w{2}).*",str(child.get("class"))).group(1)
			elif re.match(".*name.*",str(child.get("class"))):
				FirstName = child.text.strip()
	else:
		FirstMiiImage = ""
		FirstCountry = ""
		FirstName = ""
	return({"RecordMiiImage":RecordMiiImage,"RecordCountry":RecordCountry,"RecordName":RecordName,"RecordTime":RecordTime,"FirstMiiImage":FirstMiiImage,"FirstCountry":FirstCountry,"FirstName":FirstName})

def ExtractCourseRecentlyPlayedBy(bs):
	#extracting the recently played by users
	Temp = bs.find("div", {"class" : re.compile(".*played-body.*")}).findAll("li")
	RecentPlayers = []
	for Temp2 in Temp:
		Temp3 = Temp2.find("div", {"class" : "user-wrapper"})
		UserMii = Temp3.find("div", {"class" : "mii-wrapper"}).find("a",{"id" : "mii"}).find("img")["src"]
		for child in Temp3.findChildren("div"):
			if re.match(".*flag.*",str(child.get("class"))):
				UserCountry = re.match(".*flag.*(\w{2}).*",str(child.get("class"))).group(1)
			elif re.match(".*name.*",str(child.get("class"))):
				UserName = child.text.strip()
		RecentPlayers.append({"UserName":UserName,"UserCountry":UserCountry,"UserMii":UserMii})
	return(RecentPlayers)

def ExtractCourseClearedBy(bs):
	#Extracting the Cleared by users
	Temp = bs.find("div", {"class" : re.compile(".*cleared-body.*")}).findAll("li")
	ClearedBy = []
	for Temp2 in Temp:
		Temp3 = Temp2.find("div", {"class" : "user-wrapper"})
		UserMii = Temp3.find("div", {"class" : "mii-wrapper"}).find("a",{"id" : "mii"}).find("img")["src"]
		for child in Temp3.findChildren("div"):
			if re.match(".*flag.*",str(child.get("class"))):
				UserCountry = re.match(".*flag.*(\w{2}).*",str(child.get("class"))).group(1)
			elif re.match(".*name.*",str(child.get("class"))):
				UserName = child.text.strip()
		ClearedBy.append({"UserName":UserName,"UserCountry":UserCountry,"UserMii":UserMii})
	return(ClearedBy)

def ExtractCourseLikedBy(bs):
	#Extracting the Liked by users
	Temp = bs.find("div", {"class" : re.compile(".*liked-body.*")}).findAll("li")
	LikedBy = []
	for Temp2 in Temp:
		Temp3 = Temp2.find("div", {"class" : "user-wrapper"})
		UserMii = Temp3.find("div", {"class" : "mii-wrapper"}).find("a",{"id" : "mii"}).find("img")["src"]
		for child in Temp3.findChildren("div"):
			if re.match(".*flag.*",str(child.get("class"))):
				UserCountry = re.match(".*flag.*(\w{2}).*",str(child.get("class"))).group(1)
			elif re.match(".*name.*",str(child.get("class"))):
				UserName = child.text.strip()
		LikedBy.append({"UserName":UserName,"UserCountry":UserCountry,"UserMii":UserMii})
	return(LikedBy)

#Gets all the available info for the given ID
#Returns a dictionary with different dictionaries and lists of dictionaries
def GetCourseByID(ID):
	#Sometimes i had to do it the ugly way (mostly where you see .attrs and .get("class")), because the different versions of BeautifulSoup return different things
	#This is the most versatile regex I was able to come up with, it will be able to change incorrect input to correct output (only bad formatted, it can't do wonders ;) )
	InputValidation = re.match("{IDRegex}".format(IDRegex=IDRegex),ID)
	if InputValidation:
		ID = "{one}-{two}-{three}-{four}".format(one=InputValidation.group(1),two=InputValidation.group(2),three=InputValidation.group(3),four=InputValidation.group(4)).upper()
	else:
		return({"Status":{"StatusCode":400,"StatusExplanation": "the given ID wasn't correctly formatted"}})
	page = requests.get("https://supermariomakerbookmark.nintendo.net/courses/{ID}".format(ID=ID))
	if not page.status_code == 404:
		bs = BeautifulSoup(page.content, "html.parser")
		#using the extract functions
		Header = ExtractCourseHeaderInfo(bs)
		Body = ExtractCourseBodyInfo(bs)
		Records = ExtractCourseRecords(bs)
		RecentPlayers = ExtractCourseRecentlyPlayedBy(bs)
		ClearedBy = ExtractCourseClearedBy(bs)
		LikedBy = ExtractCourseLikedBy(bs)
		return( {"ID" : ID,
				"Header" : Header,
				"Body": Body,
				"Records": Records,
				"RecentPlayers":RecentPlayers,
				"ClearedBy":ClearedBy,
				"LikedBy":LikedBy,
				"Status":{"StatusCode":200,"StatusExplanation":"Everything went great!"}
				})
	else:
		return({"Status":{"StatusCode":404,"StatusExplanation":"Incorrect ID given, Not Found"}})

#This gets 10 random SMM courses
#Returns a lits of dictionaries 
def GetRecommendedCourses():
	page = requests.get("https://supermariomakerbookmark.nintendo.net/pickup")
	if not page.status_code == 404:
		bs = BeautifulSoup(page.content, "html.parser")
		courses = bs.findAll("div",{"class" : "course-card"})
		StrippedCourses = []
		for course in courses:
			Header = ExtractCourseHeaderInfo(course)
			Body = ExtractCourseBodyInfo(course)
			ID = re.match("/courses/{IDRegex}".format(IDRegex=IDRegex),course.find("a", {"class" : "button course-detail link"})["href"])
			ID = "{one}-{two}-{three}-{four}".format(one=ID.group(1),two=ID.group(2),three=ID.group(3),four=ID.group(4)).upper()
			StrippedCourses.append({"Header":Header,
									"Body":Body,
									"ID":ID})
		return({"Status":{"StatusCode":200,"StatusExplanation":"Everything went great!"},
				"StrippedCourses":StrippedCourses})
	else:
		return({"Status":{"StatusCode":404,"StatusExplanation":"Something went wrong while requesting the page?"}})

#This gets the Ranked courses
#There are optional parameters, but it defaults to the total liked count (all time), as Nintendo does.
def GetRankedCourses(PageNum=1,Type="total_liked_count"):
	#Valid input Type: total_liked_count,weekly_liked_count,like_rate
	#Valid input PageNum: 1-10
	if PageNum > 10:
		return({"Status":{"StatusCode":400,"StatusExplanation": "Pagenumber is to high."}})
	if not (Type == "total_liked_count") and not (Type == "weekly_liked_count") and not (Type == "like_rate"):
		return({"Status":{"StatusCode":400,"StatusExplanation": "Unexpected Type received."}})
	page = requests.get("https://supermariomakerbookmark.nintendo.net/ranking?page={PageNum}&type={Type}".format(PageNum=PageNum,Type=Type))
	if not page.status_code == 404:
		bs = BeautifulSoup(page.content, "html.parser")
		courses = bs.findAll("div",{"class" : "course-card"})
		StrippedCourses = []
		for course in courses:
			Header = ExtractCourseHeaderInfo(course)
			Body = ExtractCourseBodyInfo(course)
			ID = re.match("/courses/{IDRegex}".format(IDRegex=IDRegex),course.find("a", {"class" : "button course-detail link"})["href"])
			ID = "{one}-{two}-{three}-{four}".format(one=ID.group(1),two=ID.group(2),three=ID.group(3),four=ID.group(4)).upper()
			StrippedCourses.append({"Header":Header,
									"Body":Body,
									"ID":ID})
		return({"Status":{"StatusCode":200,"StatusExplanation":"Everything went great!"},
				"StrippedCourses":StrippedCourses})
	else:
		return({"Status":{"StatusCode":404,"StatusExplanation":"Something went wrong while requesting the page?"}})

#This gets the highest ranked players (most stars received)
#There are optional parameters, but it defaults to the total liked count (all time), as Nintendo does.
def GetRankedMakers(PageNum=1,Type="total_liked_count"):
	#Valid input Type: total_liked_count,weekly_liked_count
	#Valid input PageNum: 1-5
	if PageNum > 5:
		return({"Status":{"StatusCode":400,"StatusExplanation": "Pagenumber is to high."}})
	if not (Type == "total_liked_count") and not (Type == "weekly_liked_count"):
		return({"Status":{"StatusCode":400,"StatusExplanation": "Unexpected Type received."}})
	page = requests.get("https://supermariomakerbookmark.nintendo.net/ranking/creator?page={PageNum}&type={Type}".format(PageNum=PageNum,Type=Type))
	if not page.status_code == 404:
		bs = BeautifulSoup(page.content, "html.parser")
		Makers = bs.findAll("div",{"class" : "creator-card"})
		RankedMakers = []
		for Maker in Makers:
			#I didn't include the stars in the ExtractMakerInfo function, as it is specific to the Ranked Maker page
			MakerInfo = ExtractMakerInfo(Maker)
			MakerName = MakerInfo["MakerName"]
			MakerCountry = MakerInfo["MakerCountry"]
			MakerMedals = MakerInfo["MakerMedals"]
			MakerMiiImage = MakerInfo["MakerMiiImage"]
			MakerHeaderInfo = ExtractMakerHeaderInfo(Maker)
			MakerLikes = ""
			#Extracting the total likes
			Likes = Maker.find("div",{"class" : "liked-count"})
			for tag in Likes.findAll("div",{"class" : re.compile("typography.*")}):
					MakerLikes += ConvertSVGtoText(re.match(".*typography.*typography-(\w+).*",str(tag.attrs)).group(1))
			RankedMakers.append({"MakerName":MakerName,"MakerCountry":MakerCountry,"MakerMedals":MakerMedals,"MakerMiiImage":MakerMiiImage,"MakerLikes":MakerLikes,
								"Header":MakerHeaderInfo})
		return({"Status":{"StatusCode":200,"StatusExplanation":"Everything went great!"},
				"RankedMakers":RankedMakers})
	else:
		return({"Status":{"StatusCode":404,"StatusExplanation":"Something went wrong while requesting the page?"}})