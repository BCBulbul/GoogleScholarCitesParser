#!/usr/bin/env python3

from Author import Author
from bs4 import BeautifulSoup
import requests
import re
import Scholar_Bib_Text
class ParserScholar(Author):
    _HEADERS = {
    'accept-language': 'en-US,en',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml'
    }


    def get_scholar_url(self):

        """ Getting  The Google Scholar url """


        url="https://scholar.google.com.tr/"+"scholar?hl=tr&q="+self.get_author_name()+" "+self.get_author_surname()+"&btnG=&lr="
        r=requests.get(url)
        if r.status_code==200:
            print("Connection Successfully")
            soup=BeautifulSoup(r.content,'html.parser')
            soup.prettify()
        else:
            print("Connection was not Successfully")
            return
        print(r.url)
        return r.url
    def get_citation_page_html(self):
        """
           This method is using The Citation Page href and getting The Citation Page Html
        """

        url="https://scholar.google.com.tr/"+self.get_citation_page_href()
        r=requests.get(url)
        if r.status_code==200:
            print("Connection Succesfully")
            soup=BeautifulSoup(r.content,'html.parser')
            soup.prettify()

        else:
            print("Connection was not Successfully")
        return soup

    def get_citation_page_href(self):
        """
        Getting href link from Google Scholar Search Page
        """
        url=self.get_scholar_url()
        href_link=""
        r=requests.get(url)
        print(r.url)
        if r.status_code==200:
            soup=BeautifulSoup(r.content,"html.parser")
            soup.prettify()
            for link in soup.find_all('h4','gs_rt2'):
                for a in link.find_all('a'):
                   href_link=a.get('href')
                   print(href_link)


        else:
            print("Connection was not Successfully")
            return

        return href_link

    def get_quotes(self):
        """
        Getting The Quotes from Google Scholar Author Page
        """

        get_href_list=self.get_quotes_href_link()
        print(get_href_list)
        get_quotes_list=[]
        counter=0
        for read_href in get_href_list:
         r=requests.get(read_href)
         print(r.url)
         if r.status_code==200:
            soup=BeautifulSoup(r.content,'html.parser')
            for quotes in soup.find_all('div','gs_ri'):
                get_quotes_list.append(quotes.get_text())
                print(quotes.get_text())
                counter+=1

         get_quotes_list.append("\n ----------------------------------")

        for i in range(get_quotes_list.__len__()):
            print(get_quotes_list.__getitem__(i))
        self.get_quotes_length(counter)
        return get_quotes_list
    def get_author_writings(self):
        """
        Getting Author's Writings
        """
        #writings=top 20
        id_list=[]
        soup=self.get_citation_page_html()
        soup.prettify()
        for td in soup.find_all('td','gsc_a_t'):
            for a in td.find_all('a','gsc_a_at'):
                id_list.append(a.string)
                print(a.string)

        return id_list

    def get_author_writers(self):
        """
        Getting The Author's Writers
        """
        soup=self.get_citation_page_html()
        soup.prettify()
        counter=1
        writer_list=[]
        for div in soup.find_all('div','gs_gray'):
            if counter % 2 == 1:
                writer_list.append(div.string)

            counter+=1

        return writer_list


    def get_quotes_length(self,length):
        self.is_upgrade(length)
        return length;

    def is_upgrade(self,old_length):
        """
        This method controls all quotes and can do upgrade or not upgrade
        """
        is_equal=False
        get_href_list=self.get_quotes_href_link()
        is_upgrade_list=[]
        for read_href in get_href_list:
            r=requests.get(read_href)
            if r.status_code==200:
                soup=BeautifulSoup(r.content,'html.parser')
                for quotes in soup.find_all('div','gs_ri'):
                    is_upgrade_list.append(quotes.get_text)
                    if len(is_upgrade_list) is not old_length:
                        is_equal=False
                    elif len(is_upgrade_list)>old_length:
                        is_equal=True
                        if is_equal is True:
                            print("Updating...")
                            return is_upgrade_list
                        else:
                            is_equal=False
                            if is_equal is False:
                             print("The Quotations are already up to date")
                             return self.get_quotes()






    def get_parsed_bib_text_data_author(self):
        """
        Getting The Author's Bibliography
        """
        result=Scholar_Bib_Text.query(self.get_author_name()+" "+self.get_author_surname(),Scholar_Bib_Text.FORMAT_BIBTEX)
        print(result)
        return result



    def get_quotes_href_link(self):
        """
        Getting The Quotes Href Link for Retrieve Data from Quotes Html Page
        """
        soup=self.get_citation_page_html()
        #print(soup)
        quotes_href_list=[]
        for a in soup.find_all('a','gsc_a_ac'):
            if a.get('href') is '':
                continue
            else:
              quotes_href_list.append(a.get('href'))

        print(quotes_href_list)
        return quotes_href_list



citation=ParserScholar('Ecir Uğur','Küçüksille')
citation.get_citation_page_html()
#citation.get_parsed_bib_text_data_author()
#citation.get_author_writings()
#citation.get_quotes_href_link()
#citation.get_quotes()
# citation.get_quotes_href_link()
#citation.get_citation_page_href()
## citation.get_scholar_url()

