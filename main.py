
import requests
from urllib.parse import urlparse, urlunparse
import argparse
from lxml import html

base_url = urlparse("https://www.pastebin.com/")

default_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Content-Type': 'text/html'
}

parser = argparse.ArgumentParser(description='description of program here')
parser.add_argument('paste', help='handle operations and options for chosen Paste')
parser.add_argument('-i', '--pasteid', help='Specify the unique Id associated with the Paste')
parser.add_argument('-m', '--metadata', action='store_true', help='Get the Information/Metadata available about the Paste')
parser.add_argument('-dR', '--downloadRaw', action='store_true', help='Option to download the Raw Paste ..')
args = parser.parse_args()

arg_value = args.paste
arg_pasteid = args.pasteid
arg_metadata = args.metadata
arg_downloadRaw = args.downloadRaw

def getUrl(pasteUniquePathId):
    temp_url_tuple = base_url._replace(path=pasteUniquePathId)
    return urlunparse(temp_url_tuple)

def getPasteReqResp(full_url):
    return requests.get(full_url)

def pageParser(pastePage):
    tree = html.fromstring(pastePage.content)
    
    xpath_dict = {
        'title_xpath': "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/h1/text()",
        'userUploader_xpath': "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[3]/div[2]/div[1]/a/text()",
        'uploadDate_xpath': "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[3]/div[2]/div[2]/span/text()",
        'visits_xpath': "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[3]/div[2]/div[3]/text()",
        'stars_xpath': "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[3]/div[2]/div[4]/text()",
        'expiry_xpath': "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[3]/div[2]/div[5]/text()",
        'syntax_xpath': "/html/body/div[1]/div[2]/div[1]/div[2]/div[4]/div[1]/div[1]/a[1]/text()",
        'filesize_xpath': "/html/body/div[1]/div[2]/div[1]/div[2]/div[4]/div[1]/div[1]/text()[1]/text()",
        'category_xpath': "/html/body/div[1]/div[2]/div[1]/div[2]/div[4]/div[1]/div[1]/span/text()",
        'thumbsup_xpath': "/html/body/div[1]/div[2]/div[1]/div[2]/div[4]/div[1]/div[1]/a[2]/text()",
        'thumbsdown_xpath': "/html/body/div[1]/div[2]/div[1]/div[2]/div[4]/div[1]/div[1]/a[3]/text()",
        'extra_xpath': "/html/body/script[4]/text()"
    }
    
    result_dict = {}
    for variable, xpath in xpath_dict.items():
        elements = tree.xpath(xpath)
        if elements:
            element = elements[0]
            print(f'Found: {element.strip()}')
            result_dict[variable] = str(element).strip()
            
    return result_dict

def getInfoAboutPaste(paste_url, action = "print"):
    
    res = getPasteReqResp(paste_url)
    
    if res.status_code == 200:
        result_dict = pageParser(res)
        for key,value in result_dict.items():
            if action == "print":
                print(f'{key}: {value}')
            else: pass #f'{key}: {value}'
    
    print(f'my_input: {arg_pasteid}  |  paste_url: {paste_url}  |  page_status_code: {res.status_code}\n')

def getRawPaste(raw_url, *headers):
    if not headers:
        headers = default_headers
    return requests.get(url=raw_url, headers=headers).text

def main():
    
    if not arg_value: return 0
    if not arg_pasteid: return 0
    
    paste_url = getUrl(arg_pasteid)
    raw_url = getUrl("/raw/" + arg_pasteid)
    
    if arg_metadata: getInfoAboutPaste(paste_url, "print")
    if arg_downloadRaw:
        raw_paste_text= getRawPaste(raw_url)
        print(raw_paste_text)
    
if __name__ == "__main__":
    main()