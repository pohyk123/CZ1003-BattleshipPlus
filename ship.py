# CZ1003 Battleship+ [Group Project]
# Contains the Ship Class

class Ship:
	def __init__(self,len,img,rot,head):
		self.len = len
		self.img = img
		self.initPos = (0,0)
		self.head = head
		self.life = self.len
		self.rot = rot #horizontal (H) or vertical (V)
		self.body = self.bodyIdx() #includes head
		self.damaged = []
		self.isPickedUp = 0

	# position indexes of the ship, based off position of shiphead
	def bodyIdx(self):
		body = []
		x_head,y_head = self.head
		if(self.rot=='H'):
			for i in range(self.len):
				x = x_head+i
				body.append((x,y_head))
		else:
			for i in range(self.len):
				y = y_head+i
				body.append((x_head,y))
		return body

	# checks if any part of the ship gets hit and update damage
	def hit(self,ij):
		i,j = ij
		if((i,j) in self.body and (i,j) not in self.damaged):
			self.life-=1
			self.damaged.append((i,j))
			print((i,j),end=' ')
			return True
		else:
			return False

	# Reset ship drawing
	def drawReset(self):
		self.head = self.initPos
		self.rot = rot #horizontal (H) or vertical (V)
		self.body = self.bodyIdx() #includes head
		self.isPickedUp = 0
		self.drawShip()
