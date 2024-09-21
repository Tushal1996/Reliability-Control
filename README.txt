About the Project

Reliability Control

Reliability Control is the high-level control strategy for wind turbine systems. They detect the current degradation state of the wind turbine component and feed this information back to the operational control. Closed-loop reliability control is comprised of the detection of the current degradation state, the determination of the required turbine configuration, and an adjustment of the operational controllers. Reliability control thus autonomously adjusts the behavior of a standard turbine to its site conditions. The closed-loop reliability control is implemented in the Python programming environemnt. Automated reliability control contributes to a reduction in the cost of energy.      


 

Input_LaHauteBorne folder -> This folder has lookup tables for La Haute Borne wind farm including La Haute Borne SCADA data and B-value function.

Input_Lillgrund folder -> This folder has lookup tables for Lillegrund wind farm including Lillegrunfd SCADA data and B-value function. There is a folder for LifetimeDels_IWT7_5 which has Lifetime_DEL value computed for different turbine configurations. There is a folder called ParetoOptimalLookUpTable, which contains optimal configurations.

LongtermSimulation folder -> In Simulations sub-folder, you will find 1) the pareto_front_computation.py file which computes the alpha value for each optimal configuration; 2) ReliabilityControllerSimulator.py file is the PI-controller file, whereas WindSimulator.py is the wind turbine model file where pre-simulation lookup table are loaded. 3) simulateLillegrund.py file calls the ReliabilityControllerSimulator.py and WindSimulator.py and performs long-term simulation.
                          -> LoadGainSchedulingLookUpTable.py file loads the PI-controller gain values for scheduling based on wind condition.
                          -> LoadWindSimulationLookUpTable.py file loads the pre-simulation lookup table.
                          -> InterpolationFunction.py file does interpolation.
