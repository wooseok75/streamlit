"""실습 3~4: 텍스트 답변 + 이미지 생성."""

import base64
import hashlib

import streamlit as st

from helpers import IMAGE_MODEL, TEXT_MODEL, require_client

st.title("Home | 텍스트 & 이미지 생성")
client = require_client()

# cache_data에 client 객체를 직접 해싱하면 오류가 날 수 있어 _client로 제외합니다.
# 대신 API Key의 해시값을 캐시 키의 일부로 사용합니다.
@st.cache_data(show_spinner=False)
def get_text_answer(prompt: str, key_fingerprint: str, _client):
    response = _client.responses.create(model=TEXT_MODEL, input=prompt)
    return response.output_text


st.subheader("실습 3. 질문에 대한 AI 답변")
question = st.text_area("질문을 입력하세요", placeholder="예: 강화학습이란 무엇인가요?", key="home_question")
if st.button("텍스트 생성", key="text_button"):
    if not question.strip():
        st.warning("질문을 입력하세요.")
    else:
        fingerprint = hashlib.sha256(st.session_state["active_api_key"].encode()).hexdigest()
        try:
            with st.spinner("답변을 생성하는 중입니다..."):
                answer = get_text_answer(question, fingerprint, client)
            st.markdown(answer)
        except Exception as exc:
            st.error(f"텍스트 생성 실패: {exc}")

st.divider()
st.subheader("실습 4. 이미지 생성")
image_prompt = st.text_area("이미지 프롬프트", placeholder="예: 비 오는 서울 거리를 그려줘", key="image_prompt")
if st.button("이미지 생성", key="image_button"):
    if not image_prompt.strip():
        st.warning("이미지 프롬프트를 입력하세요.")
    else:
        try:
            with st.spinner("이미지를 생성하는 중입니다..."):
                img = client.images.generate(model=IMAGE_MODEL, prompt=image_prompt)
                image_bytes = base64.b64decode(img.data[0].b64_json)
            st.image(image_bytes, caption="AI 생성 이미지", use_container_width=True)
        except Exception as exc:
            st.error(f"이미지 생성 실패: {exc}")
