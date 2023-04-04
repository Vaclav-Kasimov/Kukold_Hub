import json, random
def make_complmient(name):
    with open('compliments.json', 'r') as compliments:
        compliments_list = json.load(compliments)
    compliment = compliments_list.get(str(random.randint(1,50)))
    return compliment.replace("[name]", name)
print(make_complmient('Наташа'))