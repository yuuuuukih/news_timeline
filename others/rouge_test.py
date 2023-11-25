from sumeval.metrics.rouge import RougeCalculator

russia_ukraine_id  = 236

story = "As Russia pulls back forces from Ukraine's Kharkiv region, tensions remain high. The Biden administration confirms that Russia has purchased rockets from North Korea, while Ukraine reports approximately 9,000 troop losses. Amidst the turmoil, Russia's intent to annex large portions of Eastern Ukraine has been exposed. Ukraine's President Zelenskyy warns that his country may only be the beginning. As Russia targets Ukraine's industrial heartland, global response ramps up with Joe Biden approving $800 million in military aid. Despite the grim situation, Ukraine stands resilient, refusing to surrender its lands and remaining hopeful that Russia's strategy will ultimately fail.",

docs_bad = [
    "Russia Launches Fight For Industrial Heartland, Ukraine Says",
    "Moscow has declared the capture of the Donbas to be its main goal in the war since its attempt to seize the capital, Kyiv, failed.",
    "Russia Plans To Annex Much Of Eastern Ukraine, Senior U.S. Official Says",
    "Such a move would not be recognized by the U.S. or its allies, Michael Carpenter, U.S. ambassador to the Organization for Security and Cooperation in Europe, said.",
    "Ukraine: 9,000 Of Its Troops Killed Since Russia Began War",
    "The Russian invasion of Ukraine began on Feb. 24.",
    "Russia Says It's Pulling Back Forces From Ukraine's Kharkiv Region",
    "Russia’s Defense Ministry announced that troops will be pulled back in two area where a Ukrainian counter offensive has made significant advances.",
]

docs_good = [
    "Russia Launches Fight For Industrial Heartland, Ukraine Says",
    "Moscow has declared the capture of the Donbas to be its main goal in the war since its attempt to seize the capital, Kyiv, failed.",
    "Russia Plans To Annex Much Of Eastern Ukraine, Senior U.S. Official Says",
    "Such a move would not be recognized by the U.S. or its allies, Michael Carpenter, U.S. ambassador to the Organization for Security and Cooperation in Europe, said.",
    "Ukraine: 9,000 Of Its Troops Killed Since Russia Began War",
    "The Russian invasion of Ukraine began on Feb. 24.",
    "Russia Says It's Pulling Back Forces From Ukraine's Kharkiv Region",
    "Russia’s Defense Ministry announced that troops will be pulled back in two area where a Ukrainian counter offensive has made significant advances.",
    "Joe Biden Approves $800 Million In New Military Aid For Ukraine",
    "As Russia prepares a major offensive in eastern Ukraine, the government in Kyiv says it needs more support from international partners in its efforts to resist.",
    "Volodymyr Zelenskyy Warns That Ukraine Is Just The Beginning For Russia",
    "“The want to capture other countries. ... We are the first in line. Who will come next?” Zelenskyy asked in his daily address.",
]


rouge = RougeCalculator(stopwords=True, lang="en")

docs_bad = " ".join(docs_bad)
docs_good = " ".join(docs_good)

rouge_1 = rouge.rouge_n(
            summary=docs_bad,
            references=story,
            n=1)

rouge_2 = rouge.rouge_n(
            summary=docs_bad,
            references=story,
            n=2)

rouge_l = rouge.rouge_l(
            summary=docs_bad,
            references=story)

print("ROUGE-1: {}, ROUGE-2: {}, ROUGE-L: {}".format(
    rouge_1, rouge_2, rouge_l
).replace(", ", "\n"))

rouge_1 = rouge.rouge_n(
            summary=docs_good,
            references=story,
            n=1)

rouge_2 = rouge.rouge_n(
            summary=docs_good,
            references=story,
            n=2)

rouge_l = rouge.rouge_l(
            summary=docs_good,
            references=story)

print("ROUGE-1: {}, ROUGE-2: {}, ROUGE-L: {}".format(
    rouge_1, rouge_2, rouge_l
).replace(", ", "\n"))

"""
TH
rouge-1: 0.32
rouge-2: 0.15
rouge-l: 0.20
"""