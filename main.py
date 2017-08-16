# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.behaviors import DragBehavior
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from functools import partial
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.togglebutton import ToggleButton as TB
from kivy.uix.stacklayout import StackLayout
from statistics_sender import send_statistics, is_connected
from kivy.cache import Cache
from kivy.uix.popup import Popup
import time
from random import randint
from random import uniform
from random import sample

from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    NumericProperty,
    StringProperty,
    ListProperty,
    ObjectProperty,
    OptionProperty,
    ReferenceListProperty,
)
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

sm = ScreenManager(transition=FadeTransition())
Builder.load_file('layouts/menu.kv')
Builder.load_file('layouts/brick.kv')
Builder.load_file('layouts/multescolha.kv')
Builder.load_file('layouts/figuras.kv')
Builder.load_file('layouts/escrever.kv')
Builder.load_file('layouts/pares.kv')
Builder.load_file('layouts/tutorial.kv')
Builder.load_file('layouts/sobre.kv')

figuras_game_screen = None
escrever_game_screen = None
multi_game_screen = None
pares_game_screen = None
menu_screen = None
tutorial_screen = None
sobre_screen = None

game = None
from game import Game

hasCation = False
hasAnion = False

magic_img_ref1 = None
magic_img_ref2 = None

grabbed = False

class ajudaPopup(Popup):#classe que serve de base para criacao de popups de ajuda
	def on_press_dismiss(self, name, *args):#metodo que permite ao popup se fechar
		self.dismiss()#fecha o popup
		return

class Brick(DragBehavior, Widget):#classe que implementa os tijolos arrastaveis
    #Propriedades da classe
    id = StringProperty("")
    is_in = False
    box_size_w = NumericProperty(0)
    box_size_h = NumericProperty(0)
    ans_box_x = NumericProperty(0)
    ans_box_y = NumericProperty(0)
    ans_box_h = NumericProperty(0)
    ans_box_w = NumericProperty(0)
    max_dist = NumericProperty(0)
    hor_offset = NumericProperty(0)
    start_h_porc = NumericProperty(0)
    start_w_porc = NumericProperty(0)
   
    updated = NumericProperty(0)
    imgs = StringProperty("")
    img_name = StringProperty("")
    my_type = StringProperty("")

    
    def on_touch_up(self, t):#metodo chamado quando o tijolo e solto

        if self.collide_point(*t.pos):#verifica se esta dentro da regiao
            self.check_inside_sregion(self.ans_box_x, self.ans_box_y, self.ans_box_w, self.ans_box_h)
    

        super(Brick,self).on_touch_up(t)


    def check_inside_sregion(self, valx, valy, valw, valh):#implementacao da parte que verifica se esta na regiao da resposta
        if valx < self.x and ((valx+valw)-self.width) > self.x:#se estiver dentro dos parametros
            if valy < self.y and ((valy+valh)-self.height) > self.y:
                self.is_in = True#atributo que marca como estando dentro da zona de resposta
                return
       
        self.is_in = False#se chegou ate aqui, entao nao esta dentro da regiao de resposta
       
class ImageBrick(Brick):
    pass

