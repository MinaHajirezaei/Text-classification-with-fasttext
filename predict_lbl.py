
import emoji
import re
import fasttext

category_ref = {1: {"category": 'arts_media'},
                2: {"category": 'culture'},
                3: {"category": 'economy'},
                4: {"category": 'politics'},
                5: {"category": 'scientific_academic'},
                6: {"category": 'sports'},
                }

alphabets_regex = {
                    'ا':r'اَ|اِ|اُ|اٌ|اٍ|اً|أ|إ',
                    'آ':r'آ',
                    'ب':r'بَ|بِ|بُ|بّ',
                    'پ':r'پَ|پِ|پُ',
                    'ت':r'تَ|تِ|تُ|تّ',
                    'ث':r'ثَ|ثِ|ثُ',
                    'ج':r'جَ|جِ|جُ|جّ',
                    'چ':r'چَ|چِ|چُ|چّ',
                    'ح':r'حَ|حِ|حُ',
                    'خ':r'خَ|خِ|خُ',
                    'د':r'دَ|دِ|دُ|دّ',
                    'ذ':r'ذَ|‌ذِ|ذُ',
                    'ر':r'رَ|رِ|رُ|رّ',
                    'ز':r'زَ|زِ|زُ|زّ',
                    'ژ':r'ژَ|ژِ|ژُ',
                    'س':r'سَ|سِ|سُ|سّ',
                    'ش':r'شَ|شِ|شُ',
                    'ص':r'صَ|صِ|صُ',
                    'ض':r'ضَ|ضِ|ضُ',
                    'ط':r'طَ|طِ|طُ',
                    'ظ':r'ظَ|ظِ|ظُ',
                    'ع':r'عَ|عِ|عُ',
                    'غ':r'غَ|غِ|غُ',
                    'ف':r'فَ|فِ|فُ|فّ',
                    'ق':r'قَ|قِ|قُ|قّ',
                    'ک':r'کَ|کِ|کُ|ك|كَ|كِ|كُ|کّ|كّ',
                    'گ':r'گَ|گِ|گُ',
                    'ل':r'لَ|لِ|لُ|لّ',
                    'م':r'مَ|مِ|مُ',
                    'ن':r'نَ|نِ|نُ|نّ',
                    'و':r'وَ|وِ|وُ|ؤ|ؤَ|ؤُ|ؤِ|وّ|ؤّ',
                    'ه':r'هَ|هِ|هُ|ة',
                    'ی':r'یَ|یِ|یُ|ي|يَ|يِ|يُ|يّ|یّ',
                    'ئ':r'ئَ|ئِ|ئُ|ئّ'
                   }

def unifing_alphabets(text):
    text = re.sub(alphabets_regex['ا'], 'ا', text)
    text = re.sub(alphabets_regex['ب'], 'ب', text)
    text = re.sub(alphabets_regex['پ'], 'پ', text)
    text = re.sub(alphabets_regex['ت'], 'ت', text)
    text = re.sub(alphabets_regex['ث'], 'ث', text)
    text = re.sub(alphabets_regex['ج'], 'ج', text)
    text = re.sub(alphabets_regex['چ'], 'چ', text)
    text = re.sub(alphabets_regex['ح'], 'ح', text)
    text = re.sub(alphabets_regex['خ'], 'خ', text)
    text = re.sub(alphabets_regex['د'], 'د', text)
    text = re.sub(alphabets_regex['ذ'], 'ذ', text)
    text = re.sub(alphabets_regex['ر'], 'ر', text)
    text = re.sub(alphabets_regex['ز'], 'ز', text)
    text = re.sub(alphabets_regex['ژ'], 'ژ', text)
    text = re.sub(alphabets_regex['س'], 'س', text)
    text = re.sub(alphabets_regex['ش'], 'ش', text)
    text = re.sub(alphabets_regex['ص'], 'ص', text)
    text = re.sub(alphabets_regex['ض'], 'ض', text)
    text = re.sub(alphabets_regex['ط'], 'ط', text)
    text = re.sub(alphabets_regex['ظ'], 'ظ', text)
    text = re.sub(alphabets_regex['ع'], 'ع', text)
    text = re.sub(alphabets_regex['غ'], 'غ', text)
    text = re.sub(alphabets_regex['ف'], 'ف', text)
    text = re.sub(alphabets_regex['ق'], 'ق', text)
    text = re.sub(alphabets_regex['ک'], 'ک', text)
    text = re.sub(alphabets_regex['گ'], 'گ', text)
    text = re.sub(alphabets_regex['ل'], 'ل', text)
    text = re.sub(alphabets_regex['م'], 'م', text)
    text = re.sub(alphabets_regex['ن'], 'ن', text)
    text = re.sub(alphabets_regex['و'], 'و', text)
    text = re.sub(alphabets_regex['ه'], 'ه', text)
    text = re.sub(alphabets_regex['ی'], 'ی', text)
    text = re.sub(alphabets_regex['ئ'], 'ئ', text)
    return text

