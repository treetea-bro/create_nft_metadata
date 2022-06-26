from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
import os
import shutil
import json
from collections import OrderedDict
from tkinter import filedialog

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/download")
def exec(nft_num: int, name: str, symbol: str, description: str, trait_type: str, value: str):
    FOLDER_DIR = "images/"
    START_IDX = 0

    root_path = os.path.abspath(os.curdir)

    img_file_path = filedialog.askopenfilename(initialdir=root_path, title="이미지를 선택 해주세요.")
                                    
    img_ext_li = [".png", ".jpg", ".jpeg"]                                        
    _, ext = os.path.splitext(img_file_path)
    if ext not in img_ext_li or img_file_path == "":
        return "이미지 파일을 선택하여 주세요."

    if os.path.exists("./images.zip") : os.remove("./images.zip")
    if os.path.exists(FOLDER_DIR) : shutil.rmtree(FOLDER_DIR)
    os.mkdir(FOLDER_DIR)

    file_data = OrderedDict()
    for i in range(START_IDX, nft_num + START_IDX) :
        file_data["name"] = f"{name} #{i + 1}"
        file_data["symbol"] = symbol
        file_data["description"] = description
        file_data["image"] = f"{i}.jpg"
        file_data["attributes"] = [{"trait_type": trait_type, "value": value}]
        shutil.copyfile(img_file_path, os.path.join(root_path, FOLDER_DIR) + str(i) + ".jpg")
        
        with open(f"{FOLDER_DIR}{i}.json", "w", encoding="utf-8") as f:
            json.dump(file_data, f, ensure_ascii=False, indent="\t")

    shutil.make_archive("images", "zip", FOLDER_DIR)

    return FileResponse("images.zip", media_type='application/octet-stream',filename="images.zip")