class CustomScreen(Screen):#classe base para janelas do jogo
    def __init__(self, **kwargs):
		super(CustomScreen, self).__init__(**kwargs)
    
    def swap_screen(self, screen_to_swap, args = None):#metodo que muda a janela

        global game, figuras_game_screen, escrever_game_screen, multi_game_screen, pares_game_screen, menu_screen, sm
        global tutorial_screen, sobre_screen
        if screen_to_swap == 'game':#se a janela for do tipo jogo

            question = game.get_question()#pega a proxima pergunta

            # if True:
            if question == None:#se nao houver pergunta
                game.time = time.time() - game.time#verifica o tempo total em segundos
                send_statistics(game.format_questions(), int(game.time))#envia estatisticas
                
                #cria popup do fim
                cont = BoxLayout(id='end_popup_cont',orientation='vertical',spacing=[0,2])

                cont2 = BoxLayout(id='score_name_cont',orientation='horizontal', padding=[0,0,0,0])
                lab_end = Label(text='[color=FFFFFF][b]'+'Parabéns por concluir o jogo!'+'[/b][/color]', markup=True, size_hint=(.5,1), halign='center')
                img = Image(source='cientista.jpg',allow_stretch=True,keep_ratio=True,size_hint=(1,3))
                img.bind(size=lambda s, w: s.setter('texture_size')(s, w))
                lab_end.bind(size=lambda s, w: s.setter('text_size')(s, w))
                cont.add_widget(img)
                cont2.add_widget(lab_end)
                exitbtn = Button(text='[b]OK[/b]',markup=True, font_size='25sp', size_hint=(.4,2), background_color=(.4,.4,.4, 0.95), pos_hint={'center_x': .5})
                cont.add_widget(cont2)
                lab_end.bind(size=lambda s, w: s.setter('text_size')(s, w))

                #mensagem customizada para pontuacao perfeita
                if game.points < 30:
                    custom_text = "\nPara se tornar um cientista "
                    custom_text2 = "você deve atingir 30 pontos!"

                else:
                    custom_text = "\nVocê se tornou um cientista!"
                    custom_text2 = ""


                #exibe pontuacao
                lab_end_point = Label(id='score_disp',text='[color=FFFFFF][b]Resultado Final: '+str(game.points)+' Pontos[/b][/color]',size_hint=(1,1), markup=True, halign='center')
                cont.add_widget(lab_end_point)
                lab_end_point.bind(size=lambda s, w: s.setter('text_size')(s, w))

                lab_custom = Label(id='lab_custom',text='[color=FFFFFF][b]'+ custom_text+'[/b][/color]',size_hint=(1,1),markup=True, halign='center')
                lab_custom2 = Label(id='lab_custom2',text='[color=FFFFFF][b]'+ custom_text2+'[/b][/color]',size_hint=(1,1),markup=True, halign='center')
                cont.add_widget(lab_custom)
                lab_custom.bind(size=lambda s, w: s.setter('text_size')(s, w))
                cont.add_widget(lab_custom2)
                lab_custom2.bind(size=lambda s, w: s.setter('text_size')(s, w))

                cont.add_widget(exitbtn)

                var = ajudaPopup(id='popup_end',title='Resultado Final', content=cont, size_hint=(.8, .4), auto_dismiss=False)
                var.open()
                exitbtn.bind(on_press=var.on_press_dismiss)

                screen_to_swap = MenuScreen(name='menu')#volta ao menu

            else:#se houver pergunta

                #criar uma janela do tipo sorteado
                if question['question_type'] == 'arrastar':

                    screen_to_swap = Figuras(name='figuras', question = question)

                elif question['question_type'] == 'escrever':

                    screen_to_swap = Escrever(name='escrever', question = question)

                elif question['question_type'] == 'multi_esc':
                    screen_to_swap = Multescolha(name='multescolha', question = question)
                else:
                    screen_to_swap = Pares(name='pares', question = question)
        #outros tipos de janela
        elif screen_to_swap == 'menu':
            screen_to_swap = MenuScreen(name='menu')
        elif screen_to_swap == 'tutorial':
            screen_to_swap = Tutorial(name='tutorial')
        elif screen_to_swap == 'sobre':
            screen_to_swap = Sobre(name='sobre')

        sm.switch_to(screen_to_swap)#mudar a janela

