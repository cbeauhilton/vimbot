import math
from functools import lru_cache
from pprint import pprint

from colbert import Searcher  # type: ignore[unknown]
from fastapi import APIRouter, Response

from vimbot.config import settings

router = APIRouter()

searcher = Searcher(index=settings.INDEX_FULL_NAME, index_root=settings.INDEX_ROOT)

print(settings.INDEX_FULL_NAME, settings.INDEX_ROOT)


@lru_cache(maxsize=1000000)
def api_search_query(query: str, k: int | None) -> dict[str, object]:
    print(f"Query={query}")
    if k is None:
        k = 10
    k = min(int(k), 100)
    pprint(searcher.search(query, k=k))
    pids, ranks, scores = searcher.search(query, k=100)
    print("*" * 100)
    print("K:", k)
    print("PIDs:", pids)
    print("")
    print("Ranks:", ranks)
    print("")
    print("Scores:", scores)
    print("")
    print("*" * 100)
    pids, ranks, scores = pids[:k], ranks[:k], scores[:k]
    probs = [math.exp(score) for score in scores]
    probs = [prob / sum(probs) for prob in probs]
    topk: list[dict[str, object]] = []
    ids = list(range(len(pids)))
    print(len(ids))
    for i, pid, rank, score, prob in zip(ids, pids, ranks, scores, probs):
        # print(f"PID: {pid}")
        # print(f"rank: {rank}")
        # print(f"score: {score}")
        # print(f"prob: {prob}")
        # for t in searcher.collection:
        #     pprint(t)
        text = searcher.collection[i]
        d = {"text": text, "pid": pid, "rank": rank, "score": score, "prob": prob}
        pprint(d)
        topk.append(d)
    topk = list(sorted(topk, key=lambda p: (-1 * p["score"], p["pid"])))
    data = {"query": query, "topk": topk}
    print(data)
    return Response(content=data)


@router.get("/api/search")
async def api_search(
    query: str | None = None,
    k: int | None = None,
) -> dict[str, object] | tuple[str, int]:
    if query:
        result = api_search_query(query, k)
        return result
    else:
        return ("", 405)
