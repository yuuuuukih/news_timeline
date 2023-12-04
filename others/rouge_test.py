from sumeval.metrics.rouge import RougeCalculator

alpha = 0.8

story = "As Russia pulls back forces from Ukraine's Kharkiv region, tensions remain high. The Biden administration confirms that Russia has purchased rockets from North Korea, while Ukraine reports approximately 9,000 troop losses. Amidst the turmoil, Russia's intent to annex large portions of Eastern Ukraine has been exposed. Ukraine's President Zelenskyy warns that his country may only be the beginning. As Russia targets Ukraine's industrial heartland, global response ramps up with Joe Biden approving $800 million in military aid. Despite the grim situation, Ukraine stands resilient, refusing to surrender its lands and remaining hopeful that Russia's strategy will ultimately fail."

docs_bad_list = [
    "Russia Launches Fight For Industrial Heartland, Ukraine Says",
    "Moscow has declared the capture of the Donbas to be its main goal in the war since its attempt to seize the capital, Kyiv, failed.",
    "Russia Plans To Annex Much Of Eastern Ukraine, Senior U.S. Official Says",
    "Such a move would not be recognized by the U.S. or its allies, Michael Carpenter, U.S. ambassador to the Organization for Security and Cooperation in Europe, said.",
    "Ukraine: 9,000 Of Its Troops Killed Since Russia Began War",
    "The Russian invasion of Ukraine began on Feb. 24.",
    "U.S.: Russia To Buy Rockets, Artillery Shells From North Korea",
    "The finding comes after the Biden administration confirmed that the Russian military in August took delivery of Iranian-manufactured drones for use in Ukraine.",
    "Russia Says It's Pulling Back Forces From Ukraine's Kharkiv Region",
    "Russia’s Defense Ministry announced that troops will be pulled back in two area where a Ukrainian counter offensive has made significant advances.",
]

docs_half_good_list = [
    "Russia Launches Fight For Industrial Heartland, Ukraine Says",
    "Moscow has declared the capture of the Donbas to be its main goal in the war since its attempt to seize the capital, Kyiv, failed.",
    "Russia Plans To Annex Much Of Eastern Ukraine, Senior U.S. Official Says",
    "Such a move would not be recognized by the U.S. or its allies, Michael Carpenter, U.S. ambassador to the Organization for Security and Cooperation in Europe, said.",
    "Ukraine: 9,000 Of Its Troops Killed Since Russia Began War",
    "The Russian invasion of Ukraine began on Feb. 24.",
    "U.S.: Russia To Buy Rockets, Artillery Shells From North Korea",
    "The finding comes after the Biden administration confirmed that the Russian military in August took delivery of Iranian-manufactured drones for use in Ukraine.",
    "Russia Says It's Pulling Back Forces From Ukraine's Kharkiv Region",
    "Russia’s Defense Ministry announced that troops will be pulled back in two area where a Ukrainian counter offensive has made significant advances.",
    "Joe Biden Approves $800 Million In New Military Aid For Ukraine",
    "As Russia prepares a major offensive in eastern Ukraine, the government in Kyiv says it needs more support from international partners in its efforts to resist."
]

docs_good_list = [
    "Russia Launches Fight For Industrial Heartland, Ukraine Says",
    "Moscow has declared the capture of the Donbas to be its main goal in the war since its attempt to seize the capital, Kyiv, failed.",
    "Russia Plans To Annex Much Of Eastern Ukraine, Senior U.S. Official Says",
    "Such a move would not be recognized by the U.S. or its allies, Michael Carpenter, U.S. ambassador to the Organization for Security and Cooperation in Europe, said.",
    "Ukraine: 9,000 Of Its Troops Killed Since Russia Began War",
    "The Russian invasion of Ukraine began on Feb. 24.",
    "U.S.: Russia To Buy Rockets, Artillery Shells From North Korea",
    "The finding comes after the Biden administration confirmed that the Russian military in August took delivery of Iranian-manufactured drones for use in Ukraine.",
    "Russia Says It's Pulling Back Forces From Ukraine's Kharkiv Region",
    "Russia’s Defense Ministry announced that troops will be pulled back in two area where a Ukrainian counter offensive has made significant advances.",
    "Joe Biden Approves $800 Million In New Military Aid For Ukraine",
    "As Russia prepares a major offensive in eastern Ukraine, the government in Kyiv says it needs more support from international partners in its efforts to resist.",
    "Volodymyr Zelenskyy Warns That Ukraine Is Just The Beginning For Russia",
    "“The want to capture other countries. ... We are the first in line. Who will come next?” Zelenskyy asked in his daily address.",
]


