# TODO


### Interpret news
* Parse each news article and summarize into short text and save in catalyst with correct catalyst_type
* Parse

### Simplify template:
* Remove examples?
* Take 3-5 examples and iterate with chatgpt until good template
* Unit test with CosineSimilarity on generated response vs. manually OK response (also to quantify quality of response)

### different types of news fetching
* Use local LLM with simple web parser on generic site, e.g. finviz.com/msft  - https://github.com/ScrapeGraphAI/Scrapegraph-ai
    * with prompt 'Find shares outstanding, days to cover etc." instead of hardcoding divs/ids etc.
* duckduckgo: https://github.com/deedy5/duckduckgo_search
* Google/other search: only valid for a specific date, including day before (mostly)
* Benzinga
* Try Olostep (actual browser?)
* TheFly (upgrades/downgrades)
* stockhouse.com (all news etc  )
* polygon.io
* Alphavantage: fetch and save all news (for all stocks) as json, then parse separately to fetch actual news
* Verified good source for news/ERs: save all articles for ticker (maybe classify as news/ER before?)
    * Parse news before storing it?
    * Använd https://unstructured-io.github.io/unstructured/index.html för att parse ER documents t.ex.

### API (cloud or local) or use system directly with code and try different llm libs (must return structured json?)



