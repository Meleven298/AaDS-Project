from time import perf_counter

import pandas as pd
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from structures.hashmap import build_hash_index, linear_search
from structures.segment_tree import SegmentTree

app = FastAPI()
templates = Jinja2Templates(directory="templates")


df = pd.read_csv("data/data.csv", parse_dates=["created_at"])

# хеш-таблица: rating_id -> номер строки
keys = df["rating_id"].tolist()
hash_index = build_hash_index(keys)

# дерево отрезков по оценкам, отсортированным по времени
df_by_time = df.sort_values("created_at").reset_index(drop=True)
tree = SegmentTree(df_by_time["rating"].tolist())



@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"n": len(df)}
    )


@app.get("/search", response_class=HTMLResponse)
def search(request: Request, rating_id: int | None = None):
    row = None
    hash_ms = linear_ms = 0

    if rating_id is not None:
        start = perf_counter()
        row_id = hash_index.get(rating_id)           # быстрый поиск
        hash_ms = (perf_counter() - start) * 1000

        start = perf_counter()
        linear_search(keys, rating_id)               # медленный поиск, для сравнения
        linear_ms = (perf_counter() - start) * 1000

        if row_id is not None:
            row = df.iloc[row_id].to_dict()

    return templates.TemplateResponse(
        request=request,
        name="search.html",
        context={"rating_id": rating_id, "row": row,
                 "hash_ms": hash_ms, "linear_ms": linear_ms},
    )


@app.get("/segment", response_class=HTMLResponse)
def segment(request: Request, l: int | None = None, r: int | None = None):
    result = error = None

    if l is not None and r is not None:
        try:
            result = tree.query(l, r)
        except IndexError as e:
            error = str(e)

    return templates.TemplateResponse(
        request=request,
        name="segment.html",
        context={"n": tree.n, "l": l, "r": r, "result": result,
                 "error": error, "message": None},
    )


@app.post("/segment/update", response_class=HTMLResponse)
def segment_update(request: Request, i: int = Form(), x: float = Form()):
    error = message = None

    if not 0.5 <= x <= 5:
        error = "Оценка должна быть от 0.5 до 5"
    else:
        try:
            old = tree.a[i] if 0 <= i < tree.n else None
            tree.update(i, x)
            message = f"Оценка №{i}: {old} → {x}"
        except IndexError as e:
            error = str(e)

    return templates.TemplateResponse(
        request=request,
        name="segment.html",
        context={"n": tree.n, "l": None, "r": None, "result": None,
                 "error": error, "message": message},
    )