def remove_extra_chars(text):
    # if url exists in the text
    url_pattern = r"(?:(?:https?):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"
    if re.findall(url_pattern, text, re.IGNORECASE):
        text = re.sub(url_pattern,"",text)

    # if username exists in the text
    if re.findall(r"@(\w+[.]*\b)", text):
        text = re.sub(r"@(\w+[.]*\b)","",text)

    regex = re.compile('[%s]' % re.escape(':"#$&\'()*+-/<=>@[\\]^_`{|}~>>?؟!,،.;'))
    text = regex.sub(' ', text)

    # unifying all alphabets in the text
    text = unifing_alphabets(text)

    #remove number from text
    text = re.sub(r'\d+', '', text)

    # remove duplicate letters
    duplicate_letter_pattern = re.compile(r"(.)\1{2,}")
    text = duplicate_letter_pattern.sub(r"\1", text)

    #remove emoji
    for ch in text:
        if ch in emoji.UNICODE_EMOJI:
            text = text.replace(ch, "")

    #remove all characters other than persian characters
    for ch in text:
        if ch not in alphabets_regex.keys():
            text = text.replace(ch, " ")

    text = (" ").join([word.strip() for word in text.split()])
    return text

#load 7 model for to category = (7 label and sublabels )
fasttext_model1 = fasttext.load_model("fastai_7lbl.ftz")
fasttext_model2 = fasttext.load_model("art_media.ftz")
fasttext_model3 = fasttext.load_model("culture.ftz")
fasttext_model4 = fasttext.load_model("economy.ftz")
fasttext_model5 = fasttext.load_model("politics.ftz")
fasttext_model6 = fasttext.load_model("scientific_academic.ftz")
fasttext_model7 = fasttext.load_model("sports.ftz")
fasttext_model8 = fasttext.load_model("social.ftz")



label1 = ""
label2 = ""

def artmedia_model(text):
    output2 = fasttext_model2.predict(text)
    if output2[0][0] == "__label__6":
        label2 = "cinema"
    elif output2[0][0] == "__label__35":
        label2 = "radio-tv"
    elif output2[0][0] == "__label__27":
        label2 = "music"
    else:
        label2 = "media"
    return (label2)


def culture_model(text):
    output3 = fasttext_model3.predict(text)
    if output3[0][0] == "__label__29":
        label2 = "others_culture"
    elif output3[0][0] == "__label__38":
        label2 = "thought"
    elif output3[0][0] == "__label__34":
        label2 = "quran"
    elif output3[0][0] == "__label__26":
        label2 = "mosque"
    elif output3[0][0] == "__label__18":
        label2 = "history"
    elif output3[0][0] == "__label__17":
        label2 = "hajj-pilgrimage-waqf"
    elif output3[0][0] == "__label__15":
        label2 = "general-culture"
    else:
        label2 = "book"
    return (label2)

def economy_model(text):
    output4 = fasttext_model4.predict(text)
    if output4[0][0] == "__label__5":
        label2 = "business"
    elif output4[0][0] == "__label__37":
        label2 = "stock"
    elif output4[0][0] == "__label__23":
        label2 = "macroeconomics"
    elif output4[0][0] == "__label__12":
        label2 = "energy"
    elif output4[0][0] == "__label__7":
        label2 = "civil"
    elif output4[0][0] == "__label__3":
        label2 = "banking"
    elif output4[0][0] == "__label__1":
        label2 = "agriculture"
    elif output4[0][0] == "__label__41":
        label2 = "world-economy"
    elif output4[0][0] == "__label__10":
        label2 = "economic-warfare"
    elif output4[0][0] == "__label__28":
        label2 = "occupation"
    else:
        label2 = "companies-news"
    return (label2)

