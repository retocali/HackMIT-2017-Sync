import requests, urllib, sys
import random
import csv

if __name__ == "__main__":
    url = "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2017-02-27&"

    # parse first command as type of input
    
    if (sys.argv[1] == "-f"): # Takes a filename
        text = ""

        # Reads first command line argument as filename
        f = open(sys.argv[2], "r")
        for line in f:
            text += line.strip() + " "
        f.close()
    elif (sys.argv[1] == "-t"): # Takes text
        text = sys.argv[2]
    
    #print(text)


    features = "keywords,semantic_roles,emotion,relations,entities"

    data = {"text": text, "features": features}

    data = urllib.parse.urlencode(data)

    r = requests.get(url+data, auth=("2ce5f314-7f6c-4ee5-a599-74847c51d534","8NIIaWCN3PiW"))
    
    
    questions = {}
    
    # Grammar Questions
    for role in r.json()['semantic_roles']:
        for item in role.keys():
            if (item == "sentence"):
                continue
            if (item == "action" and role[item].get("verb", "") != ""):
                tense_question = "What is the tense of the word " + role[item]["text"] + " in the sentence: " + role["sentence"]
                tense_answer = "The answer is " + role[item]["verb"]["tense"] + "."
                questions[tense_question] = (tense_answer, "Tense")
            question = "What is the " + item + " in the sentence: " + role["sentence"]
            answer = "The answer is " + role[item]["text"] + "."
            questions[question] = (answer, "Grammar")

    # Emotions Questions
    sadness = ["It was sad.", "The piece was sad.", "The tone was sad."]
    fear = ["It was scary.", "The piece was scary.", "The tone was scary."]
    angry = ["It was frustrating.", "The piece was frustrating.", "The tone was frustration."]
    joy = ["It was happy.", "The piece was happy.", "The tone was happy."]  
    disgust = ["It was disgusting.", "The piece was disgusting."]

    emotions = {"sadness": sadness, "fear": fear, "angry": angry, "joy": joy, "disgust": disgust}

    emotion_question = "What is the tone of the piece?"
    
    # Finds the max emotion
    e = (r.json()["emotion"]["document"]["emotion"])
    emotion = max(e.keys(), key=lambda x: e[x])
    
    emotion_answer = emotions[emotion][random.randint(0, len(emotions[emotion])-1)]

    questions[emotion_question] = (emotion_answer, "Tone")

    # Relations Questions
    def relation_parser(relation):
        action = ""
        for c in relation["type"]:
            if (c.upper() == c):
                action += " "
            action += c.lower()
        
        actor = relation["arguments"][0]["text"]
        direct_object = relation["arguments"][1]["text"]
        return action, actor, direct_object
    
    relations = r.json()["relations"]
    #print(relations)

    min_confidence = 0.51

    # Type of question
    b = "Fill in the blank"

    for x in range(0, len(relations)):
        relation = relations[x]
        if (relation["score"] < min_confidence):
            continue
        
        action, actor, direct_object = relation_parser(relation)

        # Deals with relations in pairs
        if (action == "affected by" or action == "agent of"):
            try:
                next_relation = relations[x+1]
                
                n_action, n_actor, n_direct_object = relation_parser(next_relation)
                
                #print("Pair:",relation, next_relation)
                #print(direct_object, n_direct_object)
                # print("S:",set([action, n_action]))
                if (direct_object == n_direct_object and len(set([action, n_action])) == 2):
                    answer = actor + " " + direct_object + " " + n_actor
                    
                    question = "Fill in the blank: " + actor + " " + direct_object + " " + "____"
                    questions[question] = (answer, b)
                    
                    question = "Fill in the blank: " + "____" + " " + direct_object + " " + n_actor
                    questions[question] = (answer, b)
            except:
                continue;
        else:
            # single relations
            answer = actor + " " + action + " " + direct_object

            question = "Fill in the blank: " + actor + " " + action + " " + "____"
            questions[question] = (answer, b)

            question = "Fill in the blank: " + "____" + " " + action + " " + direct_object
            questions[question] = (answer, b)

    # Location Questions



    for question in questions.keys():  
        # pass
        print("Q: " + question, "<br>", '<div id="spoiler" style="display:none">',"A: " + questions[question][0],'''
        </div><button title="Click to show/hide content" type="button" onclick="if(document.getElementById('spoiler') .style.display=='none') {document.getElementById('spoiler') .style.display=''}else{document.getElementById('spoiler') .style.display='none'}">Show/hide</button>
        ''',"<br>")

    count = 0
    # data = [['Number', 'Question', 'Answer', 'Types']]
    data = []
    for question, answer in questions.items():
        data.append([count, question, answer[0], answer[1]])
        count += 1
    
    with open('questions_answers.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(data)

    #print('{ data:' + str(data) + "}")
