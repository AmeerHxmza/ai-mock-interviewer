# frontend/gradio_ui.py

import gradio as gr
from core.interviewer import start_interview, submit_answer, restart_interview

with gr.Blocks(title="🎙️ AI Mock Interviewer") as demo:
    gr.Markdown("""
    <div style='text-align: center;'>
        <h1 style='color:#ffb347;'>🤖 The AI Mock Interviewer</h1>
        <p>Upload your CV, pick a category, and answer via <b>voice or text</b>.</p>
    </div>
    """)

    with gr.Row():
        cv_input = gr.File(label="📄 Upload Your CV", file_types=[".pdf", ".docx"])
        cat_input = gr.Radio(
            ["Technical", "Behavioral", "Problem Solving", "Leadership"],
            label="📂 Select Interview Category",
            info="Choose your interview type"
        )

    start_btn = gr.Button("🚀 Start Interview")
    start_output = gr.Textbox(label="🛠️ System Message", lines=2)
    question_box = gr.Textbox(label="🗣️ Interview Question", lines=4)
    
    # Set autoplay=True so audio plays automatically
    question_audio = gr.Audio(label="🔊 Listen to Question", interactive=False, autoplay=True)

    with gr.Row():
        text_input = gr.Textbox(label="✍️ Type Your Answer")
        audio_input = gr.Audio(type="filepath", label="🎤 Or Speak Your Answer")

    submit_btn = gr.Button("✅ Submit Answer")
    restart_btn = gr.Button("🔁 Restart")

    start_btn.click(
        fn=start_interview,
        inputs=[cat_input, cv_input],
        outputs=[start_output, question_box, question_audio]
    )

    submit_btn.click(
        fn=submit_answer,
        inputs=[text_input, audio_input],
        outputs=[start_output, question_box, question_audio]
    ).then(
        fn=lambda: ("", None),  # clears text + audio input
        inputs=[],
        outputs=[text_input, audio_input]
    )

    restart_btn.click(
        fn=restart_interview,
        outputs=[start_output, question_box, question_audio]
    )
