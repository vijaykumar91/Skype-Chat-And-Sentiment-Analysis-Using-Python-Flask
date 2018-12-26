from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analysis=TextBlob("happy sad happy best good  bad ugly sorry screens are scrollable with bouncing when reaching to the top and the bottom of the list. These screens are Discover, Device List, and all Customization screens")

print(analysis.tags)
print(analysis.sentiment)

sentences = ["I expect the all the list-based screens are scrollable with bouncing when reaching to the top and the bottom of the list. These screens are Discover, Device List, and all Customization screens.",  # positive sentence example
             "VADER is smart, handsome, and funny!",  # punctuation emphasis handled correctly (sentiment intensity adjusted)
             "VADER is very smart, handsome, and funny.", # booster words handled correctly (sentiment intensity adjusted)
             "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
             "VADER is VERY SMART, handsome, and FUNNY!!!", # combination of signals - VADER appropriately adjusts intensity
             "VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!", # booster words & punctuation make this close to ceiling for score
             "VADER is not smart, handsome, nor funny.",  # negation sentence example
             "The book was good.",  # positive sentence
             "At least it isn't a horrible book.",  # negated negative sentence with contraction
             "The book was only kind of good.", # qualified positive sentence is handled correctly (intensity adjusted)
             "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
             "Today SUX!",  # negative slang with capitalization emphasis
             "Today only kinda sux! But I'll get by, lol", # mixed sentiment example with slang and constrastive conjunction "but"
             "Make sure you :) or :D today!",  # emoticons handled
             "Catch utf-8 emoji such as such as 💘 and 💋 and 😁",  # emojis handled
             "Not bad at all"  # Capitalized negation
             ]
analyzer = SentimentIntensityAnalyzer()
analysisArr=[]
for sentence in sentences:
    vs = analyzer.polarity_scores(sentence)
    neg=str(vs).split(",")[0]
    compund=str(vs).split(",")[3]
    neg = neg.replace("{", "")
    neg=neg.replace("'", '"')
    compund=compund.replace("}", "")
    compund = compund.replace("'", '"')
    neu=str(vs).split(",")[1]
    neu=neu.replace("'", '"')
    pos=str(vs).split(",")[2]
    pos = pos.replace("'", '"')

    neg =neg.split(":")[1]
    neu = neu.split(":")[1]
    pos = pos.split(":")[1]
    compund = compund.split(":")[1]
    print(neg)
    print(neu)
    print(pos)
    print(compund)
    #print("{:-<65} {}".format(sentence, str(vs)))