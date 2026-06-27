# -*- coding: utf-8 -*-
"""
Dropbox API 串接：抓取三檔商品圖到 assets/，供 build_dm.py 自動套入 DM。

需求：Dropbox access token（scope 至少 files.metadata.read + files.content.read；
若用共享連結另加 sharing.read）。token 由環境變數提供，不寫入檔案、不進 repo。

用法（擇一）：
  # A. 你的 Dropbox 內某資料夾路徑
  DROPBOX_TOKEN=sl.xxx python3 fetch_dropbox.py --path "/團購/8月商品圖"

  # B. 共享連結（資料夾或單檔皆可）
  DROPBOX_TOKEN=sl.xxx python3 fetch_dropbox.py --link "https://www.dropbox.com/scl/fo/xxxx?rlkey=yyyy"

抓下來後執行：python3 build_dm.py 即會把對應商品圖套進 4 張 DM。
檔名建議含關鍵字以利自動對應：wokyis / luna(或 mag/lycander) / sharge(或 disk/pro)。
"""

import argparse
import json
import os
import ssl
import sys
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")
CA = "/root/.ccr/ca-bundle.crt"
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif")

API = "https://api.dropboxapi.com/2"
CONTENT = "https://content.dropboxapi.com/2"


def _ctx():
    if os.path.exists(CA):
        return ssl.create_default_context(cafile=CA)
    return ssl.create_default_context()


def _opener():
    # urllib 會自動讀取環境變數 HTTPS_PROXY；明確指定 https handler 帶 CA context
    handlers = [urllib.request.HTTPSHandler(context=_ctx())]
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
    return urllib.request.build_opener(*handlers)


OPENER = _opener()


def token():
    t = os.environ.get("DROPBOX_TOKEN", "").strip()
    if not t:
        sys.exit("✗ 缺少環境變數 DROPBOX_TOKEN（請帶上 Dropbox access token）")
    return t


def rpc(endpoint, arg):
    """api.dropboxapi.com 的 JSON-RPC 呼叫，回傳 dict。"""
    req = urllib.request.Request(
        API + endpoint, data=json.dumps(arg).encode("utf-8"),
        headers={"Authorization": "Bearer " + token(),
                 "Content-Type": "application/json"})
    with OPENER.open(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def content_download(endpoint, arg):
    """content.dropboxapi.com 下載，回傳 bytes。"""
    req = urllib.request.Request(
        CONTENT + endpoint, data=b"",
        headers={"Authorization": "Bearer " + token(),
                 "Dropbox-API-Arg": json.dumps(arg)})
    with OPENER.open(req, timeout=120) as r:
        return r.read()


def is_img(name):
    return name.lower().endswith(IMG_EXT)


def save(name, data):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    with open(p, "wb") as f:
        f.write(data)
    print("  ✓ %s (%d KB)" % (name, len(data) // 1024))


def list_entries(path=None, link=None):
    arg = {"path": path or "", "recursive": False}
    if link:
        arg["path"] = ""
        arg["shared_link"] = {"url": link}
    out = rpc("/files/list_folder", arg)
    entries = list(out.get("entries", []))
    while out.get("has_more"):
        out = rpc("/files/list_folder/continue", {"cursor": out["cursor"]})
        entries += out.get("entries", [])
    return entries


def fetch_path(path):
    print("→ 列出資料夾：", path)
    n = 0
    for e in list_entries(path=path):
        if e.get(".tag") == "file" and is_img(e["name"]):
            data = content_download("/files/download", {"path": e["path_lower"]})
            save(e["name"], data); n += 1
    return n


def fetch_link(link):
    # 先試當資料夾列出；失敗則當單檔下載
    try:
        entries = list_entries(link=link)
        print("→ 共享資料夾，含 %d 個項目" % len(entries))
        n = 0
        for e in entries:
            if e.get(".tag") == "file" and is_img(e["name"]):
                data = content_download("/sharing/get_shared_link_file",
                                        {"url": link, "path": "/" + e["name"]})
                save(e["name"], data); n += 1
        return n
    except urllib.error.HTTPError as ex:
        print("（非資料夾連結，改當單檔下載）", ex.code)
        data = content_download("/sharing/get_shared_link_file", {"url": link})
        save("dropbox_image", data)  # 副檔名請自行補；建議用 --path 模式取得原檔名
        return 1


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--path", help="Dropbox 內資料夾路徑，如 /團購/8月商品圖")
    g.add_argument("--link", help="Dropbox 共享連結（資料夾或單檔）")
    a = ap.parse_args()
    try:
        n = fetch_path(a.path) if a.path else fetch_link(a.link)
    except urllib.error.HTTPError as ex:
        body = ex.read().decode("utf-8", "ignore")[:400]
        sys.exit("✗ Dropbox API 錯誤 %s：%s" % (ex.code, body))
    except urllib.error.URLError as ex:
        sys.exit("✗ 連線失敗（檢查 proxy / token）：%s" % ex)
    print("完成：抓取 %d 張圖到 assets/。接著執行 python3 build_dm.py 套圖。" % n)


if __name__ == "__main__":
    main()
