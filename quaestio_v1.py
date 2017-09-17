import requests, urllib, sys
import random

if __name__ == "__main__":
    url = "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2017-02-27&"
    
    text = ""

    # Reads first command line argument as filename
    f = open(sys.argv[1], "r")
    for line in f:
        text += line.strip() + " "
    f.close()
    print(text)

    features = "keywords,semantic_roles"

    data = {"text": text, "features": features}

    data = urllib.parse.urlencode(data)

    r = requests.get(url+data, auth=("2ce5f314-7f6c-4ee5-a599-74847c51d534","8NIIaWCN3PiW"))
    
    
    questions = {}
    # Grammar Questions
    for role in r.json()['semantic_roles']:
        print(role.keys())
        for item in role.keys():
            if (item == "sentence"):
                continue
            question = "What is the " + item + " in the sentence: " + role["sentence"]
            # print(role["sentence"], role)
            answer = "The answer is " + role[item]["text"] + "."
            questions[question] = answer

    #   

    for question in questions.keys():  
        print("Q: " + question, "\nA: " + questions[question])
