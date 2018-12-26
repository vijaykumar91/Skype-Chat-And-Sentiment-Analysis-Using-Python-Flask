req = Request('https://www.google.co.in/search?q=' + searchData,
              headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')