class GameScreen(CustomScreen):#base para janela do tipo jogo
    def __init__(self, name = None, question = None):
        super(CustomScreen, self).__init__(name = name)
        self.question = question

        self.get_ans = None

    def showPopup(self, args):#metodo exibir popup nas janelas do jogo
        cont = BoxLayout(id='cur_popup_cont',orientation='vertical', size_hint=(1,1))
        mlabel = Label(valign="top", size_hint=(1,5), text='[size=16sp][color=FFFFFF][b]'+self.helpText+'[/b][/color][/size]', markup=True)
        mlabel.bind(size=lambda s, w: s.setter('text_size')(s, w))
        cont.add_widget(mlabel)
        exitbtn = Button(text='OK',size_hint=(.5,1), pos_hint={'center_x': .5}, font_name= "./OpenSpritesUI/Font/Ranchers-Regular.ttf")
        cont.add_widget(exitbtn)

        ajpop = ajudaPopup(id='popup_cur',title='Ajuda', content=cont, size_hint=(.9, .5), auto_dismiss=False)
        ajpop.open()
        exitbtn.bind(on_press=ajpop.on_press_dismiss)

    def next_question(self, special_used = False):#metodo que busca a proxima pergunta
        global game

        self.get_ans()#pega a resposta

        right_ans = game.check_answer(self.get_ans() , self.question, special_used)

        if right_ans:#se resposta estiver correta
            cont = BoxLayout(id='cur_popup_acertou',orientation='vertical')
            cont2 = BoxLayout()
            mlabel = Label(text='[size=16sp][color=FFFFFF][b]'+'Resposta Correta\nParabens Você acertou!'+'[/b][/color][/size]', markup=True, halign='center')
            mlabel.bind(size=lambda s, w: s.setter('text_size')(s, w))
            cont.add_widget(mlabel)
            cont.add_widget(cont2)
            exitbtn = Button(text='OK',size_hint=(.5,1), pos_hint={'center_x': .5}, font_name= "./OpenSpritesUI/Font/Ranchers-Regular.ttf")
            cont.add_widget(exitbtn)

            ajpop = ajudaPopup(id='popup_acerto',title='Resultado', content=cont, size_hint=(.9, .3), auto_dismiss=False)
            ajpop.open()
            exitbtn.bind(on_press=ajpop.on_press_dismiss)
            ajpop.bind(on_dismiss=self.closedFinalPopup)
        else:#se estiver errado
            cont = BoxLayout(id='cur_popup_errou',orientation='vertical')
            cont2 = BoxLayout()
            mlabel = Label(text='[size=16sp][color=FFFFFF][b]'+'Resposta Incorreta\nContinue Tentando!'+'[/b][/color][/size]', markup=True, halign='center')
            mlabel.bind(size=lambda s, w: s.setter('text_size')(s, w))
            cont.add_widget(mlabel)
            cont.add_widget(cont2)
            exitbtn = Button(text='OK',size_hint=(.5,1), pos_hint={'center_x': .5}, font_name= "./OpenSpritesUI/Font/Ranchers-Regular.ttf")
            cont.add_widget(exitbtn)

            ajpop = ajudaPopup(id='popup_erro',title='Resultado', content=cont, size_hint=(.9, .3), auto_dismiss=False)
            ajpop.open()
            exitbtn.bind(on_press=ajpop.on_press_dismiss)
            ajpop.bind(on_dismiss=self.closedFinalPopup)

    def closedFinalPopup(self, args):
        self.swap_screen('game')

    def set_image_score(self, stack):#metodo que trata as imagens de pontuacao

        global game

        if game.scored_questions < 5:#se pontos estiverem no tipo 1
            image_score = './IMAGENS_JOGO/Pontos_jogo/testtube.png'

        elif game.scored_questions >= 5 and  game.scored_questions < 10:#se pontos estiveram no tipo 2
            image_score = './IMAGENS_JOGO/Pontos_jogo/erlenmeyer.png'

        else:#se pontos estiverem no tipo 3
            image_score = './IMAGENS_JOGO/Pontos_jogo/balao.png'

        n_score_icons = game.scored_questions%5

        #parte que trata imagens de pocoes magicas
        global magic_img_ref1
        src = Image(source='./IMAGENS_JOGO/Pontos_jogo/magic2.gif', size_hint=(.1,1), id="img_magic1")
        magic_img_ref1 = src
        global magic_img_ref2
        src2 = Image(source='./IMAGENS_JOGO/Pontos_jogo/magic3.gif', size_hint=(.1,1), id="img_magic2")
        magic_img_ref2 = src2

        for x in range(n_score_icons):#para cada icone adicione ao stack
            scr = Image(source=image_score, size_hint=(.1,1))
            stack.add_widget(scr)

        if game.Magic2 == True:#adicione pocoes magicas se existirem
            stack.add_widget(src2)
        
        if game.Magic1 == True:
            stack.add_widget(src)
       

class Sobre(GameScreen):#janela do menu sobre
    def __init__(self, name = None):
        super(Sobre, self).__init__(name = name)  
        txt = self.ids.text_sobre
        txt.bind(size=lambda s, w: s.setter('text_size')(s, w))#vincula o tamanho do texto a janela

    def get_menu(self):#volta ao menu
        self.swap_screen('menu')

