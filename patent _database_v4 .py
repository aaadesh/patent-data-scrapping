from bs4 import BeautifulSoup
import requests 
import pandas as pd


patnum=input("Enter the patent numbers").split()


def get_patent_data(patent):

    url = "https://patents.google.com/patent/" + str(patent) + "/en"

    r = requests.get(url)
    datas = r.content
    
    if r.status_code == 404:
        print("Patent not available on Google")
        data = [patent, "Patent not available on Google", "Patent not available on Google", "Patent not available on Google", "Patent not available on Google", "Not available on Google", "Patent not available on Google", "Not available on Google", "Patent not available on Google", "Patent not available on Google", "Patent not available on Google", "Patent not available on Google", "Patent not available on Google", "Patent not available on Google", "Patent not available on Google", "Patent not available on Google", "Patent not available on Google"]
        return data    

    soup = BeautifulSoup(datas, 'html.parser')

    tit = soup.find('span', attrs={'itemprop':"title"})
    if tit != None:
        title = tit.text.replace("\n", "")
    else:
        title = "N/A"
    #print(title.text)
    
    prdate= soup.find('time', attrs={'itemprop':"priorityDate"})
    if prdate != None:
        prd = prdate.text
    else:
        prd = "N/A"
    #print(prd.text)
    
    flgdate= soup.find('time', attrs={'itemprop':"filingDate"})
    if flgdate != None:
        flg = flgdate.text
    else:
        flg = "N/A"
    #print(flgdate.text)
    
    pubdate= soup.find('time', attrs={'itemprop':"publicationDate"})
    if pubdate != None:
        pub = pubdate.text
    else:
        pub = "N/A"
    #print(pubdate.text)

    event = []
    events= soup.find_all('dd', attrs={'itemprop':"events"})
    if len(events) != 0:
        for d in range(len(events)):
            event.append(events[d].get_text())
        legal_events = " ".join(event).replace('\n',' ').strip()
    else:
        legal_events = "N/A"
    #for i in range(len(events)):
    #    print(events[i].get_text())

    first_clm= soup.find('div', attrs={'id':"CLM-00001"})
    if first_clm != None:
        first_claim = first_clm.text.strip()
    else:
        first_claim = "N/A"
    #print(first_claim.text)

    numclaim= soup.find_all('span', attrs={'itemprop':"count"})
    x = len(numclaim) - 1
    if numclaim != None:
        numclaims = numclaim[x].text
    else:
        numclaims = "N/A"
    #print(numclaims[x].text)

    inventor =[]
    inv= soup.find_all('dd', attrs={'itemprop':"inventor"})
    if inv != None:
        #y = len(inv) - 1
        for c in range(len(inv)):
            inventor.append(inv[c].string.replace('\n', ' ').strip())
        inventors = " | ".join(inventor)
    else:
        inventors = "N/A"
    #print(inv.text)

    asg= soup.find('dd', attrs={'itemprop':"assigneeOriginal"})
    if asg != None:
        assignee = asg.text
    else:
        assignee = "N/A"
    #print(assignee.text)

    current_asg= soup.find('dd', attrs={'itemprop':"assigneeCurrent"})
    if current_asg != None:
        current_assignee = current_asg.text.strip()
    else:
        current_assignee = "N/A"
    #print(current_assignee.text)
    
    NPL = []
    NPLS = soup.find_all('tr', attrs={'itemprop':"detailedNonPatentLiterature"})
    
    if len(NPLS) != 0:
        for e in range(len(NPLS)):
            NPL.append(NPLS[e].text.replace('\n', ' ').strip())
            #print(NPL)
            #print(len(NPL))
        npl_cit = " | ". join(NPL)
        #print(npl_cit)
    else:
        npl_cit = "N/A"
    
    citation = []
    cit = soup.find_all('tr', attrs={'itemprop':"backwardReferencesOrig"} )
    if cit != None:
        for f in range(len(cit)):
            citation.append(cit[f].text.replace('\n', ' ').strip())
            #print(citation)
            #print(len(citation))
        citations = " | ".join(citation)
        #print(citations)
    else:
        citations = "N/A"
    
    
    fcitation = []
    fcit = soup.find_all('tr', attrs={'itemprop':"forwardReferencesOrig"} )
    if len(fcit) != 0:
        for f in range(len(fcit)):
            fcitation.append(fcit[f].text.replace('\n', ' ').strip())
            #print(fcitation)
            #print(len(fcitation))
        fcitations = " | ".join(fcitation)
        #print(fcitations)
    else:
        fcitations = "N/A"
    
    #for publicationNumber in fcitation:
    #    print(publicationNumber)

    data=[patent, title, inventors, assignee, current_assignee, prd, flg, pub, numclaims, first_claim, legal_events, len(NPL), npl_cit, len(citation), citations, len(fcitation), fcitations]
    return data


df=pd.DataFrame(index=['Patent Number', 'Title', 'Inventor', 'Assignee', 'Current Assignee', 'Priority Date', 'Application Date', 'Publication Date', 'Number of Claims', 'First CLaim', 'Legal Events', 'Number of NPL Citations', 'NPL Citations', 'Number of Backward Citations', 'Backward Citations', 'Number of Forward Citations', 'Forward Citations'])

for a in range(len(patnum)):
    data=(get_patent_data(patnum[a]))
    print("Fetching data for: ", a, patnum[a])
    df[a] = (data)

dft = df.transpose()

print(dft)

dft.to_csv('patent data.csv')