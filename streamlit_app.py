"""실습 5: Streamlit 멀티페이지 앱의 진입점."""

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="생성 AI 응용 프로그래밍", page_icon="🤖", layout="wide")

with st.sidebar:
    st.title("AI 실습")
    api_key = st.text_input("OpenAI API Key", type="password", key="api_key")
    st.caption("키는 웹 페이지에서만 입력하고 GitHub 저장소에 올리지 마세요.")

# 다른 페이지에서 사용할 수 있도록 클라이언트를 Session State에 저장합니다.
if api_key:
    if api_key != st.session_state.get("active_api_key"):
        # 다른 API Key로 교체되면 이전 클라이언트의 PDF 리소스를 정리합니다.
        old_client = st.session_state.get("openai_client")
        if old_client is not None:
            try:
                if old_store := st.session_state.get("pdf_vector_store_id"):
                    old_client.vector_stores.delete(vector_store_id=old_store)
                if old_file := st.session_state.get("pdf_file_id"):
                    old_client.files.delete(old_file)
            except Exception as exc:
                st.warning(f"이전 계정의 PDF 리소스를 삭제하지 못했습니다: {exc}")
        for state_key in (
            "chat_messages", "library_messages", "pdf_messages",
            "pdf_vector_store_id", "pdf_file_id", "pdf_filename",
        ):
            st.session_state.pop(state_key, None)
        st.session_state["pdf_uploader_version"] = st.session_state.get("pdf_uploader_version", 0) + 1
        st.session_state["active_api_key"] = api_key
        st.session_state["openai_client"] = OpenAI(api_key=api_key)
else:
    st.session_state.pop("openai_client", None)
    st.session_state.pop("active_api_key", None)

pg = st.navigation(
    [
        st.Page("app_pages/Home.py", title="Home", icon=":material/home:"),
        st.Page("app_pages/Chat.py", title="Chat", icon=":material/chat:"),
        st.Page("app_pages/Chatbot.py", title="Chatbot", icon=":material/school:"),
        st.Page("app_pages/ChatPDF.py", title="ChatPDF", icon=":material/picture_as_pdf:"),
    ]
)
pg.run()
