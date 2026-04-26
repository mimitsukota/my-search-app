import streamlit as st

st.set_page_config(page_title="mimitsukoパズル検索", page_icon="🧩")
st.title("🧩 数字で指定！パズル検索くん")

@st.cache_data
def load_words():
    try:
        with open('words.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

words = load_words()

st.info("【使い方】\n同じ漢字が入る場所に同じ数字を入れてください。\n例：「1期1会」や「1231」など")

pattern_raw = st.text_input("検索パターンを入力（数字と漢字を混ぜてOK）", placeholder="例：1231")

if st.button("検索実行"):
    if not pattern_raw:
        st.warning("パターンを入力してください。")
    else:
        results = []
        for word in words:
            if len(word) == len(pattern_raw):
                match = True
                mapping = {} # 数字と漢字の対応を記録するメモ
                
                for char_p, char_w in zip(pattern_raw, word):
                    if char_p.isdigit(): # もし入力が数字だったら
                        if char_p in mapping:
                            # すでに同じ数字が出てきていたら、その時の漢字と同じかチェック
                            if mapping[char_p] != char_w:
                                match = False
                                break
                        else:
                            # 初めて出る数字なら、漢字をメモする
                            mapping[char_p] = char_w
                    else:
                        # 数字じゃない（漢字が指定されている）場合、一致するかチェック
                        if char_p != char_w:
                            match = False
                            break
                
                if match:
                    results.append(word)
        
        if results:
            st.success(f"{len(results)}件見つかりました")
            for res in results:
                st.write(f"・ **{res}**")
        else:
            st.info("見つかりませんでした。")
