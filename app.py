
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

from dotenv import load_dotenv

load_dotenv()

# Webアプリの概要・操作説明
st.title("LLM専門家相談アプリ")
st.write("""
このアプリは、LLM（大規模言語モデル）に様々な専門家として質問できるWebアプリです。

1. 下の入力フォームに相談内容や質問を入力してください。
2. 専門家の種類を選択してください。
3. 「送信」ボタンを押すと、選択した専門家になりきったLLMが回答します。
""")

# 専門家の種類とシステムメッセージ
EXPERTS = {
    "医師": "あなたは優秀な医師です。医学的な知識と患者への思いやりを持って、わかりやすく丁寧に回答してください。",
    "弁護士": "あなたは経験豊富な弁護士です。法律の専門知識を活かし、正確かつ誠実に回答してください。",
    "ITエンジニア": "あなたは熟練したITエンジニアです。技術的な観点から、論理的かつ簡潔に回答してください。"
}

# OpenAI APIキーの取得（環境変数から）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.warning("OpenAI APIキーが設定されていません。環境変数 'OPENAI_API_KEY' を設定してください。")

# LLM応答関数
def get_llm_response(user_input: str, expert: str) -> str:
    """
    入力テキストと専門家の種類を受け取り、LLMからの回答を返す
    """
    if not OPENAI_API_KEY:
        return "OpenAI APIキーが設定されていません。"
    messages = [
        SystemMessage(content=EXPERTS.get(expert, "あなたは親切な専門家です。")),
        HumanMessage(content=user_input)
    ]
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0.7)
    response = llm(messages)
    return response.content

# 入力フォームとラジオボタン
with st.form("llm_form"):
    user_input = st.text_area("相談内容・質問を入力してください：", height=100)
    expert = st.radio("専門家の種類を選択してください：", list(EXPERTS.keys()), horizontal=True)
    submitted = st.form_submit_button("送信")

if submitted and user_input.strip():
    with st.spinner("LLMが回答中..."):
        answer = get_llm_response(user_input, expert)
    st.markdown("### 回答")
    st.write(answer)