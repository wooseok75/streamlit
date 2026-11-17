"""챗봇 페이지에서 공통으로 사용하는 유틸리티."""

import streamlit as st

TEXT_MODEL = "gpt-6-luna"
IMAGE_MODEL = "gpt-image-2.6-flare"


def require_client():
    """API Key가 입력되지 않았으면 페이지에 안내합니다."""
    client = st.session_state.get("openai_client")
    if client is None:
        st.info("왼쪽 사이드바에서 OpenAI API Key를 입력하세요.")
        st.stop()
    return client


def response_text_chunks(stream):
    """Responses API 스트리밍 이벤트에서 텍스트 부분만 추출합니다."""
    for event in stream:
        if event.type == "response.output_text.delta":
            yield event.delta
        elif event.type == "error":
            raise RuntimeError(getattr(event, "message", "스트리밍 도중 오류 발생"))


def display_previous_messages(messages):
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
