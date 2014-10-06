import numpy as np # `array`
# import scipy as sp
from scipy.optimize import leastsq
from pylab import *
from importData import *
import sys
import time
graphics = 0
if graphics:
    from visual import *

#
def predict_funct(alpha, x0, parameters, equation, rangeOfVars,
                  dt=1, tmin=0, tmax=7, pastPred={}):
    '''
        predict_funct(
                       alpha, x0, parameters, equation, rangeOfVars,
                       dt=1, tmin=0, tmax=7, pastPred={}
                     )

        `alpha` is an array of coefficients for use in the fitting equation.
        `x0` is the initial percentage of redds constructed in river.
        `parameters` is an array organized by time of tuples of the data
        `equation` is a function that takes in `alpha`, a previous `x` value,
            and a tuple of parameters for a certain time and returns a predicted
            value. Ex: eq(alpha,x,param).
        `rangeOfVars` is a range of parameter variables that will be used in the
            function `equation`. Note the range will default to all the
            variables in `parameter`'s tuple.
        `dt` is the increase in time.
            -> dt=1 (1 year) by default
        `tmin` is when time should start.
            -> tmin=0 by default
        `tmax` is when time should stop. Note it must be a multiple of `dt`.
            -> tmax=7 by default
        `pastPred` is a dictionary of predictions. Useful for combining results.
            -> pastPred={} by default

        Gives a dictionary of predicted percentage of salmon redds constructed
        at a given site over a period of time. The prediction will skip over
        missing parameter variables to be used (as defined by `rangeOfVars`) and
        use the previous two points to linearly find the next "missing" point.
        Required that (tmin - tmax) is a multiple of dt.
    '''
    # Prepare prediction dictionary (copy the dictionary contents)
    prediction = pastPred.copy()
    # Add initial data point (x is the resulting variable; focus of simulation)
    x = x0

    # Iterate over time
    for t in np.arange(tmin,tmax,dt): #change to make it integers
        # Add point into prediction dictionary
        prediction[t] = x
        # Get parameter at `t`
        try:
            param = parameters[t]
            # Default that no `None` was detected
            detectedNone = False
            # Check only used variables
            for pos in rangeOfVars:
                # Check if this value is `None` (implies empty)
                if parameters[t][pos] == None:
                    # Set that `None` value was found and break out
                    detectedNone = True
                    break
        # Failed to get parameter, equivalent to `None`
        except:
            detectedNone = True

        # Check if there is a missing data point
        if detectedNone:
            # Guess missing data point with previous measurements w/ linear eq
            x = guessEquation("linear","pre",prediction,t,dt)
        else:
            # Use user-defined equation
            x = equation(alpha,x,param)

    # Add last predicted data point
    prediction[tmax] = x

    ## Convert `prediction` to array
    # Save as a sorted array (by key) of tuples -> (key,value)
    temp = prediction.items(); temp.sort()
    # Add just values into array
    prediction = [item[1] for item in temp]
    # Return an array to do numpy/scipy stuff to
    return np.array(prediction)

# Find residuals using `alpha` between data and prediction (of one site)
def resid(alpha, data, parameters, equation, rangeOfVars):
    '''
        Returns an array of the differences between predicted values (based on
        parameters) and given data for a given site.
    '''
    # Save array of predictions
    pred = predict_funct(alpha, data[0], parameters, equation, rangeOfVars,
                         tmax=len(data)-1 )
    # Iterate to find all differences between prediction and data for each time
    err = []
    for i in range(len(pred)):
        # Attempt to get difference between prediction and data points
        try:
            d = data[i]
            p = pred[i]
            # Test tha
            e = p - d
        # Getting data failed, make the error 0 (no effect)
        except:
            e = 0
        err.append(e)
    # Return a numpy array of differences
    return np.array(err)

# Find residuals using `alpha` between data and parameters for all sites
def residAll(alpha, dataAll, parametersAll, equation, rangeOfVars):
    '''
        Returns an array of arrays of the differences between predicted values
        (based on parameters) and given data for multiple arrays. Similar to the
        `resid` function.
    '''
    errTotal = np.array([])
    for data in dataAll:
        # Place `resid` array into errTotal np.array
        errTotal = concatenate( (errTotal,\
                                 resid(\
                                    alpha,\
                                    data,\
                                    parametersAll,\
                                    equation,\
                                    rangeOfVars)
                                ))
    return errTotal

