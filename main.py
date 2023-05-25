
import requests
from urllib.parse import urlparse, urlunparse
import argparse
from lxml import html

active_url = urlparse("https://www.pastebin.com/")

parser = argparse.ArgumentParser(description='description of program here')
parser.add_argument('arg_name', help='Help message for the do argument')
parser.add_argument('-p', '--pasteid', help='specify the unique paste path id')
parser.add_argument('-t', '--tryconnect', action='store_true', help='try the connection')
args = parser.parse_args()

arg_value = args.arg_name
arg_pasteid = args.pasteid
arg_tryconnect = args.tryconnect

def getUrl(pasteUniquePathId):
    temp_url_tuple = active_url._replace(path=pasteUniquePathId)
    return urlunparse(temp_url_tuple)

def getPastePageBytes(full_url):
    return requests.get(full_url)

def pageParser(pastePage):
    tree = html.fromstring(pastePage.content)
    xpath = "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/h1/text()"
    element = tree.xpath(xpath)
    if element:
        text = element[0].text
        print(f'title of paste: {text}')
    
def main():
    
    if arg_value and arg_pasteid:
        print(arg_pasteid)
        
        my_url = getUrl(arg_pasteid)
        
        if arg_tryconnect:
            res = getPastePageBytes(my_url)
            
            print(f'my_input: {arg_pasteid}  |  my_url: {my_url}  |  page_status_code: {res.status_code}\n')

            if res.status_code == 200:
                pageParser(res)
            #print(res.text)
        else:
            print(f'my_input: {arg_pasteid}  |  my_url: {my_url}  |  page_status_code: N/A')
            
if __name__ == "__main__":
    main()