import os

def getProPath(proFile) -> str:
    if os.path.exists("pro/" + proFile):
        return "pro/" + proFile
    else:
        return "_internal/pro/" + proFile
    
def getDataPath(filepath: str) -> str:
    if os.path.exists("data/" + filepath):
        return "data/" + filepath
    else:
        return "_internal/data/" + filepath