def politics_model(text):
    output5 = fasttext_model5.predict(text)
    if output5[0][0] == "__label__33":
        label2 = "parliament"
    elif output5[0][0] == "__label__16":
        label2 = "government"
    elif output5[0][0] == "__label__0":
        label2 = "academic-formations"
    elif output5[0][0] == "__label__30":
        label2 = "others_politics"
    elif output5[0][0] == "__label__44":
        label2 = "Partiess"
    elif output5[0][0] == "__label__45":
        label2 = "Defense"
    else:
        label2 = "Leadership"
    return (label2)


def scientific_model(text):
    output6 = fasttext_model6.predict(text)
    if output6[0][0] == "__label__36":
        label2 = "research"
    elif output6[0][0] == "__label__21":
        label2 = "knowledge"
    elif output6[0][0] == "__label__19":
        label2 = "iran-science"
    elif output6[0][0] == "__label__11":
        label2 = "education"
    elif output6[0][0] == "__label__31":
        label2 = "others_scientific_academic"
    elif output6[0][0] == "__label__42":
        label2 = "world-science"
    elif output6[0][0] == "__label__20":
        label2 = "IT"
    else:
        label2 = "culture"
    return (label2)

def sports_model(text):
    output7 = fasttext_model7.predict(text)
    if output7[0][0] == "__label__13":
        label2 = "football-iran"
    elif output7[0][0] == "__label__14":
        label2 = "football-world"
    elif output7[0][0] == "__label__24":
        label2 = "martial-arts"
    elif output7[0][0] == "__label__2":
        label2 = "ballgames"
    elif output7[0][0] == "__label__32":
        label2 = "others_sports"
    elif output7[0][0] == "__label__39":
        label2 = "women"
    elif output7[0][0] == "__label__40":
        label2 = "world"
    else:
        label2 = "wrestling-powerlifting"
    return (label2)


def social_model(text):
    output8 = fasttext_model8.predict(text)
    if output8[0][0] == "__label__47":
        label2 = "Welfare_social_harms"
    elif output8[0][0] == "__label__48":
        label2 = "Health"
    elif output8[0][0] == "__label__49":
        label2 = "Disciplinary_incidents"
    elif output8[0][0] == "__label__50":
        label2 = "Civic"
    elif output8[0][0] == "__label__51":
        label2 = "Legal and judicial"
    elif output8[0][0] == "__label__52":
        label2 = "Education"
    elif output8[0][0] == "__label__53":
        label2 = "Socialـresponsibilities"
    elif output8[0][0] == "__label__54":
        label2 = "Others"
    elif output8[0][0] == "__label__55":
        label2 = "Environment_Tourism"
    elif output8[0][0] == "__label__56":
        label2 = "Womenـyouth"
    else:
        label2 = "Tavankhahـgroups"

    return (label2)


def predict_with_improved_ai_model(text):
    z = remove_extra_chars(sentence)
    output1 = fasttext_model1.predict(z)
    if output1[0][0] == "__label__1":
        label1 = "arts_media"
        m = artmedia_model(z)

    elif output1[0][0] == "__label__2":
        label1 = "culture"
        m = culture_model(z)

    elif output1[0][0] == "__label__3":
        label1 = "economy"
        m = economy_model(z)

    elif output1[0][0] == "__label__4":
        label1 = "politics"
        m=politics_model(z)

    elif output1[0][0] == "__label__5":
        label1 = "scientific_academic"
        m = scientific_model(z)

    elif output1[0][0] == "__label__6":
        label1 = "sports"
        m = sports_model(z)

    else:
        label1 = "social"
        m = social_model(z)

    return (label1, m)



    
if __name__ == "__main__":
    sentence = (input("please enter a sentence for predict class:"))
    cat1, cat2 = predict_with_improved_ai_model(sentence)
    print("category1:", cat1)
    print("category2: ", cat2)
    