class Tutorial(GameScreen):#janela da classe tutorial
    def __init__(self, name = None):
        super(Tutorial, self).__init__(name = name)
        self.slide_num = 1
        img = self.ids.slide_img
        img.source = "./img_tutoriais/tela1.png"

    def get_menu(self):#volta ao menu
        self.swap_screen('menu')

    def next_slide(self):#metodo que busca o proximo slide
        self.slide_num = self.slide_num+1
        if self.slide_num == 9:#se for o ultimo volta ao menu
            self.get_menu()
        else:#senao pega o proximo
            img = self.ids.slide_img
            img.source = "./img_tutoriais/tela"+ str(self.slide_num) +".png"

class Pares(GameScreen):#janela da classe de cations e anions
    drawed = False
    count = 0
    count2 = 0
    bricks = []
    root_path = "./banco_questoes/imagens/imagens_arrastar/"

    def get_ans_implemented(args):#metodo que retorna a resposta do jogador
        ans = []
        for brick in args.bricks_cation:
            if brick.is_in:
                ans.append((brick.img_name,0))
        for brick in args.bricks_anion:
            if brick.is_in:
                ans.append((brick.img_name,1))

    
        return ans

    def __init__(self, name = None, question = None):
        super(Pares, self).__init__(name = name, question = question)
        rbox = self.ids.par_answ_box_cation
        rbox.bind(pos=self.update)
        rbox.bind(size=self.update)

        rbox2 = self.ids.par_answ_box_anion
        rbox2.bind(pos=self.update)
        rbox2.bind(size=self.update)

        self.bricks_cation = []
        self.bricks_anion = []
        self.cation_tuple = []
        self.anion_tuple = []
        self.cations = question['cation']
        self.anions = question['anion']
        
        for element in self.cations:#para cada cation
            self.cation_tuple.append((element, "cation"))#adiciona a lista

        for element in self.anions:#para cada anion
            self.anion_tuple.append((element, "anion"))#adiciona a lista

        self.bricks_joined = self.cation_tuple+self.anion_tuple
        self.conj = sample(self.bricks_joined, len(self.bricks_joined))

        if "help" in question:#se houver ajuda
            self.helpText = question["help"]
            btn_ajuda = self.ids.btn_help_par
            btn_ajuda.bind(on_press=self.showPopup)#desenha popup quando for clicado
        else:#se nao houver
            btn_ajuda = self.ids.btn_help_par
            btn_ajuda.disable = True
       

        self.ids.enunciado_label.text = u"[color=FFFFFF][b]"+question['enunciado']+u"[/b][/color]"

        scrbox = self.ids.par_scorebox
        stack = StackLayout(orientation='rl-tb')
        #desenha pontuacao
        self.set_image_score(stack)
        global game
        txt = Label(text="[color=252525][b]Pontuação : %d[/b][/color]"%(game.points), font_name= "./OpenSpritesUI/Font/Ranchers-Regular.ttf",size_hint=(1, 1), markup=True, font_size="20sp")
        scrbox.add_widget(txt)

        scrbox.add_widget(stack)
        self.update()
        self.get_ans = self.get_ans_implemented
    
    def apply_magic(self):#botao da pocao magica
        cont = BoxLayout(id='cur_popup_pares',orientation='vertical')
        cont2 = BoxLayout()
        mlabel = Label(text='[size=16sp][color=FFFFFF][b]'+'Bônus apenas para questões de múltipla escolha!'+'[/b][/color][/size]', markup=True)#avisa que so pode ser usada em multipla escolha
        mlabel.bind(size=lambda s, w: s.setter('text_size')(s, w))
        cont.add_widget(mlabel)
        cont.add_widget(cont2)
        exitbtn = Button(text='OK',size_hint=(.5,1), pos_hint={'center_x': .5}, font_name= "./OpenSpritesUI/Font/Ranchers-Regular.ttf")
        cont.add_widget(exitbtn)

        ajpop = ajudaPopup(id='popup_mag_pares',title='Ajuda', content=cont, size_hint=(.9, .3), auto_dismiss=False)
        ajpop.open()
        exitbtn.bind(on_press=ajpop.on_press_dismiss)
   

    def update(self, *args):#metodo que atualiza a janela quando e redimensionada
        if self.height != 100 and self.width != 100:

            self.remove_bricks()
            self.insert_bricks()

      
    def end_pares(self):#metodo do botao de proximo
        global hasCation ,hasAnion
        hasAnion = False
        hasCation = False
        self.remove_bricks()
        self.next_question()
        self.bricks_cation = []
        self.bricks_anion = []
        

    def insert_bricks(self):#insere os tijolos

        i = 0
        for item in self.conj:
            self.add_brick(self.root_path+item[0], i, item)
            i = i+1

    def remove_bricks(self):#remove os tijolos
        self.count = 0
        self.count2 = 0
        self.box = self.ids.par_brk_box
        for brick in self.bricks_cation:#remove todos os tijolos de cation
            self.box.remove_widget(brick)

        for brick in self.bricks_anion:#remove todos os tijolos de anion
            self.box.remove_widget(brick)
    
    def add_brick(self, image_path, index, item):#adiciona os tijolos
        brick = Brick()
        elem = self.conj[index]

        if elem[1] == "cation":#distribui os tijolos de acordo com o tipo
            self.bricks_cation.append(brick)
        elif elem[1] == "anion":
            self.bricks_anion.append(brick)
        
        self.box = self.ids.par_brk_box
        brick.my_type = elem[1]
        brick.box_size_w = self.width
        brick.box_size_h = self.height

        if elem[1] == "cation":
            self.ansbox = self.ids.par_answ_box_cation
            brick.id = str(self.count)
            self.count = self.count+1
        elif elem[1] == "anion":
            self.ansbox = self.ids.par_answ_box_anion
            brick.id = str(self.count2)
            self.count2 = self.count2+1

        brick.ans_box_x = self.ansbox.x
        brick.ans_box_y = self.ansbox.y
        brick.ans_box_h = self.ansbox.height
        brick.ans_box_w = self.ansbox.width

        brick.pos = self.box.pos
        brick.imgs = image_path
        brick.img_name = item[0]
        brick.start_h_porc = .15

        self.box.add_widget(brick)
        return brick

