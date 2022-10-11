from xml.etree.ElementTree import parse

def makeCodeInfo():
    ret = dict()
    tree = parse('corpCode/CORPCODE.xml')
    root = tree.getroot()
    lists = root.findall('list')
    corp_codes = [x.findtext("corp_code") for x in lists]
    corp_names = [x.findtext("corp_name") for x in lists]
    size = len(corp_codes)
    for i in range(size):
       ret[corp_names[i]] = corp_codes[i]
    return ret