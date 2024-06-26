# Conceptual Tests

### utils.py/runGDL.py
```
run_gdl(file_in, latitude, gdl_or_idl)

file_in: string. expected to be a file path pointing to a radiosonde test file.
file_out: string. expected to be a file path.
latitude: number.
gui: ctk context.

-> side effect: file at the location of file_out contains 16 parameters
 | file_in not found error
 | unable to write file_out error
 | malformatted file_in error
 
 Test Case 1: valid input file
 Objective: Successfully pass a valid input to GDL
 Input: filepath to a valid radiosonde txt file
 Output: A txt file containing 16 parameters with 8 for each troposphere and stratosphere
 
 run_gdl("T3_1800_Artemis_Rerun.txt", -35, gdl_or_idl) -> 16 GW parameters stored in a txt fil ein the tmp directory
 
 Test Case 2: bad input file
 Objective: Detect that GDL returned a bad file error and communicate to the user that their data was bad
 Input: A malformated txt file
 Output: GDL error popup in UI
 
 run_gdl("SuperbadDataFile.txt",-35,gdl_or_idl) -> GDL error
 
 Test Case 3: Invalid filepath/File not found
 Objective: Detect that the input data file 
 Input: A non-existent filepath
 Output: Alert User of invalid file path error
 
 run_gdl("..",-35,gdl_or_idl) -> File not found error
 
```

```
read_params(file_in)

file_in: string. expected to be a file path pointing to a file generated by run_gdl().

-> 16 parameters from file at file_in
 | file_in not found error
 | malformatted file error
 
Test Case 1: Valid input file
Objective: Return retrieved parameters from troposphere/stratosphere
Input: A correct filepath to the temp file created by GDL
Output: A list of parameters from the temp file
read_params(GoodFilepath) -> tropo and strato parameters as dictionaries

Test Case 2: Invalid Input File
Objective: Return a malformatted data error
Input: Filepath pointing to a .txt file that is not the temp file created by GDL
Output: Malformatted data error
read_params(badFilepath) -> Malfromatted data error to UI

Test Case 3: Filepath not a .txt file
Objective: Detect if the filepath is pointing to a directory or non-txt file
Input: Filepath to non-txt data file/directory
Output: Non-txt file error
read_params(non-txt filepath/directory filepath) -> Invalid file format error 
```

```
save_params_to_file(strato_params, tropo_params, file_out)

strato_params: dict(string, number). a dictionary with name -> value.
tropo_params: dict(string, number). " " 
file_out: string. expected to be a file path.

-> side effect: text file at file_out with labeled troposphere and stratophere parameters
 | filename not found error
 | failed to write file error
 
 Test Case 1: Good Parameters, Good filepath
 Objective: Have the method successfully save the parameters to a .txt file at the specified location
 Input: Good Strato,Tropo data and Good filepath
 Output: A .txt file at the target directory containing 16 parameters
 save_params_to_file(goodStrato, goodTropo, filepath) -> .txt file representing formatted strato/tropo values
 
 Test Case 2: Bad paramter(s), Good filepath
 Objective: Cancel creation of the .txt file dur to bad data
 Input: Either one or both of the input parameters containing bad data, but a good filepath
 Output: No output except for an error message to the UI
 save_params_to_file(stratoData, tropoData, filepath) -> UI response that an error occured
 
 Test Case 3: Good Parameters, Bad filepath
 Objective: Cancel creation of .txt file and alert user of bad filepath
 Input: Good Strato/Tropo, Bad filepath (non-existent directory,etc.)
 Output: Bad filepath error message to user
 save_params_to_file(stratoData, tropoData, badFilepath) -> Bad Filepath Error 
```

```
save_graph_to_file(graph_objects, file_out, selected_graphs, gui)

graph_objects: dict(string, graph). a dictionary with name -> graph
file_out: string. expected to be a file path.
selected_graphs: dict(string, string). a dictionary with name -> "strato" | "tropo" | "all".
gui: ctk context.

-> side effect: pdf file at file_out with each of the selected graphs.
 | unable to write to file_out error 
```