class Figuras(GameScreen):#janela da classe de figuras de arrastar comum
    drawed = False
    count = 0
    bricks = []
    root_path = "./banco_questoes/imagens/imagens_arrastar/"

    def get_ans_implemented(args):#metodo que retorna a resposta
        ans = []
        for brick in args.bricks:
            if brick.is_in:
                ans.append(brick.img_name)

        return ans




    def __init__(self, name = None, question = None):

        super(Figuras, self).__init__(name = name, question = question)
        rbox = self.ids.fig_answ_box
        rbox.bind(pos=self.update)
        rbox.bind(size=self.update)

        if 'image' in question:#se houver imagem de fundo desenhe
            self.ids.background_box.canvas.get_group('a')[0].source = "banco_questoes/" + question['image']


        self.bricks = []

        self.brick_images = question['options']
        self.conj = sample(self.brick_images, len(self.brick_images))
        if "help" in question:#se houver ajuda, apresente quando for clicado
            self.helpText = question["help"]
            btn_ajuda = self.ids.btn_help_fig
            btn_ajuda.bind(on_press=self.showPopup)
        else:#se nao houver ajuda
            btn_ajuda = self.ids.btn_help_fig
            btn_ajuda.disable = True
       
        self.ids.enunciado_label.text = u"[color=FFFFFF][b]"+question['enunciado']+u"[/b][/color]"

        self.update()
        scrbox = self.ids.fig_scorebox
        stack = StackLayout(orientation='rl-tb')

        self.set_image_score(stack)
        global game
        txt = Label(text="[color=252525][b]Pontuação : %d[/b][/color]"%(game.points), font_name= "./OpenSpritesUI/Font/Ranchers-Regular.ttf", size_hint=(1, 1), markup=True, font_size="20sp")
        scrbox.add_widget(txt)

        scrbox.add_widget(stack)

        self.get_ans = self.get_ans_implemented

    def apply_magic(self):#botao pocao magica, avisa que so vale para classe multipla escolha
        cont = BoxLayout(id='cur_popup_figuras',orientation='vertical')
        cont2 = BoxLayout()
        mlabel = Label(text='[size=16sp][color=FFFFFF][b]'+'Bônus apenas para questões de múltipla escolha!'+'[/b][/color][/size]', markup=True)
        mlabel.bind(size=lambda s, w: s.setter('text_size')(s, w))
        cont.add_widget(mlabel)
        cont.add_widget(cont2)
        exitbtn = Button(text='OK',size_hint=(.5,1), pos_hint={'center_x': .5}, font_name= "./OpenSpritesUI/Font/Ranchers-Regular.ttf")
        cont.add_widget(exitbtn)

        ajpop = ajudaPopup(id='popup_mag_figuras',title='Ajuda', content=cont, size_hint=(.9, .3), auto_dismiss=False)
        ajpop.open()
        exitbtn.bind(on_press=ajpop.on_press_dismiss)

   

    def update(self, *args):#metodo que atualiza a janela quando a resolucao muda
        if self.height != 100 or self.width != 100:

            self.remove_bricks()
            self.insert_bricks()
       
    def end_figuras(self):#metodo do botao proximo
        self.remove_bricks()
        self.next_question()
        self.bricks = []
        

    def insert_bricks(self):#insere os tijolos
        for item in self.conj:
            self.add_brick(self.root_path+item, item)

    def remove_bricks(self):#remove os tijolos
        self.count = 0
        self.box = self.ids.fig_brk_box
        for brick in self.bricks:
            self.box.remove_widget(brick)
            
    def add_brick(self, image_path, item):#adiciona os tijolos
        brick = Brick()
        self.bricks.append(brick)
        self.box = self.ids.fig_brk_box
        brick.box_size_w = self.width
        brick.box_size_h = self.height

        self.ansbox = self.ids.fig_answ_box#parametros do tijolo
        brick.ans_box_x = self.ansbox.x
        brick.ans_box_y = self.ansbox.y
        brick.ans_box_h = self.ansbox.height
        brick.ans_box_w = self.ansbox.width

        brick.id = str(self.count)
        self.count = self.count+1
        brick.pos = self.box.pos
        brick.start_h_porc = .15
        brick.imgs = image_path
        brick.img_name = item
       

        self.box.add_widget(brick)
       
        return brick