# Perform a fit test for multiple sites
def fit_data(alpha, data, parameters, equation, rangeOfVars,
             paramName, dt, years=np.arange(1997,2005,1), Graph=True):
    '''
        fit_data(alpha, data, parameters, equation, rangeOfVars,
                 paramName, dt, years=np.arange(1997,2005,1), Graph=True)

        First line is the useful things to make predictions.
        Second line is for plotting (not directly useful for prediction).
    '''
    # For plotting:
    t_window = len(data[0])
    n_window = t_window/dt
    t_range = np.arange(0,t_window,dt)
    # Fitting function is just the prediction
    # Perform fitting:
    alphaNew, success = leastsq( residAll,
                                 alpha[:],
                                 args=(data, parameters, equation, rangeOfVars))
    # Make an empty prediction array same size as the data
    pred = [0]*len(data)

    for i in range(0,len(pred)):
        # Compare predicted data
        pred[i] = predict_funct(alphaNew,
                                data[i][0],
                                parameters,
                                equation,
                                rangeOfVars,
                                dt,
                                tmax = (len(data[i])-1)*dt,
                                pastPred = {}
                                )

        print "\nFitting parameters for Site %d with parameters:\n"\
                %(i), alphaNew
        # Print results side-by-side
        print "Actual     Predicted  Squared-Difference"
        for x,y in zip(data[i],pred[i]):
            # Attempt to get the squared-difference
            try:
                print "%8.5f  %8.5f  %9.3e" % (x,y,(x-y)**2)
            except:
                print " Diffence couldn't be found"
        print "\n"

    # Plot individual sites with predictions
    # Graph the data and the fit
    # for i in range(0,len(pred)):
        # since first figure is taken
        print len(pred[i]) , pred[i]
        print len(data[i]) , data[i]
        figure(i+1)
        if Graph:
            xlabel("t")
            ylabel("Percent of Redds Constructed at Site")
            title("Percent of Redds Constructed at Site [%d-%d]"
                    %(years[0],years[-1]) )
            plot(t_range,pred[i],label="Site %d Prediction" %(i) )
            plot(t_range,data[i],label="Site %d Data" %(i) )
            legend( bbox_to_anchor=(0., 1.02, 1., .102),
                    loc="best",
                    ncol=2,
                    mode="expand",
                    borderaxespad=0.)
            savefig("figure_%s_%d.png" %(paramName,i)  )
    # Present all firgures at execution
    close()
    return alphaNew

# Do a guess based on what type of guess
def guessEquation(eqType,preORpost,pred,t,dt):
    if eqType == "linear":
        return linearGuessEq(preORpost,pred,t,dt)

# Do a linear guess for the data point
def linearGuessEq(preORpost,pred,t,dt):
    if preORpost == "pre":
        # Check that previous points are defined
        if t >= 2: #get that we aren't at the second point
            # Find the past two points
            x1 = pred[t-dt]
            x0 = pred[t-2*dt]
            dx = x0-x1
            # Final guess x - x1 = m * (t-(t-dt)), note m=dx/dt
            x  = dx + x1
            return x
        # Default to post-prediction guess if the first two points...?
        else:
            return linearGuessEq("post",pred,t,dt)
    ## Still working on getting this (if possible)
    # # If chosen to do post-prediction guess
    # elif preORpost == "post":
    #     # If the last point, default to pre-prediction guess
    #     if t == len(pred) - 1: #will have to get the greatest key
    #         return linearGuessEq("pre",pred,t,dt)
    #     # Check that not the first point
    #     if t > 0:
    #         # Will need to be sure that this won't fail...
    #         x0 = pred[t-dt]
    #         x2 = pred[t+dt]
    #         #
    #         dx = x2 - x0
    #         x  = dx + x0
    #         return x
    #     # If this is the first point
    #     else:
    #         return 0
    # Doesn't match any kind of guess
    else:
        return None

# # Possibily use this to prevent errors.
# # Get the next or previous point
# def getPt(nextORprev,pred,t,dt):
#     # Dictionary for whether to take next or previous data point
#     incORdec = { "next":dt,   1:dt,  "+":dt,
#                  "prev":-dt, -1:-dt, "-":-dt, "previous":-dt}
#     # Get the next/previous time
#     tn = t + incORdec[nextORdec]
#     # Attempt to get this data point
#     try:
#         ptMaybe = pred[tn]
#     # Point not found in dictionary
#     except:
#         # Get a different point
#         return pred[t]
#     # Return the point or find the next/previous point if `None`
#     return ptMaybe if ptMaybe != None\
#                    else getPt(nextORprev,pred,tn,dt)
