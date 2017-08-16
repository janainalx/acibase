
# -*- coding: utf-8 -*-

import random
import time
from question_loader import choose_questions, writing_questions, drag_questions #pair_questions

import re

class Game():
	print "class_game"
	def pick_questions(self, questions_db):
		#print "pick_questions_game"
		#Sorteia 5 questões dentro do banco de dados fornecido

		questions_ids = []
		questions = []

		while len(questions_ids) < 5:#mudar para 5 depois
			#print "teste_game"
			q = random.randint(0, len(questions_db)-1)

			if q not in questions_ids:
				questions_ids.append(q)


		for id_question in questions_ids:
			questions.append(questions_db[id_question])

		return questions


	def generate_questions(self):
		print "generate_questions_game"
		choose_questions_sorted = self.pick_questions(choose_questions)
		writing_questions_sorted = self.pick_questions(writing_questions)
		drag_questions_sorted = self.pick_questions(drag_questions)
		#pair_questions_sorted = self.pick_questions(pair_questions)

		round1 = [choose_questions_sorted.pop(), writing_questions_sorted.pop(),
				 choose_questions_sorted.pop(), drag_questions_sorted.pop(), choose_questions_sorted.pop()]

		
		round2 = [drag_questions_sorted.pop(), choose_questions_sorted.pop(),
				  writing_questions_sorted.pop(), drag_questions_sorted.pop(), writing_questions_sorted.pop()]

		round3 = [drag_questions_sorted.pop(), writing_questions_sorted.pop(),
				  choose_questions_sorted.pop(), drag_questions_sorted.pop(), writing_questions_sorted.pop()]


		rounds_temp = [round1, round2, round3]

		rounds_ids = []

		round_id = random.randint(0, 2)

		while round_id in rounds_ids:
			  round_id = random.randint(0, 2)

		rounds_ids.append(round_id)

		round_id = random.randint(0, 2)

		while round_id in rounds_ids:
			  round_id = random.randint(0, 2)

		rounds_ids.append(round_id)

		round_id = random.randint(0, 2)

		while round_id in rounds_ids:
			  round_id = random.randint(0, 2)

		rounds_ids.append(round_id)

		# print "rounds : " + str(rounds_ids)

		rounds = [rounds_temp[rounds_ids[0]], rounds_temp[rounds_ids[1]], rounds_temp[rounds_ids[2]]]

		self.rounds = rounds



	def __init__(self):
		print "init_game"
		self.points = 0

		self.time = None

		self.current_round = 0

		self.current_question = 0

		self.scored_questions = 0

		self.generate_questions()

		self.Magic1 = False
		self.Magic2 = False

		self.report = []

		self.specials = 0

		# for round in self.rounds:
		# 	for q in round:
		# 		print q['question_id']
	def has_questions_left(self):
		if self.current_round == 2:
			if (self.current_question+1) >= 5:
				return False
			
		return True


	def get_question(self):
		#print "get_question_game"
		if self.current_question == 5:

			if self.current_round == 2:
				return None

			self.current_round+=1
			self.current_question = 0
		
		self.current_question+=1

		return self.rounds[self.current_round][self.current_question-1]

	def format_questions(self):

		text_formated = u''

		for item in self.report:
			text_formated += u'Questão : ' + str(item['questao']) + u' ----------- '
			text_formated +=  u'Resposta : ' + str(item['resposta']) + u' '

			if 'entrada' in item:
				print item['entrada']

				text_formated += u" ----------- Entrada do aluno : " + item['entrada']

			text_formated += u'\n'

		return text_formated 

	def update_points(self):

		self.scored_questions += 1

		if self.scored_questions == 5:
			self.Magic1 = True

		if self.scored_questions == 10:
			self.Magic2 = True

		if self.scored_questions <= 5:
			multiplier = 1

		elif self.scored_questions > 5 and self.scored_questions <= 10:
			multiplier = 2

		else:
			multiplier = 3

		self.points += multiplier

		if self.scored_questions%5==0:
			self.specials +=1

	def sanitize_text(self, text):

		# text = text.decode('utf8')

	# Convert all to lower case
		text = text.lower()

		text = text.replace(u'á', 'a')
		text = text.replace(u'é', 'e')
		text = text.replace(u'í', 'i')
		text = text.replace(u'ó', 'o')
		text = text.replace(u'ú', 'u')

		text = text.replace(u'ã', 'a')
		text = text.replace(u'õ', 'o')

		text = text.replace(u'â', 'a')
		text = text.replace(u'ô', 'o')

		text = text.replace(u'ç', 'c')

		text = text.replace(',', '')
		text = text.replace('.', '')

		text = re.sub( '\s+', ' ', text ).strip()

		return text



	def check_answer(self, ans, question, special_used):
		print "check_ans_game"
		#print "question type : " + str(question['question_type'])

		if special_used:
			self.update_points()	
			self.report.append({'questao' : question['question_id'], 'resposta' : 'USOU ESPECIAL'})	
			return True

		if question['question_type'] == 'multi_esc':
			print "mult_escolha---------------------------"
			if question['answer'] == ans:
				self.update_points()
				self.report.append({'questao' : question['question_id'], 'resposta' : 'CERTA'})	
				return True

			self.report.append({'questao' : question['question_id'], 'resposta' : 'ERRADA', 'entrada' : '%s'%ans})
			#self.report.append({'questao' : question['question_id'], 'resposta' : 'ERRADA'})
			return False

		elif question['question_type'] == 'arrastar':
			print "arrastar---------------------------"
			ans_images = []

			for image_id in ans:
				print "IDS:  "+str(image_id)
				i = 0
				for item in question['options']:
					if item == image_id:
						break
					i = i+1
				ans_images.append(question['options'][i])

			ans = sorted(ans_images)

			expected_ans = sorted(question['answer'])
			
			print ">>>>>>RESPOSTAS"
			print ans
			print expected_ans

			if ans == expected_ans:
				self.update_points()
				self.report.append({'questao' : question['question_id'], 'resposta' : 'CERTA'})	
				return True

			# print ans
			# print expected_ans

			#self.report.append({'questao' : question['question_id'], 'resposta' : 'ERRADA'})
			self.report.append({'questao' : question['question_id'], 'resposta' : 'ERRADA', 'entrada' : '%s'%ans})
			return False

		elif question['question_type'] == 'escrever':#modificado verificar
			print "escrever---------------------------"
			ans = self.sanitize_text(ans)
			expected_ans = self.sanitize_text(question['answer'])

			if ans == expected_ans:
				self.update_points()
				self.report.append({'questao' : question['question_id'], 'resposta' : 'CERTA'})	
				return True

			self.report.append({'questao' : question['question_id'], 'resposta' : 'ERRADA', 'entrada' : '%s'%ans})
			return False
		else:#pares
			print "pares---------------------------"
			ans_images = []

			z = 0
			for items in question['cation']:#itens da segunda lista devem descontar os indices da primeira
				z = z+1

			for (x,y) in ans:
				#print "<><><><><><><><><>"
				#print y
				if y == 0:
					print str(question['cation'])
					print "index->" + str(x)
					i = 0
					for item in question['cation']:
						if item == x:
							break
						i = i+1
					ans_images.append(question['cation'][i])
				else:
					print str(question['anion'])
					print "index->" + str(x)
					i = 0
					for item in question['anion']:
						if item == x:
							break
						i = i+1
					ans_images.append(question['anion'][i])

			ans = sorted(ans_images)
			print str(ans)+"--XXX---"
			expected_ans = sorted(question['answer'])
		
			print ">>>>>>RESPOSTAS"
			print ans
			print expected_ans
			
			if ans == expected_ans:
				self.update_points()
				self.report.append({'questao' : question['question_id'], 'resposta' : 'CERTA'})	
				return True

			# print ans
			# print expected_ans
			self.report.append({'questao' : question['question_id'], 'resposta' : 'ERRADA'})
			return False







		
