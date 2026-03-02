from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import re

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def analyze_es(text):
    result = []

    # 結論チェック
    if not text.strip().startswith(("私", "私は")):
        result.append("⚠ 結論から始まっていない可能性があります。")

    # 数字チェック
    if not re.search(r"\d", text):
        result.append("⚠ 数字が含まれていません。具体性を上げましょう。")

    # 抽象ワードチェック
    abstract_words = ["頑張", "努力", "成長", "学び"]
    for word in abstract_words:
        if word in text:
            result.append(f"⚠ 『{word}』は抽象的です。具体例を追加しましょう。")

    if not result:
        result.append("✅ 大きな問題は見つかりませんでした。")

    return result

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
def analyze(request: Request, es_text: str = Form(...)):
    results = analyze_es(es_text)
    return templates.TemplateResponse("index.html", {"request": request, "results": results, "original": es_text})