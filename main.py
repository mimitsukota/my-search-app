import tkinter as tk
from tkinter import messagebox
import os
import sys

# --- 1. 辞書を読み込む ---
def load_dictionary():
    base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file_path = os.path.join(base_path, "words.txt")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return []
    return []

# --- 2. 検索の仕組み ---
def kousa_search(query, dictionary):
    results = []
    symbols = ["○", "□", "△"]
    for word in dictionary:
        if len(word) != len(query): continue
        symbol_to_kanji, used_kanji, is_match = {}, set(), True
        for q, w in zip(query, word):
            if q in symbols:
                if q in symbol_to_kanji:
                    if symbol_to_kanji[q] != w: is_match = False; break
                else:
                    if w in used_kanji: is_match = False; break
                    symbol_to_kanji[q] = w
                    used_kanji.add(w)
            elif q != w: is_match = False; break
        if is_match: results.append(word)
    return results

# --- 3. 検索ボタンを押した時の動き ---
def on_search():
    current_dict = load_dictionary()
    query = entry.get()
    if not query: return
    
    found = kousa_search(query, current_dict)
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    if found:
        result_text.insert(tk.END, "\n".join(found))
    else:
        result_text.insert(tk.END, "見つかりませんでした\n")
        if not current_dict:
            result_text.insert(tk.END, "(words.txtが隣にないようです)")

# --- 4. 画面を作る ---
root = tk.Tk()
root.title("mimitsuko専用 漢字パズル検索くん")
root.geometry("400x450")

tk.Label(root, text="\n○□△と漢字を入力してください", font=("Yu Gothic", 12)).pack()

# imemode="active" はWindows環境によってエラーになることがあるので、
# 一旦外して、より安定した形にしました
entry = tk.Entry(root, font=("Yu Gothic", 18), justify="center")
entry.pack(pady=10)

tk.Button(root, text=" 検索する ", font=("Yu Gothic", 14), command=on_search).pack(pady=10)
result_text = tk.Text(root, font=("Yu Gothic", 14), height=10, width=30)
result_text.pack(pady=10)

# 起動した瞬間にカーソルを合わせる
entry.focus_set()

root.mainloop()
