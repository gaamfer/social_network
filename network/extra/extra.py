def rip_tags(text):
    list =[]
    for word in text.split():
        if word.startswith('#'):
            list.append(word.removeprefix('#'))
    
    return list

def rip_pings(text):
    list = []
    for word in text.split():
        if word.startswith('@'):
            list.append(word.removeprefix('@'))
    
    return list