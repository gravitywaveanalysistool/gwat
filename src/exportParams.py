"""
Parameters are stored in UI as a Python dictionary with ParameterName -> Value
Need: output file path, parameter dictionary
To add: right alignment needed for larger values to prevent key-value clipping in output
"""


def exportParams(parameterDictionary, filePath):
    file = open(filePath, 'w')
    longestKeyName = 0  # For keeping track of how much to indent value
    for key in parameterDictionary:
        if len(key) > longestKeyName:
            longestKeyName = len(key)

    for key, value in parameterDictionary.items():
        difference = longestKeyName - len(key)  # Controls how much to indent the value as to line up values in a column
        line = key + ("{:>" + str(difference+8) + "}").format(str(value)) # +8 is an output formatting preference
        file.write(line + "\n")
    file.close()
