# Used for the actual regression analysis
import ols
from numpy import asarray
from scipy import empty

# Perform a regression anlaysis on an multi-dimensiaonal array
def regressionAnalysis( percentRedds, varArray, nameArray, siteRange=range(0,3) ):
    '''
        * percentRedds -> 2D array of sites vs. percent of redds constructed at
                          site.
                          Ex: [ [0.2,0.4,0.1,...], [0.1,0.6,0.2], ... ]
        * varArray -> 2D array of types of variables vs. 2D array of sites vs.
                      data of variable at site.
                      Ex: [ [ [13,26,...], ... ], .... ]
        * nameArray -> Array of names of varaibles defiend in `varArray`
                       Ex:
        * siteRange -> Range of what sites to use
                       Ex: range(0,2) or [2,3]

    '''
    # constructed redd percentage ([]->asarray)
    y = [ asarray(arr) for arr in percentRedds ]
    # empty list of "n-dimensions" [var1,var2,var3,...]
    nDim = len(varArray)
    x = [ empty( [len(arr),nDim] ) for arr in y ]

    # #use the total range of sites
    # if siteRange ="all":
    #     siteRange = range(0,len(percentRedds))
    # #use up to max site number
    # else:
    #     siteRange = range(0,siteRange)


    #perform the regression for all sites available
    for i in siteRange:
        j = 0
        # get just the variables for site `i` from `varArray`
        tempVarArray = []
        for vars in varArray:
            # save variable array for specific site `i`
            tempVarArray += [vars[i]]
        # create zipped array of variables in site `i`
        zipVarArray = zip(*tempVarArray)
        # iterate over each year in site
        for varTuple in zipVarArray: #zipVarArray -> zip(var1[i],var2[i],...)
            # convert tuple of vars to an array of vars
            xTemp = [ var for var in varTuple ]
            x[i][j] = xTemp
            j += 1
        # use `ols` build for linear regression
        # possibly better to do different regression, like logistic?
        model = ols.ols(y[i],x[i],'y:Precent of Redds',nameArray)
        # return coefficient p-values
        names = '[coeff,' + ','.join(nameArray) + ']'
        print names+':\n', model.p
        # print results
        print model.summary()

# Replaces None with 0 within inner arrays
def nonesToZero(tempSites,sites=[[],[],[]]):
    '''
    '''
    for (temp,values) in zip(tempSites,sites):
        #iterate over the inner array
        for i in range(len(temp)):
            temp0 = [] #tempary storage array to build
            for val in temp[i]:
                if val != None: #place value in inner arry as normal
                    temp0.append(val)
                else: # None -> 0 within inner array
                    temp0.append(0)
            values.append(temp0)
    return sites

## Removes None within the inner arrays
## Note that this will only work if the rest of the
## inner arrrays have None in the same position(s)
def removeNones(tempSites,sites=[[],[],[]]):
    '''
    '''
    for (temp,values) in zip(tempSites,sites):
        #iterate over the inner array
        for i in range(len(temp)):
            temp0 = [] #tempary storage array to build
            for val in temp[i]:
                if val != None: #place value in inner arry as normal
                    temp0.append(val)
                # ignore values of None (essentially removing from final data)
            values.append(temp0)
    return sites


# dictionary to hold what actions to take
noneDataAction = {"removeNone":removeNones, "convertToZero":nonesToZero}
