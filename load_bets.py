import requests
from lxml import html

def get_bets(stage):

    res = dict()
    r = requests.get('https://www.eurocups.ru/bets/stage/' + str(stage) + '/')
    tree = html.fromstring(r.text)
    bets_table = tree.xpath('//table[@id="bets_tournaments_table"]')[0]
    bets = bets_table.xpath('.//tr')

    for bet in bets:
        b = bet.xpath('.//td')
        if len(b)==3:
            res[b[0].text] = [b[2].text.strip()]
            br = b[2].xpath('.//br')
            for el in br:
                res[b[0].text].append(el.tail.strip())
    return res

    
    


