import locale
import tagsmod
import os
import re
import sys
import requests


locale.setlocale(locale.LC_ALL, "ru-ru.UTF-8")


# --- Try open "tagsfile" file ---
try:
	with open(r"c:\Projects\hw\tagsfile", "r", encoding="utf-8") as tfile:
		key_tags = {}
		for line in tfile:
			if line != "":
				kwd = line[line.find("<keyword>")+len("<keyword>"):line.find("</keyword>")]  # keyword<tag>tag1</tag>
				keyword = kwd[0:kwd.find("<tag>")]  # cut keyword

				shiftpos_opentag = kwd.find("<tag>")
				shiftpos_closetag = kwd.find("</tag>")

				tags = ''
				for counter in range(kwd.count("<tag>")):

					# one tag
					tag = kwd[kwd.find("<tag>", shiftpos_opentag)+len("<tag>"):kwd.find("</tag>", shiftpos_closetag)]

					# pack tags in string
					tags += str(tag) + ","

					# shift position for 'find', search next tag
					shiftpos_opentag = kwd.find("<tag>", shiftpos_opentag+len("<tag>") + len("<tag>"))
					shiftpos_closetag = kwd.find("</tag>", shiftpos_closetag + len("</tag>"))

				key_tags.setdefault(keyword, tags[:-1])		# construct dict... [word:'tag1,tag2,tag3'...]

except FileNotFoundError:
	print("File 'tagsfile' not exist.")
	exit()


# --- Search keyword in text ---
def search_in_fulltext(word):

	def find_word():

		# find "text" in "sample text," and do " text,"
		def expand_word():
			if 0 < shiftpos < len(fullText) - 2:
				return fullText[shiftpos - 1:shiftpos + len(word) + 1].lower()

		shiftpos = fullText.lower().find(word)
		for counter in range(fullText.lower().count(word)):
			if expand_word() not in tagsmod.words_gen(word):
				shiftpos = fullText.lower().find(word, shiftpos + len(word))
			else:
				return True

		return False

	if "<advsearch>" in word:
		word = word.replace("<advsearch>", "")
		if find_word():
			return key_tags.get(word+"<advsearch>")

	elif fullText.lower().find(word) >= 0:
		return key_tags.get(word)


# -----------------------------------------------

# --- Get "tags.py" argument (full path to work subfolder) ---
subFolder = ""
if len(sys.argv) == 2:
	subFolder = tagsmod.clean(sys.argv[1])
	subFolder = subFolder[:-1]
else:
	exit()


# --- Try open "tg-message.txt" file ---
try:
	fileName = subFolder + r"\tg-message.txt"
	with open(fileName, "r", encoding="UTF-8") as txtFile:
		fullTextUntouched = txtFile.read()
		if fullTextUntouched.find("**") == 0:
			exit()
		fullTextUntouched = tagsmod.repl(fullTextUntouched)
		fullText = tagsmod.clean(fullTextUntouched)

except FileNotFoundError:
	print("File 'tg-message.txt' not exist.")
	exit()


# --- Begin construct result text ---
finalText = fullTextUntouched + "\n"


# --- **Header** ---
header = finalText[0:finalText.find("\n")]
finalText = finalText.replace(header, "**" + header + "**", 1)


# --- Download (Size) - Compress to X times ---
rarSize = 0
for file in os.listdir(subFolder):				 # count the Final RAR Archive(s) size
	extension = os.path.splitext(file)[1][1:].strip()
	if extension == "rar":
		rarSize += os.path.getsize(subFolder+"\\"+file)	 # size in bytes

rarSize /= (1024 * 1024)				 		 # size in megabytes


# --- Try open "размер.txt" file ---
try:
	fileName = subFolder + r"\размер.txt"
	with open(fileName, "r", encoding="UTF-8") as txtFile:
		originalSize = txtFile.read()					 # get original size from "размер.txt"
		if originalSize.find(r"https://") == 0:
			url = re.sub("[^a-zA-Z0-9\\-_:%./]", "", originalSize)
			req = requests.get(url)
			elemList = req.text.split('"size": ')        # find first '"size":' in page code - this is preposition of Size
			f = elemList[1].find(",")					 # find ',' in received substring - this is postposition of Size
			originalSize = int(int(elemList[1][:f]) / (1024*1024))	 # delete postposition, receive Size in megabytes
		else:
			originalSize = int(re.sub("[^0-9]", "", originalSize))	  # Size in megabytes

	compress_ratio = originalSize / rarSize

	if rarSize < 1024:
		rarSize = str(int(rarSize)) + " Мб"
	else:
		rarSize = "{0:.2f} Гб".format(rarSize / 1024)

	if finalText[-1] != "\n":
		finalText += "\n\n"
	elif finalText[-2] != "\n":
		finalText += "\n"

	# --- "Download" string ---
	finalText += "Скачать ({size}) - Сжато в {c_ratio:.2f} раза\n\n".format(size=rarSize, bytes=bytes,
																			c_ratio=compress_ratio)
except FileNotFoundError:
	print("File 'размер.txt' not exist.")
	exit()


# --- Hashtags ---
# --- Find keywords in text ---
keywords = list(map(search_in_fulltext, key_tags))  	  # duplicated tags in tuples  		[a,b,c] [] [a,b,d,e]
keywords = list(filter(None, keywords))					  # filtering					 		[a,b,c] [a,b,d,e]
keywords = ",".join(keywords).replace("<advsearch>", "")  # convert all to monostring and clean  "a,b,c,a,b,d,e"
keywords = list(set(keywords.split(",")))				  # split snd deduplicate		  		"a","b","c","d","e"

finalText = finalText + '#' + ' #'.join(keywords)


# --- Subscribe message ---
finalText += "\n\nПереходи в @the_most_gusto. Здесь есть ещё!"


# --- Output to Screen ---
print(finalText + "\v")


# --- Write finalText to file ---
try:
	fileName = subFolder + r"\tg-message.txt"
	with open(fileName, "w", encoding="UTF-8") as txtFile:
		txtFile.write(finalText)
except FileNotFoundError:
	print("File 'tg-message.txt' not exist.")
	exit()
