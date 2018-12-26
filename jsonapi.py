import Algorithmia
client = Algorithmia.client("sim5bi+k7qsHJBcNbtxku4CGLb71")


def get_links(url2):
    """Gets links from URL"""
    input = url2
    if input.startswith("http") or input.startswith("https"):
        algo = client.algo('web/GetLinks/0.1.5')
        links = algo.pipe(input).result
        return links
    else:
        print("Please enter a properly formed URL")


def get_content(url1):
    """Get text content from URL."""
    data = get_links(url1)
    algo = client.algo("util/Url2Text/0.1.4")
    # Limit content extracted to only blog articles
    content = [{"url": link, "content": algo.pipe(
        link).result} for link in data if link.startswith(url1)]
    return content


def find_sentiment(url):
    """Get sentiment from web content."""
    data = get_content(url)
    algo = client.algo("nlp/SentimentAnalysis/1.0.2")
    try:
        # Find the sentiment score for each article
        algo_input = [{"document": item["content"]} for item in data]
        algo_response = algo.pipe(algo_input).result

        algo_final = [{"url": doc["url"], "sent": sent["sentiment"], "content": sent[
            "document"]} for sent in algo_response for doc in data]
        #print(algo_final)
        return algo_final

    except Exception as e:
        print(e)

data=find_sentiment("https://www.loginworks.com/")
print(data)