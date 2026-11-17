"""실습 5: 대화 내용을 저장하고 응답을 스트리밍하는 챗봇."""

import streamlit as st

from helpers import TEXT_MODEL, display_previous_messages, require_client, response_text_chunks

st.title("Chat | 대화형 챗봇")
client = require_client()

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []


def clear_chat():
    st.session_state["chat_messages"] = []


st.button("Clear", on_click=clear_chat)
display_previous_messages(st.session_state["chat_messages"])

if prompt := st.chat_input("메시지를 입력하세요", key="general_chat_input"):
    st.session_state["chat_messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            stream = client.responses.create(
                model=TEXT_MODEL,
                input=st.session_state["chat_messages"],
                stream=True,
            )
            answer = st.write_stream(response_text_chunks(stream))
        except Exception as exc:
            st.error(f"답변 생성 실패: {exc}")
        else:
            st.session_state["chat_messages"].append({"role": "assistant", "content": answer})
