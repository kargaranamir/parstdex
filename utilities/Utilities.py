from hazm import *

def DateNormalize(sentence):
    # match = re.search(r'(\d+\s+/\s+\d+\s+/\s+\d+)','The date is 11/ 12/98')
    match = sentence.replace("/ ", "/")
    match = match.replace(" /", "/")
    match = match.replace("- ", "-")
    match = match.replace(" -", "-")
    match = match.replace(" :", ":")
    match = match.replace(": ", ":")
    
    normalizer = Normalizer()
    normalizer.normalize(match)
    return match

def CustomTokenize():

    pass