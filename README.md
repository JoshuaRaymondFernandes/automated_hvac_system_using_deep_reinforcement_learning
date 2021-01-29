<h1> Automated HVAC system using deep reinforcement learning </h1>

HVAC stands for heating, ventilation and Air conditioning. Majority offices and closed spaces have HVAC systems which are set in place to control the room temperature and humidity. Usually these systems are manually controlled or controlled by some preset logic to operate on. It becomes crutial to set these rules by which to operate the HVAC system accurately for majorly 2 reasons : Meeting the requirements of the room environment and secondly, cost and efficiency.

As cost can differ alot based on how the HVAC system is operated, in this project I attempt to control the cooling / heating output of an HVAC system based on the following parameters :

A) Fixed parameters :

  <ul>heat_mass_capacity </ul>

		heat_mass_capacity:           capacity of the building's heat mass [J/K]
		* heat_transmission:            heat transmission to the outside [W/K]
		* maximum_cooling_power:        [W] (<= 0)
		* maximum_heating_power:        [W] (>= 0)
		* time_step_size:               [s]
		* conditioned_floor_area:       [m**2]
