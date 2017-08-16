import json

choose_questions = []
writing_questions = []
drag_questions = []
pair_questions = []

with open('banco_questoes/arrastar.json') as json_data:
	drag_questions = json.load(json_data)

with open('banco_questoes/escrever.json') as json_data:
	writing_questions = json.load(json_data)

with open('banco_questoes/multi_esc.json') as json_data:
	choose_questions = json.load(json_data)

#with open('banco_questoes/pares.json') as json_data:
#	pair_questions = json.load(json_data)


# print "choose questions : "+str(choose_questions)
# print "writing questions : "+str(writing_questions)
# print "drag questions : "+str(drag_questions)
#print "pair questions : "+str(pair_questions)