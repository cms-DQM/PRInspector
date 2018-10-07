import urllib.request
import json

def paginate(url, items_count=0, page_param="?page="):
    response = []
    page = 1

    while True:
        part = urllib.request.urlopen(f"{url}{page_param}{page}").read()
        content = json.loads(part)

        if len(content) == 0:
            break

        page += 1
        response += content
    
    if items_count > 0:
        return response[:-items_count]
    
    return response
