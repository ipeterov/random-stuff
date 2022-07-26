import csv
from collections import defaultdict

import matplotlib.pyplot as plt


with open("approval_polls.csv", "r") as f:
    reader = csv.DictReader(f)
    polls = list(reader)


presidents = defaultdict(
    lambda: {
        "max_approval": 0,
        "min_approval": 100,
        "max_disapproval": 0,
        "min_disapproval": 100,
        "starting_approval": [None, 700],
        "starting_disapproval": [None, 700],
        "ending_approval": [None, 0],
        "ending_disapproval": [None, 0],
    }
)

for poll in polls:
    president = poll["President"]
    approve = float(poll["Approve"])
    disapprove = float(poll["Disapprove"])
    day = int(poll["Days"])

    if day > 539:
        continue

    if approve < presidents[president]["min_approval"]:
        presidents[president]["min_approval"] = approve

    if approve > presidents[president]["max_approval"]:
        presidents[president]["max_approval"] = approve

    if disapprove < presidents[president]["min_disapproval"]:
        presidents[president]["min_disapproval"] = disapprove

    if disapprove > presidents[president]["max_disapproval"]:
        presidents[president]["max_disapproval"] = disapprove

    if day < presidents[president]["starting_approval"][1]:
        presidents[president]["starting_approval"] = [approve, day]

    if day < presidents[president]["starting_disapproval"][1]:
        presidents[president]["starting_disapproval"] = [disapprove, day]

    if day > presidents[president]["ending_approval"][1]:
        presidents[president]["ending_approval"] = [approve, day]

    if day > presidents[president]["ending_disapproval"][1]:
        presidents[president]["ending_disapproval"] = [disapprove, day]


for president in presidents:
    data = presidents[president]
    data["half_term_delta"] = data["ending_approval"][0] - data["starting_approval"][0]
    data["half_term_disapp_delta"] = (
        data["ending_disapproval"][0] - data["starting_disapproval"][0]
    )

graphs = defaultdict(list)
for poll in polls:
    president = poll["President"]
    approve = float(poll["Approve"])
    day = int(poll["Days"])
    graphs[president].append([day, approve])

for president in graphs:
    graphs[president].sort(key=lambda x: x[0])
    plt.plot(*zip(*graphs[president]), label=president)

plt.legend()
plt.show()

# for president, data in sorted(
#     presidents.items(),
#     key=lambda item: item[1]["min_approval"],
# ):
#     print(f"| {president} | {data['min_approval']} | {data['max_disapproval']} |")

# for president, data in sorted(
#     presidents.items(),
#     key=lambda item: item[1]["half_term_delta"],
# ):
#     print(
#         f"| {president} | {data['half_term_delta']:+.1f} | {data['half_term_disapp_delta']:+.1f} |"
#     )
