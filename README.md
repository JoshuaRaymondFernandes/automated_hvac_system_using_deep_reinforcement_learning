<h1> Automated HVAC system using deep reinforcement learning </h1>

HVAC stands for heating, ventilation and Air conditioning. Majority offices and closed spaces have HVAC systems which are set in place to control the room temperature and humidity. Usually these systems are manually controlled or controlled by some preset logic to operate on. It becomes crutial to set these rules by which to operate the HVAC system accurately for majorly 2 reasons : Meeting the requirements of the room environment and secondly, cost and efficiency.

As cost can differ alot based on how the HVAC system is operated, in this project I attempt to control the cooling / heating output of an HVAC system based on the following parameters :

A) Fixed parameters :

  1) heat_mass_capacity : capacity of the building's heat mass [J/K]
  2) heat_transmission:            heat transmission to the outside [W/K]
  3) maximum_cooling_power:        [W] (<= 0)
  4) maximum_heating_power:        [W] (>= 0)
  5) time_step_size:               [s]
  6) conditioned_floor_area:       [m**2]

B) Variable parameters :

  7) current heating / cooling power
  8) current internal temperature
  9) current external temperature
  
Based on these 9 parameters at particular time t, the heating/cooling power at the next time interval t+1 is decided. This decision of deciding the heating cooling power is where the cost factor is affected. Different systems will give different outputs and their efficiency will be measured based on the cost difference.

In this model I have used a Deep Q-Learning model to learn from the data and run the predictions. For the data of external temperture I have used open source external temperature data. This data is combined and cleaned in <b>datacleaning.ipynb.</b>

In the notebook <b>temperature_simulator_collab.ipynb</b>,  I have created a class Building which has all the fixed parameters associated to it. Based on the new heating and cooling power decided by the model, the building's temperature changes and then this new temperature along with the heating cooling power is used to predict the next step.

As shown, after training and running the model, the new system shows significantly better performance than conventional formula based HVAC systems. By training the model on more data, it will get more robust and better


