import locale
from tagmods import tagsmod
import os
import re
import sys
import requests


locale.setlocale(locale.LC_ALL, "ru-ru.UTF-8")


# --- Search keyword in text ---
def search_in_fulltext(word):

	fullTextLower = fullText.lower()

	def find_word():

		# find "text" in "sample text," and make " text,"
		def expand_word():
			if 0 < shiftpos < len(fullTextLower) - 2:
				return fullTextLower[shiftpos - 1:shiftpos + len(word) + 1]

		shiftpos = fullTextLower.find(word)
		for counter in range(fullTextLower.count(word)):
			print(expand_word())
			print(tagsmod.words_gen(word))
			if expand_word() not in tagsmod.words_gen(word):
				shiftpos = fullTextLower.find(word, shiftpos + len(word))
			else:
				return True

		return False

	if "+" in word:
		word = word.replace("+", "")
		if find_word():
			return key_tags.get(word+"+")

	elif fullTextLower.find(word) >= 0:
		return key_tags.get(word)


# -----------------------------------------------

if __name__ != "__main__":
	exit()


# --- Try open "tagsfile" file ---
try:
	with open(r"c:\Projects\hw\tagsfile", "r", encoding="utf-8") as tfile:
		key_tags = {}
		for line in tfile:
			if line != "":
				keyword = line[0:line.find(":")]  			# cut keyword
				tags = line[line.find(":")+1:]				# cut tags
				key_tags.setdefault(keyword, tags[:-1])		# construct dict... ['word':'tag1,tag2,...,tagN']

except FileNotFoundError:
	print("File 'tagsfile' not exist.")
	exit()


# --- Transfer "tags.py" argument (full path to work subfolder) ---
subFolder = ""
if len(sys.argv) == 2:
	subFolder = re.sub(r"^\s+|\n|\r|\s+$", '', sys.argv[1])
	subFolder = re.sub(r"[^0-9a-zA-Z -\\\/:,\\(\\)\\-\\.\\+_" + tagsmod.alphabetRus + "]", "", subFolder)
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
		fullText = re.sub(r"^\s+|\n|\r|\s+$", '', fullTextUntouched)

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
for file in os.listdir(subFolder):				 		 # count the Final RAR Archive(s) size
	extension = os.path.splitext(file)[1][1:].strip()
	if extension == "rar":
		rarSize += os.path.getsize(subFolder+"\\"+file)	 # size in bytes

rarSize /= (1024 * 1024)				 		 		 # size in megabytes


# --- Try open "size.txt" file ---
try:
	fileName = subFolder + r"\size.txt"
	with open(fileName, "r", encoding="UTF-8") as txtFile:
		originalSize = txtFile.read()				   # get original size from "size.txt"
		if originalSize.find(r"https://") == 0:
			url = re.sub("[^a-zA-Z0-9\\-_:%./]", "", originalSize)
			req = requests.get(url)
			elemList = req.text.split('"size": ')      # find first '"size":' in page code - this is preposition of Size
			f = elemList[1].find(",")				   # find ',' in received substring - this is postposition of Size
			originalSize = int(int(elemList[1][:f]) / (1024*1024))	 # delete postposition, receive Size in megabytes
		else:
			originalSize = int(re.sub("[^0-9]", "", originalSize))	 # Size in megabytes

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
	print("File 'size.txt' not exist.")
	exit()


# --- Hashtags ---
# --- Find keywords in text ---
keywords = list(map(search_in_fulltext, key_tags))  	  # duplicated tags in tuples  		[a,b,c] [] [a,b,d,e]
keywords = list(filter(None, keywords))					  # filtering					 		[a,b,c] [a,b,d,e]
keywords = ",".join(keywords).replace("+", "")  		  # convert all to monostring and clean  "a,b,c,a,b,d,e"
keywords = list(set(keywords.split(",")))				  # split snd deduplicate		  		"a","b","c","d","e"

finalText += '#' + ' #'.join(keywords)


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
