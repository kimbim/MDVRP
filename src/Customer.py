class Customer:
	def __init__(self,i,x,y,q):
		self.i = i
		self.x = x
		self.y = y
		self.q = q # demand for this customer

	def __repr__(self):
		return str(self.i)