# Conceptual Tests
### ParseData.py
```
headerData(rawData, Encoding)

rawData: String. Expected to be a TxT file / File Path
Encoding: Defaulted to ISO-8859-1

Test Case 1: File With Complete Header Data
Objective: Identify  the start and ends lines of the raw data file when both 'Launch Data:' and 'Profile Data:' Occur
Input: TxT file of raw profile data from radiosonde
Output: two ints for the start_line and end_line
headerData('T3_1800_ARTEMIS_RERUN.TXT, ISO-8859-1) ->  start_line, end_line

Test Case 2: File Without HeaderData
Objective: Test functions behaviour when 'Launch Data' is missing
Input: TxT File without Launch
Output: None for both start_line, end_line
headerData('T3_1800_ARTEMIS_RERUN.TXT, ISO-8859-1) ->  None, None

```
```
grabProfileData(rawData, encoding)

rawData: String. Expected to be a TxT file / File Path
Encoding: Defaulted to ISO-8859-1

Test Case 1: File with complete Profile Data
Objective: Identify the start end lines of the raw data file when both 'Profile Data' and 'Tropopauses' occur
Input: TxT file of raw profile data from radiosonde
Output: two ints for the start_line and end_line
grabProfileData('T3_1800_ARTEMIS_RERUN.TXT, ISO-8859-1) -> start_line, end_line

Test Case 2:
Objective: Test function behavior when 'Profile Data' and/or 'Tropopauses' is missing
Input: Raw data file without 'Profile Data' or/and 'Tropopauses' text
Output: None for both start_line and end_line
grabProfileData('T3_1800_ARTEMIS_RERUN.TXT, ISO-8859-1) -> None, None
```
```
get_tropopause_value(file_path)
Test Case 1: Tropopause Value Present
Objective: Validate that the function extracts the tropopause value from the specified file.
Input: Raw data file with tropopause value.
Output: The function should return the correct tropopause value as a float.
get_tropopause_value('T3_1800_ARTEMIS_RERUN.TXT') -> Tropopause Value

Test Case 2: Tropopause Value Not Present
Objective: Ensure proper behavior when tropopause value is not found in the file.
Input: Raw data file without tropopause value.
Output: The function should return None.
get_tropopause_value('T3_1800_ARTEMIS_RERUN.TXT') -> Raise Error of no tropopause value
```
```
get_latitude_value(file_path)
Test Case 1: Latitude Value Present
Objective: Confirm that the function retrieves the latitude value from the given file.
Input: Raw data file with latitude value.
Output: The function should return the correct latitude value as a string.
get_latitude_value('T3_1800_ARTEMIS_RERUN.TXT') -> latitude Value

Test Case 2: Latitude Value Not Present
Objective: Verify the function's behavior when latitude value is not found in the file.
Input: Raw data file without latitude value.
Output: The function should return False (May change to defaulting to oswego latitude)
get_latitude_value('T3_1800_ARTEMIS_RERUN.TXT') -> False Raise Error
```

```
generate_profile_data(file_path, gui)
Test Case 1: Generation of Profile Data that is complete
Objective: Function generates the full profile dataframe as well as troposphere and stratosphere dataframe
Input: Raw data file path and GUI reference.
Output: Station object containing parsed data, or appropriate error handling in the GUI if an exception occurs.

Test Case 2: Generation where Profile Data that contains non numeric characters
Objective: Function throws error gui to user stating where the non numeric error occured for them to fix
Input: Raw data file and GUI reference.
Output: Error GUI frame to user stating where it occured
generate_profile_data(file_path, gui) - > [Error Occured: Cannot parse "-      " at Line 2069! Please Follow Specified Format."]

Test Case 3: Generation where Profile Data does contain Tropopause Value
Objective: Function throws error gui to user stating that there is no tropopause occuring in the file
input: Raw data file path and GUI reference
Output: Error GUI frame to user stating there is no Tropopause Value
```



tests for save graph probably cannot be implemented.
