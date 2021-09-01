from io import StringIO
import re
from ruamel.yaml import YAML
import os


yaml = YAML()

dir = ""


def RemoveFileReference(input):

    refSplit = input.split("#")
    defPath = (
        "'#" + refSplit[1].replace("'", "").replace('"', "").replace("\n", "") + "'"
    )

    indents = refSplit[0].split("$ref:")

    return refSplit[0].split("$ref:")[0] + "$ref: " + defPath + "\n"


def nestedGet(dic, keys):

    for key in keys:
        dic = dic[key]
    return dic


def nestedSet(dic, keys, value):

    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def getPaths(input):

    input = input.replace("'", "").replace('"', "")
    paths = input.split("#")
    return paths[0], paths[1]


def find(key, dictionary, dir, file):

    for k, v in dictionary.items():
        if k == key:
            path, yamlPath = getPaths(v)
            if path == "":
                yield os.path.join(dir, file + v)
            else:
                if not os.path.isabs(path):
                    yield os.path.join(dir, v)
                else:
                    yield v
        elif isinstance(v, dict):
            for result in find(key, v, dir, file):
                yield result
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    for result in find(key, d, dir, file):
                        yield result


def process(inFile, outFile):

    inFile = os.path.abspath(inFile)
    dir = os.path.dirname(inFile)

    refObjects = dict()
    yamlParsed = dict()

    inFileStream = open(inFile)
    inFileParsed = yaml.load(inFileStream)
    yamlParsed[inFile] = inFileParsed
    references = list(find("$ref", inFileParsed, dir, inFile))

    while references:
        checkRef = references.pop(0)
        apiFile, defintionpath = getPaths(checkRef)
        defintionpathSplit = defintionpath.split("/")
        if apiFile not in yamlParsed:
            f = open(apiFile)
            yamlParsed[apiFile] = yaml.load(f)
            f.close()

        input = nestedGet(yamlParsed[apiFile], defintionpathSplit[1:])
        references.extend(list(find("$ref", input, dir, apiFile)))
        nestedSet(refObjects, defintionpathSplit[1:], input)

    keys = list(refObjects.keys())
    for key in keys:
        if key in inFileParsed:
            del inFileParsed[key]

    yamlFileWriter(inFileParsed, outFile, "w")
    yamlFileWriter(refObjects, outFile, "a")

    inFileStream.close()
    print("All Done. output file: ", outFile, u"\U0001f604")


def yamlFileWriter(inputDictionary, fileName, mode):

    file = open(fileName, mode)

    fim = StringIO()
    yaml.dump(inputDictionary, fim)
    fim.seek(0)

    for line in fim:
        outputLine = line
        if "$ref:" in line:
            outputLine = RemoveFileReference(outputLine)

        file.writelines(outputLine)

    file.close()
