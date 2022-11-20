from bs4 import BeautifulSoup
import requests 
import pandas as pd


patnum=input("Enter the patent numbers").split()


def get_patent_data(patent):

    url = "https://patents.google.com/patent/" + str(patent)

    r = requests.get(url)
    data = r.content

    soup = BeautifulSoup(data, 'html.parser')


    title = soup.find('span', attrs={'itemprop':"title"})
    #print(title.text)
    prd= soup.find('time', attrs={'itemprop':"priorityDate"})
    #print(prd.text)
    flgdate= soup.find('time', attrs={'itemprop':"filingDate"})
    #print(flgdate.text)
    pubdate= soup.find('time', attrs={'itemprop':"publicationDate"})
    #print(pubdate.text)

    event = []
    events= soup.find_all('dd', attrs={'itemprop':"events"})
    for d in range(len(events)):
        event.append(events[d].get_text())
    legal_events = " ".join(event)
    #for i in range(len(events)):
    #    print(events[i].get_text())

    first_claim= soup.find('div', attrs={'id':"CLM-00001"})
    #print(first_claim.text)

    numclaims= soup.find_all('span', attrs={'itemprop':"count"})
    x = len(numclaims) - 1
    #print(numclaims[x].text)

    inventor =[]
    inv= soup.find_all('dd', attrs={'itemprop':"inventor"})
    #y = len(inv) - 1
    for c in range(len(inv)):
        inventor.append(inv[c].string.strip())
    inventors = " | ".join(inventor)
    #print(inv.text)

    assignee= soup.find('dd', attrs={'itemprop':"assigneeOriginal"})
    #print(assignee.text)

    current_assignee= soup.find('dd', attrs={'itemprop':"assigneeCurrent"})
    #print(current_assignee.text)

    data=[patent, title.string, inventors, assignee.text, current_assignee.text.strip(), prd.text, flgdate.text, pubdate.text, numclaims[x].text, first_claim.text.strip(), legal_events]
    return data


df=pd.DataFrame(index=['Patent Number', 'Title', 'Inventor', 'Assignee', 'Current Assignee', 'Priority Date', 'Application Date', 'Publication Date', 'Number of Claims', 'First CLaim', 'Legal Events'])


for a in range(len(patnum)):
    data=(get_patent_data(patnum[a]))
    df[a] = (data)

dft = df.transpose()

print(dft)

dft.to_csv('patent data.csv')