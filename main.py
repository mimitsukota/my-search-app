
import streamlit as st

# タイトル
st.title("mimitsuko専用 パズル検索くん")

# 辞書の読み込み
def load_words():
    try:
        with open('words.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        st.error("辞書ファイル(words.txt)が見つかりません。")
        return []

words = load_words()

# 入力欄
pattern = st.text_input("検索するパターンを入力してください（例：あい??）")

if st.button("検索実行"):
    if not pattern:
        st.warning("パターンを入力してください。")
    else:
        results = []
        for word in words:
            if len(word) == len(pattern):
                match = True
                for w, p in zip(word, pattern):
                    if p != '?' and w != p:
                        match = False
                        break
                if match:
                    results.append(word)
        
        # 結果表示
        if results:
            st.success(f"{len(results)}件見つかりました：")
            st.write(", ".join(results))
        else:
            st.info("見つかりませんでした。")
