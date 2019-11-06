import locale
import re
from .globals import *

locale.setlocale(locale.LC_ALL, "ru-ru.UTF-8")


# Delete all Spaces, "End of Line" sign, "Return" sign
def clean(prm):
    prm = re.sub(r"^\s+|\n|\s+|\r|\s+$", '', prm)
    return prm


# Replace special symbols
def repl(text):
    text = text.replace("▪", "-")
    text = text.replace("•", "-")
    text = text.replace("▪️", "-")
    return text


# Generate Word's variants
# word = "api" => " api", "api ", " api ", ".api", "api."...
# Concatenate word + signs
def words_gen(word):
    signs = r".,:;-?!()[]\'вЂ™ "
    genwords = []
    for sr in signs:
        for sl in signs:
            genwords.extend([sl + word + sr, word + sr, sl + word])
    return list(set(genwords))


# --- Write "word[+]:tag1,tag2..." into "tagsfile" ---
def add_keytags():
    try:
        print(
              "\nSample1:  keyword = [+] tag1 tag2...tagN\n"
              "Sample2:  keyword1 (new keyword2)...keywordN = [+] tags_abbr tag1 tag2\n"
              "\nkeyword1 (new keyword2)...keywordN - sequence of keywords\n"
              "(new keyword2) - one keyword\n"
              "'=' - separator\n"
              "[+] - Advanced search (optional parameter)\n"
              "\ntags_abbr - Tag abbreviations:\n"
              "dev_tags - development\n"
              "des_tags - design\n"
              "biz_tags - business\n"
              "traff_tags - traffic\n"
              "trav_tags - travels, rest\n"
              "office_tags - office\n"
              "webdes_tags - web-design\n"
              "\nSample: Р±РѕС‚ (РґРІР° Р±РѕС‚Р°) Р±РѕС‚Сѓ Р±РѕС‚РѕРј (Рѕ Р±РѕС‚Рµ) = + dev_tags Р±РѕС‚С‹\n"
              "Sample: РґРёР·Р°Р№РЅ = des_tags\n"
        )

        new_keytags_input = input().lower()
        if new_keytags_input != "":
            new_keytags_input = clean(new_keytags_input)
            new_keytags_input = re.sub("[^-=_ a-z0-9\\+\\(\\)"+alphabetRusLower+"]", "", new_keytags_input)
            if new_keytags_input.find("="):

                anchorpoint = new_keytags_input.find("=")

                # 1. cut all "(keyword) " from "new_keytags_input"
                monokeyword = []
                try:
                    while True:
                        if 0 <= new_keytags_input.find("(") < anchorpoint:

                            # cut one "(keyword) " from "new_keytags_input"
                            kw = clean(new_keytags_input[new_keytags_input.find("(")+1:new_keytags_input.find(")")])
                            new_keytags_input = new_keytags_input.replace("("+kw+")", "")

                            # delete all possible '(' inside monokeyword
                            monokeyword.append(kw.replace("(", ""))

                            # renew anchorpoint
                            anchorpoint = new_keytags_input.find("=")
                        else:
                            break
                except True:
                    print("')' required.")
                    exit()

                # 2. get "this this", convert to [this,this]
                keywords = new_keytags_input[0:new_keytags_input.find("=")].split(" ")
                keywords.extend(monokeyword)
                keywords = list(filter(None, keywords))

                # 3. advanced search?
                if new_keytags_input.find("+") > anchorpoint:
                    adv_search = "+"
                    anchorpoint = new_keytags_input.find("+")
                else:
                    adv_search = ""

                # 4. tag abbreviations?
                abbr_tags = ""
                tag_abbr = ["dev_tags", "des_tags", "traff_tags", "office_tags", "webdes_tags"]
                for tg in tag_abbr:
                    if new_keytags_input.find(tg) > anchorpoint:
                        if tg == "dev_tags":
                            abbr_tags += "dev,РїСЂРѕРіСЂР°РјРјРёСЂРѕРІР°РЅРёРµ,СЂР°Р·СЂР°Р±РѕС‚РєР°"
                        if tg == "des_tags":
                            abbr_tags += "design,РґРёР·Р°Р№РЅ"
                        if tg == "traff_tags":
                            abbr_tags += "С‚СЂР°С„РёРє,Р°СЂР±РёС‚СЂР°Р¶"
                        if tg == "office_tags":
                            abbr_tags += "office,РѕС„РёСЃ"
                        if tg == "webdes_tags":
                            abbr_tags += "webdesign,РІРµР±РґРёР·Р°Р№РЅ,РІСЌР±РґРёР·Р°Р№РЅ"
                        anchorpoint += len(tg) + 1                         # abbr_tags + space

                # 5. other tags
                other_tags = ""
                if anchorpoint > 0:
                    otrtags = new_keytags_input[anchorpoint+1:].split(" ")
                    otrtags = list(filter(None, otrtags))
                    for ot in otrtags:
                        other_tags += "," + re.sub("[^a-z0-9"+alphabetRusLower+"]", "", ot)
                    if abbr_tags == "":
                        other_tags = other_tags[1:]                        # delete pre-space

                # 6. assemble string
                astring = ""
                for kwd in keywords:
                    astring += kwd + adv_search + ":" + abbr_tags + other_tags + "\n"

                # confirm data...
                try:
                    inp = input("\nAre you want to add\n\n{0}\nto the tags file? [y/n]".format(astring))
                    inp = re.sub("^yYРЅРќ", "", inp)
                    if inp != '':

                        # ...and check of existence
                        try:
                            with open(r"c:\Projects\hw\tagsfile", "a+", encoding="utf-8") as tfile:
                                for line in tfile:
                                    if line != "":
                                        keyw = line[0:line.find(":")]
                                        keyw = keyw.replace("+", "")

                                        if astring.find(keyw):
                                            print("Sorry, this tag '{0}' yet exist.".format(keyw))
                                            tfile.close()
                                            exit()

                                if tfile.write(astring) > 0:
                                    print("Ok, new keytags is added")

                        except FileNotFoundError:
                            print("File 'tagsfile' not exist.")
                            exit()
                except True:
                    print("Operation is canceled.")
                    exit()

    except True:
        print("Operation is canceled.")
