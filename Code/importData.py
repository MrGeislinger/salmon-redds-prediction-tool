# Author: Victor Geislinger
import csv


# Imports data from data file, possibly with template, and returns tuple of keys
# and values (in array)
def importData(dataFile,dataTemplate="dataTemplate.csv"):
    '''
        Fetches data from a data file in CSV format.

        Reads in data from a given filename represented by dataFile by a
        specified template file represented by the optional variable
        dataTemplate (default is "dataTemplate.csv").

        Args:
            dataFile: A string of representing the name of the data file to be
                read which is formatted as CSV.
            dataTemplate: An optional variable that is a string representing the
                name of the data template. The default is "dataTemplate.csv".

        Returns:
            A tuple of list of keys representing what the values represent and a
            list of lists of values for each key from the data. For example:

            (
                ["Date-Start","Date-End","Number of Fish","Volume of Gravel (m^3)"],
                [
                    ["Sept-1996","Oct-1996","Nov-1996"],
                    ["Oct-1996","Nov-1996","Dec-1996"],
                    [200,300,150],
                    [520.5,432.5,126.0]
                ]
            )
    '''
    #storage array containers
    temp, values = [],[]
    #read file as a CSV file
    with open( dataFile, 'rb') as csvfile:
        #get row line with CSV format
        salreader = csv.reader(csvfile, delimiter=',', quotechar='\n')
        #save data type with row in tuple
        [temp.append(row) for row in salreader]

    #list of what values represent (title of column)
    keys = temp.pop(0)

    #get data format from file and save to array of types
    dataTypes = importDataTemplate(dataTemplate)

    #Use data types to decide how to handle format.
    #Convert values in each list appropiately based on data type.
    #Note that it is expected that `dataTypes` and `temp` have  the same length
    for (dataType,col) in zip(dataTypes,zip(*temp)):
        #convert each element in `col` and then save that into values array
        tempV = map( lambda x: convertByDataType(dataType,x),col)
        values.append( tempV )

    #gives a tuple of list of keys and a list of list of values
    return (keys, values)

#imports the file that will decide how to read formatted data
def importDataTemplate(dataTemplate="dataTemplate.csv"):
    '''
        Fetches the data types as given in dataTemplate.

        Reads a given filename represented by dataTemplate.

        Args:
            dataTemplate: A string representing the name of the data template where
                only the first line is considered. The default files is
                "dataTemplate.csv". For example:

            date("%d-%b-%y"->UTC),date("%d-%b-%y"->UTC),#(int),#(float)

        Returns:
            A list of strings that the template held representing each field.
    '''
    #temporary array to hold formatting file
    dataTypesArr =[]
    #look at how the data will be formatted
    with open( dataTemplate, 'rb') as csvfile:
        formatReader = csv.reader(csvfile, delimiter=',', quotechar='\n')
        [dataTypesArr.append(row) for row in formatReader]

    #save the first row as list of data types
    dataTypes = dataTypesArr[0]

    return dataTypes

#
def convertByDataType(dataType,value):
    '''
        Help Info
    '''
    #test against different data type
    #convert to number
    if dataType[0] == "#":
        #ignore the first "#" and remove "(" and ")"; just number
        numType = dataType[1:].replace("(","").replace(")","")
        #convert with default type if `numType` not given, else use type given
        return toNumberType(value) if value == '' \
                                   else toNumberType(value,numType)
    #convert to date
    elif dataType[:4] == "date":
        #split the date type info "(format,type)" -> ["format","type"]
        dateInfo = dataType[4:].replace("(","").replace(")","").split("->")

        #try to get dateInfo (at least format)
        try:

            #save after removing excess quotations
            dateFormat = dateInfo[0].replace("\"","")
        except: #nothing here (ignore excess info)
            return toDateType(value)

        #try to get what to convert to
        try:
            convertTo = dateInfo[1]
        except:
            return toDateType(value,dateFormat)

        #all of dateInfo was defined
        return toDateType(value,dateFormat,convertTo)
    #doesn't match any type
    else:
        print "NO TYPE MATCH: %s" %dataType
        return None



#defines a map to convert to a number or else return as `None`
def toNumberType( var , numType="float" ):
    '''
        Input: toNumberType( var , numType="float" )
        Output: number of given number type

        Will take in a variable and will try to convert it to the requested
        number type `numType` (defaults to `float`). If it's not possible to
        convert to that type then the variable `var` is converted to `None`.
    '''
    #dictionary of types of numbers
    numberType = {"int":int, "long":long, "float":float, "double":float}
    #try to convert
    try:
        #return as the type requested
        return numberType[numType](var)
    except:
        #`var` can't be converted to that type or
        #type requested is not in the dictionary
        return None



#defines a map to convert to a date or else return as `None`
def toDateType( dateStr , dateFormat="%d-%b-%y" , convertTo="UTC"):
    '''
        Input: toDateType( dateStr , dateFormat="dd-Mon-yy" , convertTo="UTC")
        Output: number of given number type

        Will take in a string `dateStr` and will try to convert it from the
        given date format `dateFormat` to the requested type `UTC`. If it's not
        possible to convert to that type then the variable `dateStr` is
        converted to `None`.

        The format parameter `dateFormat` is a string that defines how the
        `dateStr` will be formatted following a "datetime" object
    '''
    from calendar import timegm
    from datetime import datetime


    #dictionary of different variables to use in date's format
    #dateVars = {"UTC":"utc"}
    #try to convert
    try:
        #date string to given date format
        dt = datetime.strptime(dateStr, dateFormat)
    except:
        #`dateStr` can't be converted using that `dateFormat`
        return None
    if convertTo.lower() == "utc":
        #date in UTC (integer)
        convertedDate = timegm(dt.timetuple())

    #return the converted date
    return convertedDate
