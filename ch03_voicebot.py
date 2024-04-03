##### 기본 정보 입력 #####
import streamlit as st
# audiorecorder 패키지 추가
from audiorecorder import audiorecorder
# OpenAI 패키지 추가
import openai
# 파일 삭제를 위한 패키지 추가
import os
# 시간 정보를 위한 패키지 추가
from datetime import datetime
# TTS 패키기 추가
from gtts import gTTS
# 음원 파일 재생을 위한 패키지 추가
import base64

#os.environ["IMAGEIO_FFMPEG_EXE"] = "/path/to/ffmpeg"

##### 기능 구현 함수 #####
def STT(audio):
    # 파일 저장
    filename='input.mp3'
    audio.export(filename, format="mp3")
    # 음원 파일 열기
    audio_file = open(filename, "rb")
    # Whisper 모델을 활용해 텍스트 얻기
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    audio_file.close()
    # 파일 삭제
    os.remove(filename)
    return transcript["text"]

def ask_gpt(prompt, model):
    response = openai.ChatCompletion.create(model=model, messages=prompt)
    system_message = response["choices"][0]["message"]
    return system_message["content"]

def TTS(response):
    # gTTS 를 활용하여 음성 파일 생성
    filename = "output.mp3"
    tts = gTTS(text=response,lang="ko")
    tts.save(filename)

    # 음원 파일 자동 재생생
    with open(filename, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="True">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md,unsafe_allow_html=True,)
    # 파일 삭제
    os.remove(filename)


    #response = model(question)
    #return response

#def asking_gpt(question, model):
    #response = openai.Completion.create(
        #engine="davinci", 
        #prompt=question, 
        #max_tokens=50
    #)
    #return response.choices[0].text.strip()

