import json

def liste(file, var, mode="str"):
    fileContent = str(open(file, "r").read())
    if var + "=" in fileContent:
        var = var + "="
    elif var + " = " in fileContent:
        var = var + " = "
    else:
        print("[-] No equal in your file")
    try:
        start = fileContent.index(var) + len(var)
        end = fileContent.index("\n", start)
        fileContent = fileContent[start:end]
    except:
        return str(fileContent.split(var)[len(fileContent.split(var))-1])
    
    if ", " in fileContent:
        var = ", "
    elif '", "' in fileContent:
        var = '", "'
    elif "', '" in fileContent:
        var = "', '"
    else:
        print("[-] No find list in your var")
    fileContent = fileContent.replace("[", "").replace("]", "").replace("['", "").replace("']", "").replace('["', "").replace('"]', "")
    if mode == "str":
        return fileContent.split(var)
    if mode == "int":
        return list(map(int, fileContent.split(var)))



def string(file, var):
    fileContent = str(open(file, "r").read())
    if var + "=" in fileContent:
        var = var + "="
    elif var + " = " in fileContent:
        var = var + " = "
    else:
        print("[-] No equal in your file")
    try:
        start = fileContent.index(var) + len(var)
        end = fileContent.index("\n", start)
        return str(fileContent[start:end])
    except:
        return str(fileContent.split(var)[len(fileContent.split(var))-1])



def integer(file, var):
    fileContent = str(open(file, "r").read())
    if var + "=" in fileContent:
        var = var + "="
    elif var + " = " in fileContent:
        var = var + " = "
    else:
        print("[-] No equal in your file")
    try:
        start = fileContent.index(var) + len(var)
        end = fileContent.index("\n", start)
        return int(fileContent[start:end])
    except:
        return int(fileContent.split(var)[len(fileContent.split(var))-1])



def dictionary(file, var=None):
    if var == None:
        return json.loads(str(open(file, "r").read()))
    else:
        fileContent = str(open(file, "r").read())
        if var + "=" in fileContent:
            var = var + "="
        elif var + " = " in fileContent:
            var = var + " = "
        else:
            print("[-] No equal in your file")
        try:
            start = fileContent.index(var) + len(var)
            end = fileContent.index("\n", start)
            return dict(fileContent[start:end])
        except:
            return dict(fileContent.split(var)[len(fileContent.split(var))-1])