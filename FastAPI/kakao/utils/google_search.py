# 출처 : https://www.delftstack.com/ko/howto/python/python-google-search-api/
import requests

class GoogleSearchAPI:
    
    def __init__(self, api_key:str, search_engine_id:str):
        assert api_key, f'api_key is empty'
        assert search_engine_id, f'search_engine_id is empty'
        
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        return
    
    def __del__(self):
        return
    
    # page=2면 20개 뽑아옴
    def search_google(self, query:str, page:int=1):
        assert query, f'query is empty'
        contexts:list = []
        best_contexts:list = []
        
        for idx in range(page):
            start = idx * 10 + 1
            try:
                url = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.search_engine_id}&q={query}&start={start}"
                # make the API request
                data = requests.get(url).json()

                # get the result
                search_items = data.get("items")

                # iterate over 10 results
                for i, search_item in enumerate(search_items, start=1):
                    try:
                        long_description = search_item["pagemap"]["metatags"][0]["og:description"]
                    except KeyError:
                        long_description = "N/A"

                    # get the title of the page
                    title = search_item.get("title")

                    # get the page snippet
                    descript = search_item.get("snippet")

                    # alternatively, you also can get the HTML snippet (bolded keywords)
                    html_snippet = search_item.get("htmlSnippet")

                    # extract page url
                    link = search_item.get("link")

                    # print results
                    context:dict = {}
                    context['link'] = link
                    context['title'] = title
                    context['descript'] = descript
                    context['score'] = "0"  
                    context['longdescript'] = long_description
                    contexts.append(context)
                    
                    # 첫번째page(idx==1) 이고 첫번째 page에서 3개 까지가 best 검색된 결과임.
                    if idx == 1 and i< 4:
                        best_contexts.append(context)

            except Exception as e:
                print(f'[search_google] error={e}')
                return contexts, best_contexts, 1001
            
        return contexts, best_contexts, 0