##### 메인 함수 #####
def main():
    # 기본 설정
    st.set_page_config(
        page_title="채팅 비서 프로그램",
        page_icon="https://i.namu.wiki/i/MBfFDDfDxNGrWTgNv0t9f9439rY_4NCt5isV0_l6qZzMhR5D8Vg9ZVFVlEVaQ7H885Ge2kqzVpgg_5qnMLPEpMcQ-vutX52lwSiGtWRv9A4xIp-bM-DjtXOD8xHodSBCz7anuihzw9-GxT2GhzmbwQ.webp",
        layout="wide")

    flag_start = False

    # session state 초기화
    if "chat" not in st.session_state:
        st.session_state["chat"] = []

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": "You are the teacher of the Jangmi class at Kindergarten.You add a spirited 'Yeehaw!' at the end of each sentence, infusing their speech with a touch of cowboy flair and boundless energy, and you must speak in Korean."}]

    if "check_audio" not in st.session_state:
        st.session_state["check_audio"] = []

    if "check_reset" not in st.session_state:
        st.session_state["check_reset"] = False


    # 제목과 이미지를 포함한 컨테이너
    st.write("""
    <div style="display: flex; align-items: center;">
        <img src="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzAyMjNfMjYx%2FMDAxNjc3MTUyMjEyNDE1.k_YmMz1T5FoBs90klzioTbj1-GD7dV0MF3jZdJnc9o4g.YLboYUghaOjs7aJJJJbsmSn2sKIxZ433rLQ64Z9__A4g.JPEG.kis2092%2FIMG_8575.JPG&type=a340" width="50" style="border-radius: 50%; margin-right: 10px;">
        <h1>짱구와 나미리</h1>
    </div>
    """, unsafe_allow_html=True)
    # 구분선
    st.markdown("---")

    # 기본 설명
    with st.expander("✨ChatGPT 채팅 비서 팀 프로젝트✨", expanded=True):
        st.write(
        """     
        - 202284046 김나연, 202284050 박소윤, 202284054 박채현이 힘을 합쳐 만든 웹앱입니다.
        - 채팅 비서 서비스는 Streamlit을 이용한 웹앱입니다.
        - 답변은 OpenAI의 GPT 모델을 활용했습니다. 
        - 채팅 비서는 '짱구는 못 말려'에 나오는 나미리 선생님 역할을 부여받았습다.
        """
        )

        st.markdown("")

    # 사이드바 생성
    with st.sidebar:

        # Open AI API 키 입력받기
        openai.api_key = st.text_input(label="OPENAI API 키", placeholder="Enter Your API Key", value="", type="password")

        st.markdown("---")

        # GPT 모델을 선택하기 위한 라디오 버튼 생성
        model = st.radio(label="GPT 모델",options=["gpt-4", "gpt-3.5-turbo"])

        st.markdown("---")

        # 리셋 버튼 생성
        if st.button(label="초기화"):
            # 리셋 코드 
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role": "system", "content": "You are the teacher of the Jangmi class at Cotyledon Kindergarten.You add a spirited 'Yeehaw!' at the end of each sentence, infusing their speech with a touch of cowboy flair and boundless energy, and you must speak in Korean."}]
            st.session_state["check_reset"] = True

    # 기능 구현 공간
    col1, col2 =  st.columns(2)
    with col1:
        # 왼쪽 영역 작성
        st.subheader("🤔질문하기")
        # 음성 녹음 아이콘 추가
        audio = audiorecorder("음성질문", "녹음중...")
        if (audio.duration_seconds > 0) and (st.session_state["check_reset"]):
            # 음성 재생 
            #st.audio(audio.export().read())
            # 음원 파일에서 텍스트 추출
            question = STT(audio)

            # 채팅을 시각화하기 위해 질문 내용 저장
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"]+ [("🤔",now, question)]
            # GPT 모델에 넣을 프롬프트를 위해 질문 내용 저장
            st.session_state["messages"] = st.session_state["messages"]+ [{"role": "user", "content": question}]
            flag_start = True
        else:
            st.warning("질문을 말씀하세요.")

        
        # 텍스트 입력 상자 추가
        question = st.text_input("질문을 입력하세요", key="question")

        if st.button("질문"):
            if question and (not st.session_state["check_reset"]):
                # 채팅을 시각화하기 위해 질문 내용 저장
                now = datetime.now().strftime("%H:%M")
                st.session_state["chat"] = st.session_state["chat"] + [("🤔", now, question)]
                # GPT 모델에 넣을 프롬프트를 위해 질문 내용 저장
                st.session_state["messages"] = st.session_state["messages"] + [{"role": "user", "content": question}]
                flag_start = True
            else:
                st.warning("질문을 입력하세요.")

    
                

    with col2:
        # 오른쪽 영역 작성
        st.subheader("🤔질문/🥸답변")
        if flag_start:
            #ChatGPT에게 답변 얻기
            response = ask_gpt([{"role": "user", "content": question}], model)

            # GPT 모델에 넣을 프롬프트를 위해 답변 내용 저장
            st.session_state["messages"] = st.session_state["messages"]+ [{"role": "system", "content": response}]

            # 채팅 시각화를 위한 답변 내용 저장
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"]+ [("🥸",now, response)]

            # 채팅 형식으로 시각화 하기
            for sender, time, message in st.session_state["chat"]:
                if sender == "🤔":
                    st.write(f'<div style="display:flex;align-items:center;"><img src="https://i.namu.wiki/i/JPRWD6euNm8ETlE0psFrQ_bTtQ39bo1IIqFRiiWAlvkgUFCKOixANIr4hc0zts4Mzk9yZRd9I87FRrOQ3IhW3Baf0B3CF1VPXM6FU56m4fMPZuA7g2pBPqzMKz0gizAV-0RtuCDECizS4d25YjK6Vw.webp" width="50" height="75"><div style="background-color:#FF4500;color:white;border-radius:12px;padding:8px 8px;margin-left:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                
                else:
                    st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:#FFD700;border-radius:12px;padding:4px 8px;margin-right:8px;">{message}</div><img src="https://i.namu.wiki/i/wJK622XGoUWnt13plC6KoXDyAPclNSaVDNQoOgJ7rJjtU_1TaL0FH7XGwy8o67HG8Rqn8_iupRHw7ps0z2TWtHyIIbrnnrCs7-q9MHH5U7ctrQStpeV0avJ4FYognqCKdDXh2cbSyN8TgR57Byeqzg.webp" width="50" height="75"><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)


        elif (audio.duration_seconds > 0)  and (st.session_state["check_reset"]==False):
            # ChatGPT에게 답변 얻기
            #response = ask_gpt(st.session_state["messages"], model)
            response = ask_gpt([{"role": "user", "content": question}], model)

            # GPT 모델에 넣을 프롬프트를 위해 답변 내용 저장
            st.session_state["messages"] = st.session_state["messages"]+ [{"role": "system", "content": response}]

            # 채팅 시각화를 위한 답변 내용 저장
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"]+ [("🥸",now, response)]

            # 채팅 형식으로 시각화 하기
            for sender, time, message in st.session_state["chat"]:
                if sender == "🤔":
                    st.write(f'<div style="display:flex;align-items:center;"><img src="https://i.namu.wiki/i/JPRWD6euNm8ETlE0psFrQ_bTtQ39bo1IIqFRiiWAlvkgUFCKOixANIr4hc0zts4Mzk9yZRd9I87FRrOQ3IhW3Baf0B3CF1VPXM6FU56m4fMPZuA7g2pBPqzMKz0gizAV-0RtuCDECizS4d25YjK6Vw.webp" width="50" height="75"><div style="background-color:#FF4500;color:white;border-radius:12px;padding:8px 8px;margin-left:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                
                else:
                    st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:#FFD700;border-radius:12px;padding:4px 8px;margin-right:8px;">{message}</div><img src="https://i.namu.wiki/i/wJK622XGoUWnt13plC6KoXDyAPclNSaVDNQoOgJ7rJjtU_1TaL0FH7XGwy8o67HG8Rqn8_iupRHw7ps0z2TWtHyIIbrnnrCs7-q9MHH5U7ctrQStpeV0avJ4FYognqCKdDXh2cbSyN8TgR57Byeqzg.webp" width="50" height="75"><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)


            # gTTS 를 활용하여 음성 파일 생성 및 재생
            #TTS(response)

if __name__=="__main__":
    
    main()