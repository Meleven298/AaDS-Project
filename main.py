from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from nbconvert import HTMLExporter

NOTEBOOKS_DIR = Path("notebooks")
OUTPUT_DIR = Path("static/notebooks")

def convert_notebooks():
    """Превращает каждый .ipynb из notebooks/ в .html (вызывается при запуске)."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    exporter = HTMLExporter()
    
    for nb in NOTEBOOKS_DIR.glob("*.ipynb"):
        body, _ = exporter.from_filename(str(nb))
        (OUTPUT_DIR / f"{nb.stem}.html").write_text(body, encoding="utf-8")

        print("сконвертирован:", nb.name)

convert_notebooks()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def format_title(stem: str) -> str:
    """
    Превращает имя файла 'segment_tree' в красивый заголовок 'Segment Tree'.
    Если у вас файлы уже на русском (например, 'hashmap.ipynb'), функция вернет 'Hashmap'.
    """

    return stem.replace("_", " ").replace("-", " ").capitalize()

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    notebooks = []
    for nb in NOTEBOOKS_DIR.glob("*.ipynb"):
        notebooks.append({
            "title": format_title(nb.stem[:-4]),
            "file": nb.stem
        })
    
    notebooks.sort(key=lambda x: x["title"])

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"notebooks": notebooks},
    )