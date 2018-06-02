import urllib.request
from bs4 import BeautifulSoup
from retry import retry


class TracHTMLParser():
    def parse_page(self, url):
        page_str = self._read_html_page(url)
        return BeautifulSoup(page_str, "html.parser")

    @retry(exceptions=(ConnectionError, TimeoutError), delay=1, tries=6, backoff=2)
    def _read_html_page(self, url, codec="utf-8"):
        url_response = urllib.request.urlopen(url)
        return url_response.read().decode(codec)


# This is for test purpose
ticket_url = "https://devel.rtems.org/ticket/2988"
thp = TracHTMLParser()
bs = thp.parse_page(url=ticket_url)

milestone_url = "https://devel.rtems.org/milestone/4.11.3"
temp = TracHTMLParser()
newtemp = temp.parse_page(url=milestone_url)
xianggege = newtemp.find(name="div", attrs={"id": "content", "class": "milestone"}).find(name="h1")
#print(xianggege.string)

summary = bs.find(name="span", attrs={"class": "summary"})
#print(summary.string)
