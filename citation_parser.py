from wsgiref import headers

from Author import Author
from Citations import Citations
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
        url="https://scholar.google.com.tr/"+"scholar?hl=tr&q="+self.get_author_name()+" "+self.get_author_surname()+"&btnG=&lr="
        r=requests.get(url)
        if r.status_code==200:
            print("Connection Successfully")
            soup=BeautifulSoup(r.content,'html.parser')
            soup.prettify()
        else:
            print("Connection was not Successfully")
            return

        return url
    def get_citation_page_html(self):
        url="https://scholar.google.com.tr/"+self.get_citation_page_href()
        print(url)
        r=requests.get(url)
        if r.status_code==200:
            print("Connection Succesfully")
            soup=BeautifulSoup(r.content,'html.parser')
            soup.prettify()

        else:
            print("Connection was not Successfully")
        return soup

    def get_citation_page_href(self):
        url=self.get_scholar_url()
        href_link=""
        r=requests.get(url)
        if r.status_code==200:
            soup=BeautifulSoup(r.content,"html.parser")
            soup.prettify()
            for link in soup.find_all('h4','gs_rt2'):
                for a in link.find_all('a'):
                   href_link=a.get('href')

        else:
            print("Connection was not Successfully")
            return
        return href_link

    def get_quotes(self):
        # her bir href için istek gönder çünkü her birinin soup html'si farklı
        # işimiz bittiğinde soup=none deriz. eğer soup none değilse , append listeye ----
        # sonra soupa tekrar html belgesi gelsin yine okunsun
        # okunduktan sonra her seferinde soup.find_all('div','gs_rs') aranacak ve get text denecek bunu nasıl yaparız çift for la birinci
        # for da listeden gelen her bir href için link okunur .
        # altında aranır ve atılır.
        get_href_list=self.get_quotes_href_link()
        print(get_href_list)
        get_quotes_list=[]
        for read_href in get_href_list:
            r=requests.get(read_href)
            if r.url is None:
                continue
            else:
                if r.status_code==200:
                    soup=BeautifulSoup(r.content,'html.parser')
                    for quotes in soup.find_all('div','gs_rs'):
                     get_quotes_list.append(quotes.string)

            get_quotes_list.append("\n ----------------------------------")

        for i in range(get_quotes_list.__len__()):
            print(get_quotes_list.__getitem__(i))
        return get_quotes_list


    def isUpgrade(self,control):
        control=False

        return control




    def get_parsed_bib_text_data_author(self):
        result=Scholar_Bib_Text.query(self.get_author_name()+" "+
                self.get_author_surname(),Scholar_Bib_Text.FORMAT_BIBTEX)
        print(result)
        return result

    def get_author_writings(self):
        #writers=20
        id_list=[]
        soup=self.get_citation_page_html()
        soup.prettify()
        for td in soup.find_all('td','gsc_a_t'):
            for a in td.find_all('a','gsc_a_at'):
                id_list.append(a.string)
                print(a.string)

        return id_list

    def get_author_writers(self):
        soup=self.get_citation_page_html()
        soup.prettify()
        counter=1
        writer_list=[]
        for div in soup.find_all('div','gs_gray'):
            if counter % 2 == 1:
                writer_list.append(div.string)

            counter+=1

        return writer_list

    def get_quotes_href_link(self):
        soup=self.get_citation_page_html()
        soup.prettify()
        quotes_href_list=[]
        for a in soup.find_all('a','gsc_a_ac'):
          quotes_href_list.append(a.get('href'))


        return quotes_href_list

citation=ParserScholar('Ecir Uğur','Küçüksille')
#citation.get_citation_page_html()
#citation.get_parsed_bib_text_data_author()
#citation.get_author_writings()
#citation.get_quotes_href_link()
citation.get_quotes()

