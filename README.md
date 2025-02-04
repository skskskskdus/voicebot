# 🤖 Streamlit Chatbot 음성 비서 챗봇 웹 프로그램 
#### OpenAI API를 이용하여 "짱구는 못말려"에 나오는 짱구와 나미리 선생님 역할을 부여하여 재미있는 음성 비서 챗봇을 만들어보았습니다.

## 📌 프로젝트 개요
#### 해당 프로젝트는 Streamlit과 gTTS 라이브러리를 활용하여 음성 비서 챗봇 웹 앱입니다.
#### 사용자가 음성 또는 텍스트를 입력하면 GPT 모델이 답변을 제공합니다.
#### 보통 챗봇과는 다르게 gTTS를 통해 텍스트를 음성으로 내보낼 수 있는 기능이 있습니다.
#### 사용자의 입력에 따라 GPT 모델을 선택할 수 있습니다.
#### OpenAI API를 웹 앱 프로젝트에 활용하는 경험을 얻을 수 있도록 있었습니다.

<img width="1276" alt="image" src="https://github.com/user-attachments/assets/54a122b7-adf8-4d13-a69d-ce7d49ec0f22" />
<img width="980" alt="image" src="https://github.com/user-attachments/assets/583653b8-e875-4fd6-b5c4-2fd569e725c4" />

## 🪛 주요 기능
#### ✔️ 텍스트 및 음성 입력 기능
#### ✔️ 다양한 GPT 모델 선택 가능(GPT-4,GPT-3.5-turbo)
#### ✔️ TTS(Text-to-Speech) 기능

##  🗂️ 프로젝트 구조

#### 📦 practice_streamlit
#### ├── 📄 ch03_voicebot.py            //Streamlit 메인 코드
####  ├── 📄 requirements.txt   // 필요한 라이브러리 목록
#### └── 📄 README.md         // 프로젝트 설명서

# 🪛 사용한 기술

####   Python 3.10.0
####   Steamlit
####   HTML + CSS
####   OpenAI API
####   gTTS

# ⭐ 실행방법

### 1. 가상 환경 생성 및 실행

#### 프로젝트 폴더에서 실행

#### python -m venv venv
#### source venv/bin/activate  # macOS/Linux
#### venv\Scripts\activate  # Windows

### 2. 필수 패키지 설치

#### pip install -r requirements.txt

### 3. Streamlit 앱 실행
#### streamlit run ch03_voicebot.py
