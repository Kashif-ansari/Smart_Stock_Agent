from datetime import datetime, timezone
def search_public(query,max_results=5):
    from ddgs import DDGS
    results=[]
    with DDGS() as ddgs:
        for r in ddgs.text(query,max_results=max_results):
            results.append({"title":r.get("title"),"url":r.get("href"),"snippet":r.get("body"),
                            "retrieved_at":datetime.now(timezone.utc).isoformat()})
    return results