class Multescolha(GameScreen):#janela da classe de multipla escvolha
    usouMagic = False
    def get_ans_implemented(args):#retorna a resposta escolhida
        mydict = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e"}#dicionario para acessar as alternativas por letra
        tbs = [args.ids.a, args.ids.b, args.ids.c, args.ids.d, args.ids.e]

        for t in range(len(tbs)):
            if tbs[t].state=='down':#se a alternativa esta selecionada retorna ela
                return mydict[t]
            
        return ""


    def __init__(self, name = None, question = None):
        if 'image' in question:#se houver imagem desenha no fundo
            self.bg_image = "banco_questoes/" + question['image']
        else:
            self.bg_image = "white.jpg"
        super(Multescolha, self).__init__(name = name, question  = question)

        if "help" in question:#se houver ajuda mostra quando clica no botao
            self.helpText = question["help"]
            btn_ajuda = self.ids.btn_help_mesc
            btn_ajuda.bind(on_press=self.showPopup)
        else:#se nao houver ajuda
            btn_ajuda = self.ids.btn_help_mesc
            btn_ajuda.disable = True

        self.ids.lab_perg_mesc.text = u"[color=FFFFFF]"+ question['enunciado']+ u"[/color]"#carrega as alternativas

        self.ids.alta.text = u"[color=000000]" + question['alta'] + u"[/color]"
        self.ids.altb.text = u"[color=000000]" + question['altb'] + u"[/color]"
        self.ids.altc.text = u"[color=000000]" + question['altc'] + u"[/color]"
        self.ids.altd.text = u"[color=000000]" + question['altd'] + u"[/color]"
        self.ids.alte.text = u"[color=000000]" + question['alte'] + u"[/color]"

        scrbox = self.ids.mesc_scorebox
        stack = StackLayout(orientation='rl-tb')
        self.scr_img_stack = stack

        self.set_image_score(stack)
        global game
        txt = Label(text="[color=252525][b]Pontuação : %d[/b][/color]"%(game.points), font_name= "./OpenSpritesUI/Font/Ranchers-Regular.ttf", size_hint=(1, 1), markup=True, font_size="20sp")
        scrbox.add_widget(txt)
        scrbox.add_widget(stack)

        self.get_ans = self.get_ans_implemented

        self.adjust_magic()
    
    def adjust_magic(self):#ajusta botao da pocao magica
        btn = self.ids.magicPotion_btn
        if game.Magic1 == True or game.Magic2 == True:
            btn.background_normal = "./OpenSpritesUI/PNG/blue_sliderUp.png"
            btn.background_down = "./OpenSpritesUI/PNG/blue_sliderUp.png"
            btn.text = "[color=FFFFFF][b]Bônus[/b][/color]"
            btn.color=(1,1,1,1)

    def apply_magic(self):#aplica a pocao magica
        if self.usouMagic == False:#elimina a pocao magica utilizada
            if game.Magic1 == True:
                self.usouMagic = True
                game.Magic1 = False
                self.elim_answers()
                global magic_img_ref1
                self.scr_img_stack.remove_widget(magic_img_ref1)
                
            elif game.Magic2 == True:
                self.usouMagic = True
                game.Magic2 = False
                self.elim_answers()
                global magic_img_ref2
                self.scr_img_stack.remove_widget(magic_img_ref2)
            else:#quando nao tem pocao magica e tenta usar
                cont = BoxLayout(id='cur_popup_mesc',orientation='vertical')
                cont2 = BoxLayout()
                mlabel = Label(text='[size=16sp][color=FFFFFF][b]'+'Você ainda não possui um Bônus'+'[/b][/color][/size]', markup=True)
                mlabel.bind(size=lambda s, w: s.setter('text_size')(s, w))
                cont.add_widget(mlabel)
                cont.add_widget(cont2)
                exitbtn = Button(text='OK',size_hint=(.5,1), pos_hint={'center_x': .5}, font_name= "./OpenSpritesUI/Font/Ranchers-Regular.ttf")
                cont.add_widget(exitbtn)

                ajpop = ajudaPopup(id='popup_mag_mesc',title='Ajuda', content=cont, size_hint=(.9, .3), auto_dismiss=False)
                ajpop.open()
                exitbtn.bind(on_press=ajpop.on_press_dismiss)
    
    def elim_answers(self):#metodo que elimina alternativas para a pocao magica
        eliminate1 = -1
        eliminate2 = -1
        if self.question['answer'] == 'a':#sorteia a eliminacao, ignorando as respostas corretas
            eliminate1 = randint(1,4)
            while (eliminate2 == -1) or (eliminate2 == eliminate1):
                eliminate2 = randint(1,4)
        elif self.question['answer'] == 'b':
            while (eliminate1 == -1) or (eliminate1 == 1):
                eliminate1 = randint(0,4)
            while (eliminate2 == -1) or (eliminate2 == 1) or (eliminate2 == eliminate1):
                eliminate2 = randint(0,4)
        elif self.question['answer'] == 'c':
            while (eliminate1 == -1) or (eliminate1 == 2):
                eliminate1 = randint(0,4)
            while (eliminate2 == -1) or (eliminate2 == 2) or (eliminate2 == eliminate1):
                eliminate2 = randint(0,4)
        elif self.question['answer'] == 'd':
            while (eliminate1 == -1) or (eliminate1 == 3):
                eliminate1 = randint(0,4)
            while (eliminate2 == -1) or (eliminate2 == 3) or (eliminate2 == eliminate1):
                eliminate2 = randint(0,4)
        elif self.question['answer'] == 'e':
            eliminate1 = randint(0,3)
            while (eliminate2 == -1) or (eliminate2 == eliminate1):
                eliminate2 = randint(0,3)

        if eliminate1 == 0:#faz a eliminacao e cada caso
            cont = self.ids.multesc_resp1
            cont.disabled = True
        elif eliminate1 == 1:
            cont = self.ids.multesc_resp2
            cont.disabled = True
        elif eliminate1 == 2:
            cont = self.ids.multesc_resp3
            cont.disabled = True
        elif eliminate1 == 3:
            cont = self.ids.multesc_resp4
            cont.disabled = True
        elif eliminate1 == 4:
            cont = self.ids.multesc_resp5
            cont.disabled = True

        if eliminate2 == 0:
            cont = self.ids.multesc_resp1
            cont.disabled = True
        elif eliminate2 == 1:
            cont = self.ids.multesc_resp2
            cont.disabled = True
        elif eliminate2 == 2:
            cont = self.ids.multesc_resp3
            cont.disabled = True
        elif eliminate2 == 3:
            cont = self.ids.multesc_resp4
            cont.disabled = True
        elif eliminate2 == 4:
            cont = self.ids.multesc_resp5
            cont.disabled = True   

   
