from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from core.state import cv_text, selected_category, questions, current_index, user_answers
from utils.cv_utils import extract_cv_text
from utils.audio_utils import speak
from models.whisper_model import transcribe_audio
from utils.config import OPENAI_API_KEY

llm = ChatOpenAI(model="gpt-4o", temperature=0.7, openai_api_key=OPENAI_API_KEY)

question_prompt = PromptTemplate.from_template(
    "You are an expert interviewer. Given the following CV:\n{cv_text}\n"
    "and the interview category: {category}, generate exactly 5 professional interview questions.\n"
    "Format them as:\n1. ...\n2. ...\n3. ...\n4. ...\n5. ..."
)

score_prompt = PromptTemplate.from_template(
    "Given this CV:\n{cv}\nCategory: {cat}\nQuestions:\n{qs}\nAnswers:\n{ans}\n"
    "Evaluate the answers and give a final score out of 100 with brief feedback."
)

def set_cv(file_path):
    global cv_text
    cv_text = extract_cv_text(file_path)

def generate_questions(cv, category):
    try:
        response = llm.invoke(question_prompt.format(cv_text=cv, category=category)).content
        return [q.strip() for q in response.split('\n') if q.strip() and q[0].isdigit()]
    except Exception as e:
        raise Exception(f"❌ Question generation failed: {e}")

def evaluate_answers(cv, category, qs, ans):
    try:
        result = llm.invoke(score_prompt.format(
            cv=cv, cat=category, qs="\n".join(qs), ans="\n".join(ans)
        )).content
        return result
    except Exception as e:
        raise Exception(f"❌ Evaluation failed: {e}")

def start_interview(category, cv_file=None):
    global selected_category, questions, current_index, user_answers, cv_text
    selected_category = category
    current_index = 0
    user_answers = []
    questions.clear()

    if cv_file:
        try:
            set_cv(cv_file)
        except Exception as e:
            return f"❌ Failed to process CV: {e}", "", None
    elif not cv_text:
        return "⚠️ Please upload your CV to start the interview.", "", None

    try:
        questions.extend(generate_questions(cv_text, category))
    except Exception as e:
        return str(e), "", None

    if not questions:
        return "❌ No questions were generated. Try again.", "", None

    audio = speak(questions[current_index], filename="question.wav")
    return "✅ Interview started. First question is:", questions[current_index], audio

def submit_answer(text_input, audio_input):
    global current_index, questions, user_answers

    if not questions:
        return "⚠️ Interview not started. Please start first.", "", None

    answer_text = text_input.strip()
    if audio_input:
        try:
            answer_text = transcribe_audio(audio_input)
        except Exception as e:
            return f"❌ Audio transcription failed: {e}", "", None

    if not answer_text:
        return "⚠️ Please provide a valid answer.", "", None

    user_answers.append(answer_text)
    current_index += 1

    if current_index < len(questions):
        audio = speak(questions[current_index], filename="question.wav")
        return "✅ Answer recorded. Next question:", questions[current_index], audio
    else:
        result = evaluate_answers(cv_text, selected_category, questions, user_answers)
        return "🎉 Interview completed! Your result:", result, None

def restart_interview():
    global selected_category, questions, current_index, user_answers
    selected_category = ""
    questions.clear()
    current_index = 0
    user_answers.clear()
    return "🔄 Interview reset. Please start again.", "", None
