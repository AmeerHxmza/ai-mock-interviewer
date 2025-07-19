# main.py
from frontend.gradio_ui import demo

if __name__ == "__main__":
    demo.launch(share=True, debug=True)
