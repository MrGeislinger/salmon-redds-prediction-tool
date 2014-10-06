Predicting Preference of Salmon Spawning Preference Through Number of Redds & River Parameters
============================

## Quick Summary of Project

Salmon redds (salmon nests) prediction/modeling Python tool. 
Reads data of a river/spawning area parameters and attempts 
to predict future spawning. 

Special thanks to Joshua Deutsch and Joseph Merz for guidance 
throughout this project. Originally for Master's Thesis in 
Computational Physics at University of California, Santa Cruz 
in investigating the benefit of adding gravel to make site 
more desirable for spawning.

The tool is meant to give a better idea of salmon spawning 
preference to a given site by predicting the precentage of 
redds at sitecompared to the total redds in the river. The
tool reads in CSV files (one for data and one for easy 
formatting) and ask for a user's guess at the equation for
the mathematical model. The program then adjusts constants
found in the user-given equation until the model and data
fall within a threshold. The program exits by giving the
values for the constants as well as a graph *(Year vs. 
Percent of Redds)* of both the data and model values.



