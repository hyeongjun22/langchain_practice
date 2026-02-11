import json
import uuid
import requests
import streamlit as st

st.set_page_config(page_title="LCEL RAG Chat", layout="centered")

api_base = st.sidebar.text_input("API Base URL", "http://backend:8080")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "collection_name" not in st.session_state:
    st.session_state.collection_name = st.session_state.session_id
if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.subheader("Session / Collection")
st.session_state.session_id = st.sidebar.text_input("session_id", st.session_state.session_id)
st.session_state.collection_name = st.sidebar.text_input(
    "collection_name (기본=session_id)",
    st.session_state.collection_name
)

mode = st.sidebar.radio("Mode", ["Non-Streaming", "Streaming(SSE)"])

st.title("📎 Upload → Index(Chroma) → RAG Chat")

# ---- 파일 업로드 영역 ----
uploaded = st.file_uploader("PDF/TXT/MD 업로드", type=["pdf", "txt", "md"])
if uploaded is not None:
    if st.button("업로드 & 인덱싱"):
        files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        data = {
            "session_id": st.session_state.session_id,
            "collection_name": st.session_state.collection_name,
        }
        r = requests.post(f"{api_base}/documents/upload", files=files, data=data, timeout=300)
        if r.ok:
            res = r.json()
            st.success(f"인덱싱 완료 ✅ collection={res['collection_name']}, chunks={res['chunks_indexed']}")
        else:
            st.error(f"업로드 실패: {r.status_code} / {r.text}")

st.divider()

# ---- 채팅 UI ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("질문을 입력하세요")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    payload = {
        "session_id": st.session_state.session_id,
        "collection_name": st.session_state.collection_name,
        "message": prompt,
    }

    if mode == "Non-Streaming":
        with st.chat_message("assistant"):
            r = requests.post(
                f"{api_base}/chat",
                params={"query": prompt},
                timeout=120,
            )
            if r.ok:
                answer = r.json()["answer"]
                st.markdown(answer)
            else:
                answer = f"❌ 오류: {r.status_code} / {r.text}"
                st.error(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    else:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full = ""
            try:
                with requests.post(
                    f"{api_base}/chat/stream",
                    params={"query": prompt},
                    stream=True,
                    timeout=120,
                ) as r:
                    r.raise_for_status()
                    for line in r.iter_lines(decode_unicode=True):
                        if not line:
                            continue
                        if line.startswith("data: "):
                            data = line[len("data: "):].strip()
                            if data == "[DONE]":
                                break
                            token = json.loads(data)["token"]
                            full += token
                            placeholder.markdown(full)
            except Exception as e:
                full = f"❌ 오류: {e}"
                st.error(full)

        st.session_state.messages.append({"role": "assistant", "content": full})
