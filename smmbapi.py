import requests
from BeautifulSoup import BeautifulSoup
import re

def convert_svg_typography_to_text(text):
	if text == "percent":
		return("%")
	elif text == "minute":
		return(":")
	elif text == "second":
		return(".")
	elif text == "slash":
		return("/")
	else:
		return(text)

def course_style_extract(text):
	if text == "sb3":
		return("SMB3")
	elif text == "sb":
		return("SMB1")
	elif text == "sw":
		return("SMW")
	elif text == "sbu":
		return("NSMBU")

def smmbapi(ID):
	page = requests.get("https://supermariomakerbookmark.nintendo.net/courses/{ID}".format(ID=ID))

	bs = BeautifulSoup(page.content)

	#Extracting all the info of the header
	#Creating a temporary variable and re-using it as it uses less memory (that's what I think, please prove me wrong when I am :) )
	Temp = bs.find("div", {"class" : re.compile("course-header.*")})
	HeaderColor = re.match("course-header bg-(.*)",Temp.attrMap["class"]).group(1)
	RankNonprize = Temp.find("div", {"class" : "rank nonprize"})
	#Removing the rank nonprize element, as it will put the value in front of the difficulty
	[tag.extract() for tag in Temp.find("div",{"class":"rank nonprize"})]
	Difficulty = Temp.getText()
	#Recreate the header to only include the "clear-rate" tag
	Temp = Temp.find("div", {"class" : "clear-rate"})
	ClearRate = ""
	#each number is placed in it's own tag, so we are going off all tags in the clear-rate tag
	for tag in Temp.findAll("div",{"class" : re.compile("typography.*")}):
		#the percent is called "percent" and a dot is called "second", so we have to convert these kinds of things
		ClearRate += convert_svg_typography_to_text(re.match("typography typography-(.*)",tag.attrMap["class"]).group(1))



	#Extracting all the info from the "course-info"
	Temp = bs.find("div", {"class" : re.compile("course-info.*")})
	CourseTitle = Temp.find("div", { "class" : "course-title"}).getText()
	CourseImage = Temp.find("div", { "class" : "course-image"}).find("img")["src"]
	CourseStyle = course_style_extract(re.match("gameskin.*common_gs_(.*)",Temp.find("div", { "class" : "gameskin-wrapper"}).findAll("div")[0].attrs[0][1]).group(1))
	CreatedAt = Temp.find("div", { "class" : "gameskin-wrapper"}).findAll("div")[1].getText()
	CourseTag = Temp.find("div", { "class" : re.compile("course-tag.*")}).getText()

	#Extracting the Like,Play and share counters
	Temp2 = Temp.find("div", {"class" : re.compile("course-stats-wrapper.*")})

	Temp3 = Temp2.find("div", {"class" : re.compile("liked-count.*")})
	Likes = ""
	for tag in Temp3.findAll("div",{"class" : re.compile("typography.*")}):
		Likes += convert_svg_typography_to_text(re.match("typography typography-(.*)",tag.attrMap["class"]).group(1))

	Likes = int(Likes)

	Temp3 = Temp2.find("div", {"class" : re.compile("played-count.*")})
	Plays = ""
	for tag in Temp3.findAll("div",{"class" : re.compile("typography.*")}):
		Plays += convert_svg_typography_to_text(re.match("typography typography-(.*)",tag.attrMap["class"]).group(1))

	Plays = int(Plays)

	Temp3 = Temp2.find("div", {"class" : re.compile("shared-count.*")})
	Shared = ""
	for tag in Temp3.findAll("div",{"class" : re.compile("typography.*")}):
		Shared += convert_svg_typography_to_text(re.match("typography typography-(.*)",tag.attrMap["class"]).group(1))

	Shared = int(Shared)

	#Exctracting the try count
	Temp2 = Temp.find("div", {"class" : re.compile("tried-count.*")})
	Tries = ""
	for tag in Temp2.findAll("div",{"class" : re.compile("typography.*")}):
		Tries += convert_svg_typography_to_text(re.match("typography typography-(.*)",tag.attrMap["class"]).group(1))

	#extracting the source image for full level overview
	Temp2 = Temp.find("div", {"class" : re.compile("course-image-full-wrapper.*")})
	CourseFullImage = Temp2.find("img", { "class" : "course-image-full"})["src"]

	#Extracting the creator info
	Temp2 = Temp.find("div", {"class" : re.compile("course-detail-wrapper.*")})
	Temp3 = Temp2.find("a", {"id" : "mii"})
	CreatorMiiImage = Temp3.find("img")["src"]
	Temp3 = Temp2.find("div", {"class" : re.compile("creator-info.*")}).findChildren("div")
	#I could just do it by first = flag, second = Medals, but that will probably break sooner or later.
	for child in Temp3:
		if re.match("flag.*",child.get("class")):
			CreatorCountry = re.match("flag (.*)",child.get("class")).group(1)
		elif re.match("medals.*",child.get("class")):
			CreatorMedals = re.match("medals bg-image common_(.*)",child.get("class")).group(1)
		elif re.match("name.*",child.get("class")):
			CreatorName = child.text

	#Extracting the worldrecord and first completed
	Temp = bs.find("div", {"class" : re.compile("two-column-wrapper.*")})
	#Record
	Temp2 = Temp.find("div", {"class" : re.compile(".*fastest-user.*")})
	if not Temp2.find("div", {"class" : "no-users-message"}):
		Temp3 = Temp2.find("div", {"class" : "user-wrapper"})
		RecordMiiImage = Temp3.find("div", {"class" : "mii-wrapper"}).find("a",{"id" : "mii"}).find("img")["src"]
		for child in Temp3.findChildren("div"):
			if re.match("flag.*",child.get("class")):
				RecordCountry = re.match("flag (.*)",child.get("class")).group(1)
			elif re.match("name.*",child.get("class")):
				RecordName = child.text
		Temp3 = Temp2.find("div", {"class" : "clear-time"})
		RecordTime = ""
		for tag in Temp2.findAll("div",{"class" : re.compile("typography.*")}):
			RecordTime += convert_svg_typography_to_text(re.match("typography typography-(.*)",tag.attrMap["class"]).group(1))
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
			if re.match("flag.*",child.get("class")):
				FirstCountry = re.match("flag (.*)",child.get("class")).group(1)
			elif re.match("name.*",child.get("class")):
				FirstName = child.text
	else:
		FirstMiiImage = ""
		FirstCountry = ""
		FirstName = ""

	#extracting the recently played by users
	Temp = bs.find("div", {"class" : re.compile(".*played-body.*")}).findAll("li")
	RecentPlayers = []
	for Temp2 in Temp:
		Temp3 = Temp2.find("div", {"class" : "user-wrapper"})
		UserMii = Temp3.find("div", {"class" : "mii-wrapper"}).find("a",{"id" : "mii"}).find("img")["src"]
		for child in Temp3.findChildren("div"):
			if re.match("flag.*",child.get("class")):
				UserCountry = re.match("flag (.*)",child.get("class")).group(1)
			elif re.match("name.*",child.get("class")):
				UserName = child.text
		RecentPlayers.append({"UserName":UserName,"UserCountry":UserCountry,"UserMii":UserMii})

	#Extracting the Cleared by users
	Temp = bs.find("div", {"class" : re.compile(".*cleared-body.*")}).findAll("li")
	ClearedBy = []
	for Temp2 in Temp:
		Temp3 = Temp2.find("div", {"class" : "user-wrapper"})
		UserMii = Temp3.find("div", {"class" : "mii-wrapper"}).find("a",{"id" : "mii"}).find("img")["src"]
		for child in Temp3.findChildren("div"):
			if re.match("flag.*",child.get("class")):
				UserCountry = re.match("flag (.*)",child.get("class")).group(1)
			elif re.match("name.*",child.get("class")):
				UserName = child.text
		ClearedBy.append({"UserName":UserName,"UserCountry":UserCountry,"UserMii":UserMii})

	#Extracting the Liked by users
	Temp = bs.find("div", {"class" : re.compile(".*liked-body.*")}).findAll("li")
	LikedBy = []
	for Temp2 in Temp:
		Temp3 = Temp2.find("div", {"class" : "user-wrapper"})
		UserMii = Temp3.find("div", {"class" : "mii-wrapper"}).find("a",{"id" : "mii"}).find("img")["src"]
		for child in Temp3.findChildren("div"):
			if re.match("flag.*",child.get("class")):
				UserCountry = re.match("flag (.*)",child.get("class")).group(1)
			elif re.match("name.*",child.get("class")):
				UserName = child.text
		LikedBy.append({"UserName":UserName,"UserCountry":UserCountry,"UserMii":UserMii})

	return({"Header":{"HeaderColor":HeaderColor,"RankNonprize":RankNonprize,"Difficulty":Difficulty,"ClearRate":ClearRate},
			"Body":{"CourseTitle":CourseTitle,"CourseImage":CourseImage,"CourseStyle":CourseStyle,"CreatedAt":CreatedAt,"CourseTag":CourseTag,"Likes":Likes,"Plays":Plays,"Shared":Shared,"Tries":Tries,"CourseFullImage":CourseFullImage,"CreatorMiiImage":CreatorMiiImage,"CreatorCountry":CreatorCountry,"CreatorMedals":CreatorMedals,"CreatorName":CreatorName},
			"Records":{"RecordMiiImage":RecordMiiImage,"RecordCountry":RecordCountry,"RecordName":RecordName,"RecordTime":RecordTime,"FirstMiiImage":FirstMiiImage,"FirstCountry":FirstCountry,"FirstName":FirstName},
			"RecentPlayers":RecentPlayers,
			"ClearedBy":ClearedBy,
			"LikedBy":LikedBy
			})