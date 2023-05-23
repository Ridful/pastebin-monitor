import requests
from lxml import html

url = 'https://pastebin.com/archive'

#res = requests.get('https://google.com')

res = requests.get(url=url)
print(res)

print("Moving on to the if statement")

# Check if the request was successful
if res.status_code == 200:
    # Parse the HTML content
    tree = html.fromstring(res.content)

    # Iterate over the range of XPath elements you provided
    for i in range(2, 52):
        
        xpath = f'/html/body/div[1]/div[2]/div[1]/div[1]/div[3]/table/tbody/tr[{i}]'
        
        element = tree.xpath(xpath)
        
        if element:
            # Extract the text of the element
            text = element[0].text
            
            # Print the extracted text
            print(text)
            
print("Done.")