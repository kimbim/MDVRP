class Chromosome:
	def __init__(self,depots):
		self.depots = depots
		for d in self.depots:
			d.route_schedule()

	def __repr__(self):
		temp = []
		for d in self.depots:
			temp += d.customer_list
		return str(temp)

	def get_repr(self):
		temp = []
		for d in self.depots:
			temp += d.customer_list
		return temp
	
	def fitness(self):
		sum = 0
		for d in self.depots:
			if len(d.vehicles) > d.m: 
				sum += 40
			for vehicle in range(len(d.vehicles)):
				sum += d.route_duration(vehicle)
				if d.route_duration(vehicle) > d.D:
					sum += 40
				if d.vehicle_load(vehicle) > d.Q:
					sum += 40
		return sum

	def total_route_duration(self):
		sum = 0
		for d in self.depots:
			for vehicle in range(len(d.vehicles)):
				sum += d.route_duration(vehicle)
		return sum