Predicting Salmon Spawning Preference Through Number of Redds & River Parameters
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

##How the Program Works

The basis of the application attempts to match a fitting equation that uses 
parameters provided and outputs a predicted percent of redds constructed at the 
site with the data (of predicted percent of redds). We do this first by 
determining a likely equation which uses variables that are defined by the data 
and parameters (to be adjusted) to predict the percent of redds constructed. 
More on how to determine this equation will be discussed later.

After determining the equation, we make a guess at the values of the parameters. 
The tool can then be started and begins by using the first data point (percent 
of redds constructed) and the value of the variables at that time. This will 
produce a prediction of the percent of redds constructed. The program then 
repeats the process using this new data point and the values of the variables 
for the next time point to predict the following time point’s percent of redds 
constructed. The program then repeats this until predictions have been made for 
the full time period.

After all predictions have been made, the program then determines how well the 
predictions fit with the actual data. It does this by calculating the residuals 
(the difference between the actual data and the predicted data for a given time); 
the smaller the absolute value of the residual, the better the prediction was in 
accordance to the actual data. The overall metric is represented by the sum of 
the squares of the residuals.

The program then repeats this process by adjusting the values of the parameters 
(from their original guesses), comparing the predictions with the data, and then 
calculating the sum of the squared residuals. It then readjusts the parameters in 
attempt to decrease the sum. The program repeats this process until it determines 
the parameters cannot be adjusted anymore (within a threshold). In essence this 
is a least squares regression test where the user has defined the fit equation for 
the data.

##How to Use the Tool

The following explains how the GUI tool is used. Note that there might be a few 
issues in the graphics such as scrolling bars not appearing until window is re-
sized or not giving the user a warning when an invalid operation is attempted 
(other than any warnings in the Python terminal). However, the tool should be 
usable in the following manner even with these bugs.
