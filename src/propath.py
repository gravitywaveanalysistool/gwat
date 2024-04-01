import os

def getProPath(proFile) -> str:
    if os.path.exists("pro/" + proFile):
        return "pro/" + proFile
    else:
        return "_internal/pro/" + proFile