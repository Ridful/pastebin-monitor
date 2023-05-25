
import requests
from urllib.parse import urlparse, urlunparse
import argparse
from lxml import html

active_url = urlparse("https://www.pastebin.com/")

parser = argparse.ArgumentParser(description='description of program here')
parser.add_argument('scan', help='Help message for the do argument')
parser.add_argument('-p', '--pasteid', help='specify the unique paste path id')
parser.add_argument('-e', '--extractinfo', action='store_true', help='try the connection')
args = parser.parse_args()

arg_value = args.scan
arg_pasteid = args.pasteid
arg_extractinfo = args.extractinfo
#get_raw_paste = args.getrawpaste

def getUrl(pasteUniquePathId):
    temp_url_tuple = active_url._replace(path=pasteUniquePathId)
    return urlunparse(temp_url_tuple)

def getPastePageBytes(full_url):
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
                
    #print('\t'.join(result_dict.values()))
    
    return result_dict

def main():
    
    if arg_value and arg_pasteid:

        paste_url = getUrl(arg_pasteid)
        
        if arg_extractinfo:
            res = getPastePageBytes(paste_url)
            
            print(f'my_input: {arg_pasteid}  |  paste_url: {paste_url}  |  page_status_code: {res.status_code}\n')

            if res.status_code == 200:
                result_dict = pageParser(res)
                for key,value in result_dict.items():
                    print(f'{key}: {value}')
        else:
            print(f'my_input: {arg_pasteid}  |  paste_url: {paste_url}  |  page_status_code: N/A')
            
if __name__ == "__main__":
    main()