rouge = RougeCalculator(stopwords=True, lang="en")

docs_bad = " ".join(docs_bad_list)
docs_half_good = " ".join(docs_half_good_list)
docs_good = " ".join(docs_good_list)


print("=======")

rouge_1 = rouge.rouge_n(
            summary=story,
            references=docs_bad,
            n=1, alpha=alpha)

rouge_2 = rouge.rouge_n(
            summary=story,
            references=docs_bad,
            n=2, alpha=alpha)

rouge_l = rouge.rouge_l(
            summary=story,
            references=docs_bad, alpha=alpha)

print("ROUGE-1: {}, ROUGE-2: {}, ROUGE-L: {}".format(
    rouge_1, rouge_2, rouge_l
).replace(", ", "\n"))

print("=======")

rouge_1 = rouge.rouge_n(
            summary=story,
            references=docs_half_good,
            n=1, alpha=alpha)

rouge_2 = rouge.rouge_n(
            summary=story,
            references=docs_half_good,
            n=2, alpha=alpha)

rouge_l = rouge.rouge_l(
            summary=story,
            references=docs_half_good, alpha=alpha)

print("ROUGE-1: {}, ROUGE-2: {}, ROUGE-L: {}".format(
    rouge_1, rouge_2, rouge_l
).replace(", ", "\n"))

print("=======")

rouge_1 = rouge.rouge_n(
            summary=story,
            references=docs_good,
            n=1, alpha=alpha)

rouge_2 = rouge.rouge_n(
            summary=story,
            references=docs_good,
            n=2, alpha=alpha)

rouge_l = rouge.rouge_l(
            summary=story,
            references=docs_good, alpha=alpha)

print("ROUGE-1: {}, ROUGE-2: {}, ROUGE-L: {}".format(
    rouge_1, rouge_2, rouge_l
).replace(", ", "\n"))

"""
TH
alpha=0.8
rouge-1: 0.4
rouge-2: 0.16
rouge-l: 0.20

alpha=1
rouge-1: 0.45
rouge-2: 0.18
rouge-l: 0.24

rouge-1: 0.25(alpha-0.8)+0.40
rouge-2: 0.10(alpha-0.8)+0.16
rouge-l: 0.20(alpha-0.8)+0.20

妥協案
alpha=0.8
rouge-1: 0.25
rouge-2: 0.12
rouge-l: 0.15

RESULTS
alpha = 0.8
=======
ROUGE-1: 0.36684782608695654
ROUGE-2: 0.12396694214876033
ROUGE-L: 0.1766304347826087
=======
ROUGE-1: 0.41131105398457585
ROUGE-2: 0.16927083333333334
ROUGE-L: 0.2442159383033419
=======
ROUGE-1: 0.43424317617866004
ROUGE-2: 0.1884422110552764
ROUGE-L: 0.2357320099255583

alpha = 1
=======
ROUGE-1: 0.34177215189873417
ROUGE-2: 0.11538461538461538
ROUGE-L: 0.16455696202531647
=======
ROUGE-1: 0.3575418994413408
ROUGE-2: 0.14689265536723164
ROUGE-L: 0.2122905027932961
=======
ROUGE-1: 0.3626943005181347
ROUGE-2: 0.15706806282722513
ROUGE-L: 0.19689119170984454

memo
referenceはリストでも渡せるが、リストで渡すとスコアが下がる。(alpha>=0.5)
"""

# For rate
print('=== For rate ===')
scores = []
for i in range(8):
    docs = " ".join(docs_good_list[0:2*(i)])
    print(f"{i} docs")
    rouge_2 = rouge.rouge_n(summary=story, references=docs, n=2, alpha=0.8)
    scores.append(rouge_2)
    try:
        rate = scores[i] / scores[i-1]
    except ZeroDivisionError as e:
        rate = 0
    print(f"score: {scores[i]}")
    print(f"rate: {rate}")

"""
TH for rate of rouge-2
1.1
"""