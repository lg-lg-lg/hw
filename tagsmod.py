import locale
import re

locale.setlocale(locale.LC_ALL, "ru-ru.UTF-8")

alphabetRus = "абвгдеёжзийклмнопрстуфхцчшщъьыэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЫЭЮЯ"
alphabetRusLower = "абвгдеёжзийклмнопрстуфхцчшщъьыэюя"


def clean(prm, mode=()):
    if mode:
        mode[0].lower()
    if mode == "lite":
        strng = r"^|\n|\r|$"
    elif mode == "strong":
        strng = r"^\s+|\n|\r|[^0-9a-zA-Z -" + alphabetRus + r"\"]|\s+$"
    elif mode == "strong_eng":
        strng = r"^\s+|\n|\r|[^0-9 a-zA-Z_]|\s+$"
    elif mode == "path":
        strng = r"^\s+|\n|\r|[^0-9a-zA-Z -" + alphabetRus + r"\\\/:\\(\\).]|\s+$"
    else:
        strng = r"^\s+|\n|\r|\s+$"

    prm = re.sub(strng, '', prm).lower()
    prm = re.sub(r"\s+", " ", prm).lower()
    prm = re.sub(r"^\s+|\s+$", '', prm).lower()

    return prm


def repl(text):
    text = text.replace("▪", "-")
    text = text.replace("•", "-")
    text = text.replace("▪️", "-")
    return text


# Generate Word's variants
# word = "api" => " api", "api ", " api ", ".api", "api."...
# Concatenate word + signs

def words_gen(*words):
    signs = r".,:;-?!()[]\'’ "

    genwords = []
    for i in words:
        for sr in signs:
            for sl in signs:
                genwords.extend([sl+i+sr])
                genwords.extend([i + sr])
                genwords.extend([sl + i])
    return list(set(genwords))  # deduplicate... just in case


# --- Write <keyword>word[<advsearch>]<tag>tag1</tag></keyword> into "tagsfile" ---
def add_keytags():
    try:
        print("\nSample1:  keyword = [+] tag1 tag2...tagN")
        print("Sample2:  keyword1 (new keyword2)...keywordN = [+] tags_abbr tag1 tag2")
        print("\nkeyword1 (new keyword2)...keywordN - sequence of keywords")
        print("(new keyword2) - one keyword")
        print("'=' - separator")
        print("[+] - Advanced search (optional parameter)")
        print("\ntags_abbr - Tag abbreviations:")
        print("dev_tags - development")
        print("des_tags - design")
        print("biz_tags - business")
        print("traff_tags - traffic")
        print("trav_tags - travels, rest")
        print("office_tags - office")
        print("webdes_tags - web-design")
        print("\nSample: бот (два бота) боту ботом (о боте) = + dev_tags боты")
        print("Sample: дизайн = des_tags")

        new_keytags_input = input().lower()
        if new_keytags_input != "":
            new_keytags_input = clean(new_keytags_input)
            new_keytags_input = re.sub("[^-=_ a-zA-Z0-9\\+\\(\\)"+alphabetRus+"]", "", new_keytags_input)
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
                    adv_search = "<advsearch>"
                    anchorpoint = new_keytags_input.find("+")
                else:
                    adv_search = ""

                # 4. tag abbreviations?
                abbr_tags = ""
                tag_abbr = ["dev_tags", "des_tags", "traff_tags", "office_tags", "webdes_tags"]
                for tg in tag_abbr:
                    if new_keytags_input.find(tg) > anchorpoint:
                        if tg == "dev_tags":
                            abbr_tags += "<tag>dev</tag><tag>программирование</tag><tag>разработка</tag>"
                        if tg == "des_tags":
                            abbr_tags += "<tag>design</tag><tag>дизайн</tag>"
                        if tg == "traff_tags":
                            abbr_tags += "<tag>трафик</tag><tag>арбитраж</tag>"
                        if tg == "office_tags":
                            abbr_tags += "<tag>office</tag><tag>офис</tag>"
                        if tg == "webdes_tags":
                            abbr_tags += "<tag>webdesign</tag><tag>вебдизайн</tag><tag>вэбдизайн</tag>"
                        anchorpoint += len(tg) + 1   # abbr_tags + space

                # 5. other tags
                other_tags = ""
                if anchorpoint > 0:
                    otrtags = new_keytags_input[anchorpoint+1:].split(" ")
                    otrtags = list(filter(None, otrtags))
                    for ot in otrtags:
                        other_tags += "<tag>" + re.sub("[^a-z0-9"+alphabetRusLower+"]", "", ot) + "</tag>"

                # 6. assemble string
                astring = ""
                for kwd in keywords:
                    astring += "<keyword>" + kwd + adv_search + abbr_tags + other_tags + "</keyword>\n"

                # confirm data...
                try:
                    inp = input("\nAre you want to add\n\n{0}\nto the tags file? [y/n]".format(astring))
                    inp = re.sub("^yY", "", inp)
                    if inp != '':

                        # ...and check of existence
                        try:
                            with open(r"c:\Projects\hw\tagsfile", "a+", encoding="utf-8") as tfile:
                                for line in tfile:
                                    if line != "":
                                        keyw = line[0:line.find("<tag>")]
                                        keyw = keyw.replace("<advsearch>", "")

                                        if astring.find(keyw):
                                            print("Sorry, this tag '{0}' yet exist.".format(keyw.replace("<keyword>", "")))
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