class Escrever(GameScreen):#janela da classe de escrever
    def get_ans_implemented(args):#retorna a resposta escolhida
        myinput = args.ids.esc_txt_inpt
        return myinput.text

    def __init__(self, name = None, question = None):
        super(Escrever, self).__init__(name = name, question = question)
        Window.softinput_mode = 'below_target'#comportamento do teclado no celular

        self.ids.enunciado.text = u"[color=FFFFFF]" + question['enunciado'] + u"[/color]"

        if "help" in question:#se houver resposta mostre quando clicado
            self.helpText = question["help"]
            btn_ajuda = self.ids.btn_help_esc
            btn_ajuda.bind(on_press=self.showPopup)
        else:#se nao houver resposta
            btn_ajuda = self.ids.btn_help_esc
            btn_ajuda.disable = True

        if 'image' in question:#se houver imagem de fundo desenhe
            self.ids.esc_txt_inpt.background_normal = "banco_questoes/" + question['image']
            self.ids.esc_txt_inpt.background_active = "banco_questoes/" + question['image']

        scrbox = self.ids.esc_scorebox
        stack = StackLayout(orientation='rl-tb')
        
        self.set_image_score(stack)
       
        global game
        txt = Label(text="[color=252525][b]Pontuação : %d[/b][/color]"%(game.points), font_name= "./OpenSpritesUI/Font/Ranchers-Regular.ttf", size_hint=(1, 1), markup=True, font_size="20sp")
        scrbox.add_widget(txt)

        scrbox.add_widget(stack)

        self.get_ans = self.get_ans_implemented

    def apply_magic(self):#botao magico, avisa que so vale para multipla escolha
        cont = BoxLayout(id='cur_popup_esc',orientation='vertical')
        cont2 = BoxLayout()
        mlabel = Label(text='[size=16sp][color=FFFFFF][b]'+'Bônus apenas para questões de múltipla escolha!'+'[/b][/color][/size]', markup=True)
        mlabel.bind(size=lambda s, w: s.setter('text_size')(s, w))
        cont.add_widget(mlabel)
        cont.add_widget(cont2)
        exitbtn = Button(text='OK',size_hint=(.5,1), pos_hint={'center_x': .5}, font_name= "./OpenSpritesUI/Font/Ranchers-Regular.ttf")
        cont.add_widget(exitbtn)

        ajpop = ajudaPopup(id='popup_mag_esc',title='Ajuda', content=cont, size_hint=(.9, .3), auto_dismiss=False)
        ajpop.open()
        exitbtn.bind(on_press=ajpop.on_press_dismiss)

        
class MenuScreen(CustomScreen):#janela da classe do menu
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        title = self.ids.appTitle
       
    
    def get_tutorial(self):#clicou em tutorial
        self.swap_screen('tutorial')

    def get_sobre(self):#clicou em sobre
        self.swap_screen('sobre')

    def getgame(self):#comecou um jogo

        global game, figuras_game_screen, escrever_game_screen, multi_game_screen, pares_game_screen
        global tutorial_screen, sobre_screen

        game = Game()

        game.time = time.time()

        figuras_game_screen = None
        escrever_game_screen = None
        multi_game_screen = None
        pares_game_screen = None
        tutorial_screen = None
        sobre_screen = None

        self.swap_screen('game')

 


global menu_screen
menu_screen = MenuScreen(name='menu')
sm.add_widget(menu_screen)

class ACIBASE(App):#classe raiz do aplicativo
 
    def build(self):
        return sm

    def on_pause(self):
         return True

    def on_resume(self):

        pass
 
if __name__ == '__main__':
    print "internet : "
    print is_connected()
    
    ACIBASE().run()
