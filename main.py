import kivy
kivy.require('1.9.0')
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Line,Rectangle
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from random import randint
from threading import Thread
import time

class organelle:
	Name = ''
	Energy = 0

	def __init__ (self,name,energy):
			self.Name=name
			self.Energy = energy




class mainApp(App):

	lost = False
	organelles = ()
	mitochondria = ()

	ATP = None
	ATP_Skinum = 2
	AddingAtp = False

	def switchSkin(self):
		ATPObj, skinNum = self.ATP,self.ATP_Skinum
		if skinNum == 2: ATPObj.source="ATP.png"
		elif skinNum == 1: ATPObj.source="ADP.png"
		elif skinNum == 0: ATPObj.source="AMP.png"


	def phospherousCheck(self,mitochondria):

		ATPPOS = self.ATP.pos
		organPos = mitochondria[1].pos
		if organPos[0] + 25 >=ATPPOS[0] >= organPos[0] - 25 and organPos[1] + 25 >=ATPPOS[1] >= organPos[1] - 25 and self.ATP_Skinum != 2:
			self.ATP_Skinum+=1
			print self.ATP_Skinum
			self.switchSkin()

		# else: 
		# 	print organPos[0] + 50 >=ATPPOS[0] >= organPos[0] - 50 
		# 	print organPos[1] + 50 >=ATPPOS[1] >= organPos[1] - 50
		# 	print self.ATP_Skinum != 2
		# 	print ''
		# 	self.AddingAtp = True
		# 	return

	def givePhosperous(self):
		self.AddingAtp = True

		for j in xrange(3):
			for i in self.mitochondria:
				self.phospherousCheck(i)
				time.sleep(2*j)
		self.AddingAtp = False








	def movementCheck(self):
		ATPPOS = self.ATP.pos
		for i in self.organelles: 
			organelle = i[1]
			organPos = organelle.pos

			if organPos[0] + 25 >=ATPPOS[0] >= organPos[0] - 25 and organPos[1] + 25 >=ATPPOS[1] >= organPos[1] - 25 and self.ATP_Skinum != 0:
				i[0].Energy+=10
				self.ATP_Skinum += -1
				self.switchSkin()

		for i in self.mitochondria:
			organPos = i[1].pos
		
			if organPos[0] + 25 >=ATPPOS[0] >= organPos[0] - 25 and organPos[1] + 25 >=ATPPOS[1] >= organPos[1] - 25 and self.ATP_Skinum != 2:
				Thread(target=self.givePhosperous).start()


	def updateGlucose(self,dt):
		for mitochondria in self.mitochondria:
			mitochondria[0] += 10

	def makeSureOrganellesAreAlive(self,dt):
		for obj in self.organelles: 
			if obj[0].Energy < 1: 
				lost=True 
				break
			else: obj[0].Energy-1



	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None

	def buildATP(self):
		startingpos =self.mitochondria[randint(0,len(self.mitochondria)-1)]

		self.ATP = Image(source='ATP.png',pos=startingpos[1].pos,size_hint_x=.1,size_hint_y=.1)

	def buildOrganells(self):
		
		nucleus = organelle("nucleus",50)
		golgiApparatus = organelle("nucleus",30)
		smoothER = organelle("nucleus",20)
		roughER = organelle("nucleus",20)
		
		

		self.mitochondria = ([10,Image(source="mitochondria.png",pos=(100,325),size_hint_y=.2,size_hint_x=.2)],[10,Image(source="mitochondria.png",pos=(525,400),size_hint_y=.15,size_hint_x=.15)],[10,Image(source="mitochondria.png",pos=(300,60),size_hint_y=.15,size_hint_x=.15)])
		self.organelles = ((nucleus,Image(source="nuclous.png",pos=(0,0))),(golgiApparatus,Image(source="golgibody.png",pos=(300,375),size_hint_y=.2,size_hint_x=.2)),(smoothER,Image(source="smoothER.png",pos=(450,250),size_hint_y=.15,size_hint_x=.15)),(roughER,Image(source="roughtER_burned.png",pos=(375,150),size_hint_y=.2,size_hint_x=.2)))

   

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		if keycode[1] == 'w':
			self.ATP.pos[1] += 10
		elif keycode[1] == 's':
			self.ATP.pos[1] += -10
		elif keycode[1] == 'a':
			self.ATP.pos[0] += -10
		elif keycode[1] == 'd':
			self.ATP.pos[0] += 10
		if self.AddingAtp == False: self.movementCheck()
		return True


	def build(self):
		
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)

		self.buildOrganells()

		
		root = FloatLayout(width=(Window.width),height=(Window.height),)
		
		with root.canvas:
			Line(circle=(Window.width/2,Window.height/2,Window.height/2))
		

		for obj in self.organelles: root.add_widget(obj[1])
		for obj in self.mitochondria: 
			
			root.add_widget(obj[1])

		self.buildATP()

		root.add_widget(self.ATP)



		Clock.schedule_interval(self.makeSureOrganellesAreAlive, 1)
		Clock.schedule_interval(self.updateGlucose,10)

		return root

if __name__ == "__main__":
	mainApp().run()
