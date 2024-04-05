import os

# assumes working directory is the root of the project
def getProPath(proFile) -> str:
    """
    @param proFile:
    @return:
    """
    if os.path.exists("pro/" + proFile):
        return "pro/" + proFile
    else:
        return "_internal/pro/" + proFile
    
def getDataPath(filepath: str) -> str:
    """
    @param filepath:
    @return:
    """
    if os.path.exists("data/" + filepath):
        return "data/" + filepath
    else:
        return "_internal/data/" + filepath