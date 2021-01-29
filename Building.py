class Building():
	"""A simple Building Energy Model.
	Consisting of one thermal capacity and one resistance, this model is derived from the
	hourly dynamic model of the ISO 13790. It models heating and cooling energy demand only.
	Parameters:
		* heat_mass_capacity:           capacity of the building's heat mass [J/K]
		* heat_transmission:            heat transmission to the outside [W/K]
		* maximum_cooling_power:        [W] (<= 0)
		* maximum_heating_power:        [W] (>= 0)
		* time_step_size:               [s]
		* conditioned_floor_area:       [m**2]
	"""

	def __init__(self, heat_mass_capacity, heat_transmission,
				 maximum_cooling_power, maximum_heating_power, time_step_size,
				 conditioned_floor_area, heating_setpoint, cooling_setpoint, outside_data):

		if maximum_heating_power < 0:
			raise ValueError("Maximum heating power [W] must not be negative.")
		if maximum_cooling_power > 0:
			raise ValueError("Maximum cooling power [W] must not be positive.")

		# CONSTANT VALUES
		self.__heat_mass_capacity = heat_mass_capacity
		self.__heat_transmission = heat_transmission
		self.__maximum_cooling_power = maximum_cooling_power
		self.__maximum_heating_power = maximum_heating_power
		self.__time_step_size = time_step_size
		self.__conditioned_floor_area = conditioned_floor_area
		self.heating_setpoint = heating_setpoint
		self.cooling_setpoint = cooling_setpoint

		# VARYING VALUES
		self.outside_data = outside_data
		self.current_heating_cooling_power = None
		self.current_int_temperature = None
		self.current_ext_temperature = None
		self.current_time_interval = None

		
		#data generator
		# def next_ext_data():
		#     while True:
		#         for i in range(len(self.outside_data)):    
		#             temp, time = self.outside_data.iloc[i, :]
		#             yield temp, time

		def create_actionspace():
			i = 0
			j = self.__maximum_cooling_power

			action_space = {}

			while j <= self.__maximum_heating_power:
				action_space[i] = j
				i += 1
				j += 500

			return action_space

		#self.ext_data_generator = next_ext_data()
		self.action_space = create_actionspace()

	def next_ext_data(self):
		while True:
			for i in range(len(self.outside_data)):    
				temp, time = self.outside_data.iloc[i, :]
				yield temp, time

	def initialize_state(self, initial_int_temp):
		self.current_int_temperature = initial_int_temp
		self.current_heating_cooling_power = None
		self.ext_data_generator = self.next_ext_data()
		self.update_ext_data()

		return self.current_state()

	def update_ext_data(self):
		"""
			External Temperature and Time Interval getting updated by the data generator
		"""
		self.current_ext_temperature, self.current_time_interval = self.ext_data_generator.__next__()


	def predicting_step(self):
		"""
		Predicts by formula the appropriate heating/cooling power to maintain the temperature 
		within setpoints
		"""

		def next_temperature(heating_cooling_power):
			return self._next_temperature(heating_cooling_power = heating_cooling_power)

		next_temperature_no_power = next_temperature(0)

		# if temperature is within limits by the system being off, do nothing return power as 0
		if (next_temperature_no_power >= self.heating_setpoint and
				next_temperature_no_power <= self.cooling_setpoint):
			return 0
		# Else, devise a way to determine the required heating/cooling required
		else:
			if next_temperature_no_power < self.heating_setpoint:
				setpoint = self.heating_setpoint
				max_power = self.__maximum_heating_power

			else:
				setpoint = self.cooling_setpoint
				max_power = self.__maximum_cooling_power

			ten_watt_per_square_meter_power = 10 * self.__conditioned_floor_area
			next_temperature_power_10 = next_temperature(ten_watt_per_square_meter_power)

			unrestricted_power = (ten_watt_per_square_meter_power *
								  (setpoint - next_temperature_no_power) /
								  (next_temperature_power_10 - next_temperature_no_power))

			if abs(unrestricted_power) <= abs(max_power):
				return unrestricted_power
			else:
				return max_power
				
			# next_temperature_heating_cooling = next_temperature(self.current_heating_cooling_power)
			# self.current_int_temperature = next_temperature_heating_cooling

	def _next_temperature(self, heating_cooling_power):
		"""
			Based on the current status of building and input heating cooling power, predict the
			next temperature.
		"""
		dt_by_cm = self.__time_step_size.total_seconds() / self.__heat_mass_capacity

		return (self.current_int_temperature * (1 - dt_by_cm * self.__heat_transmission) +
				dt_by_cm * (heating_cooling_power + self.__heat_transmission * self.current_ext_temperature))

# state : time_interval, current_int_temperature, current_ext_temperature
# state will be input to agent and agent will give amount of heating_cooling_power that will be needed to be applied
# heating_cooling_power will the action that will be taken

	def step(self, action):
		"""
			Input : heating cooling power
			Output :  Should return the Next temperature, Reward 
		"""
		self.current_heating_cooling_power = self.action_space[action]

		# calculate new Temperature
		next_temperature = self._next_temperature(self.current_heating_cooling_power)
		#print(self.cooling_setpoint, next_temperature, self.heating_setpoint)

		# scaling reward factor for temperature range penalty
		L = 10
		# Cost of provding heating or cooling
		#print(self.current_heating_cooling_power)
		#operation_cost = - abs(self.current_heating_cooling_power) 

		# Cost of temperature going outside the desired range of set points

		out_of_bounds_cost = abs(next_temperature - self.cooling_setpoint) + abs(next_temperature - self.heating_setpoint)

		# As going out of bounds is more costly for us
		# total_cost = operation_cost - L * out_of_bounds_cost
		if self.cooling_setpoint <= next_temperature <= self.heating_setpoint :
			total_cost = 0
		else:
			total_cost = -L * out_of_bounds_cost

		

		# Updating to new state
		self.current_int_temperature = next_temperature
		self.update_ext_data()

		return self.current_state(), total_cost


	def current_state(self):
		return [self.current_time_interval, self.current_int_temperature, self.current_ext_temperature]