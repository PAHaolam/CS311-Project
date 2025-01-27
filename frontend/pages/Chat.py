import requests
import streamlit as st
import sidebar as sidebar

user_avatar = "images/user.png"
professor_avatar = "images/professor.png"

def main():
    sidebar.show_sidebar()
    st.header("💬 Book selling assistant")

    if (
        "user_prompts_history" not in st.session_state 
        and "chat_answers_history" not in st.session_state
    ):
        st.session_state["user_prompts_history"] = []
        st.session_state["chat_answers_history"] = []

    container = st.container()
    with container:
        # Display initial assistant message
        if not st.session_state["chat_answers_history"]:
            with st.chat_message(name="assistant", avatar=professor_avatar):
                initial_message = (
                    "Chào bạn mình là chatbot hỗ trợ tư vấn, bạn cần giúp gì?"
                )
                st.markdown(initial_message)
                st.session_state["chat_answers_history"].append(initial_message)

        # Replay chat history
        for user_message, assistant_message in zip(
            st.session_state["user_prompts_history"], st.session_state["chat_answers_history"][1:]
        ):
            with st.chat_message(name="user", avatar=user_avatar):
                st.markdown(user_message)
            with st.chat_message(name="assistant", avatar=professor_avatar):
                st.markdown(assistant_message)

    # Input prompt
    prompt = st.chat_input("Viết tin nhắn tại đây ạ...")
    if prompt:
        with container:
            # Display user's message
            with st.chat_message(name="user", avatar=user_avatar):
                st.markdown(prompt)

            # Save user message to history
            st.session_state["user_prompts_history"].append(prompt)

            # Generate assistant's response (placeholder for now)
            with st.spinner():
                try:
                    response = requests.post("http://127.0.0.1:8000/v1/complete", json={"message": prompt})
                    if response.status_code == 200:
                        assistant_response = response.json().get("response")
                    else:
                        assistant_response = "Đã xảy ra lỗi khi kết nối đến API."
                except requests.exceptions.RequestException as e:
                    assistant_response = f"Đã xảy ra lỗi: {e}"

            with st.chat_message(name="assistant", avatar=professor_avatar):
                st.markdown(assistant_response)

            # Save assistant's response to history
            st.session_state["chat_answers_history"].append(assistant_response)

if __name__ == "__main__":
    main()