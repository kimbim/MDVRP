class Depot:
	def __init__(self,i,x,y,D,Q,m):
		self.i = i
		self.x = x
		self.y = y
		if D == 0:
			self.D = float('inf')
		else:
			self.D = D # maximum duration of a route
		self.Q = Q # allowed maximum load of a vehicle (same for all the vehicles assigned to all depots) 
		self.m = m # maximum number of vehicles available in each depot
		self.customer_list = []
		self.vehicles = [[]]

	def __repr__(self):
		return str(self.i)

	# Route scheduling
	def route_schedule(self):
		vehicle = 0
		for c in self.customer_list:
			self.vehicles[vehicle].append(c)
			if self.route_duration(vehicle) > self.D or self.vehicle_load(vehicle) > self.Q:
				self.vehicles[vehicle].remove(c)
				vehicle += 1
				self.vehicles.append([c])

	def update_customer_list(self):
		self.customer_list = []
		for vehicle in range(len(self.vehicles)):
			for c in self.vehicles[vehicle]:
				self.customer_list.append(c)

	def update_routes(self):
		counter = 0
		for vehicle in range(len(self.vehicles)):
			inner_counter = 0
			for c in self.vehicles[vehicle]:
				self.vehicles[vehicle][inner_counter] = self.customer_list[counter]
				inner_counter += 1
				counter += 1
	# Working 
	def route_duration(self,vehicle):
		duration = 0
		if len(self.vehicles[vehicle]) > 1:
			duration += self.distance(self,self.vehicles[vehicle][0])
			for i in range(1,len(self.vehicles[vehicle])):
				duration += self.distance(self.vehicles[vehicle][i-1],self.vehicles[vehicle][i])
			duration += self.distance(self.vehicles[vehicle][-1],self)
		elif len(self.vehicles[vehicle]) == 1:
			duration = self.distance(self,self.vehicles[vehicle][0])*2
		return duration

	# Vehicle load
	def vehicle_load(self,vehicle):
		return sum(c.q for c in self.vehicles[vehicle])

	# Depot load
	def get_load(self):
		return sum(c.q for c in self.customer_list)

	# Distance 
	def distance(self,c1,c2):
		return ((c1.x - c2.x)**2 + (c1.y - c2.y)**2)**0.5