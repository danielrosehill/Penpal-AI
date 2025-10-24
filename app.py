import gradio as gr
import os
from datetime import datetime
from openai import OpenAI
from typing import List, Tuple, Optional
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = None
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)

def set_api_key(key: str) -> str:
    """Set the OpenAI API key."""
    global client, api_key
    if key.strip():
        api_key = key.strip()
        client = OpenAI(api_key=api_key)
        return "API key set successfully!"
    return "Please enter a valid API key."

# Global state to store conversation threads
conversation_state = {
    "thread_history": [],
    "current_subject": None,
    "user_turn": 0,
    "ai_turn": 0
}

def generate_subject_line(user_letter: str) -> str:
    """Generate a subject line for the first letter using OpenAI."""
    if not client:
        return "General Correspondence"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates concise, descriptive subject lines for letters. Generate a subject line (max 6 words) that captures the main topic. Return ONLY the subject line, nothing else."
                },
                {
                    "role": "user",
                    "content": f"Generate a subject line for this letter:\n\n{user_letter}"
                }
            ],
            max_tokens=20,
            temperature=0.7
        )
        subject = response.choices[0].message.content.strip()
        # Remove any quotes if the model added them
        subject = subject.strip('"').strip("'")
        return subject
    except Exception as e:
        return f"General Correspondence"

def generate_ai_response(user_letter: str, subject: str) -> str:
    """Generate AI response in letter format."""
    if not client:
        return "⚠️ OpenAI API key not found. Please set OPENAI_API_KEY environment variable."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are a thoughtful pen pal who writes detailed, meaningful letters.

Your writing style should be:
- Warm and personal, like writing to a friend
- Structured like a proper letter (greeting, body, closing)
- Thoughtful and substantive - take time to explore ideas thoroughly
- Formatted in markdown for readability

Start each letter with a greeting (e.g., "Dear Friend," or "Hello,") and end with a closing (e.g., "Warm regards," or "Best wishes,") followed by "Your AI Pen Pal".

Respond to the user's letter comprehensively. This is asynchronous correspondence - take your time to provide a complete, thoughtful response in a single letter."""
                },
                {
                    "role": "user",
                    "content": user_letter
                }
            ],
            temperature=0.8,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error generating response: {str(e)}"

def format_letter_header(subject: str, turn_type: str, turn_number: int) -> str:
    """Format the letter header with subject line."""
    date_str = datetime.now().strftime("%B %d, %Y")
    return f"**Re: {subject} ({turn_type} {turn_number})**\n\n*{date_str}*\n\n---\n\n"

def send_letter(user_letter: str, thread_history: List):
    """Process user letter and generate AI response."""
    if not user_letter.strip():
        # Determine labels based on conversation state
        is_first = conversation_state["current_subject"] is None
        btn_text = "Send Letter" if is_first else "Send Reply"
        input_label = "Your Letter" if is_first else "Your Reply"
        input_placeholder = "Dear AI Pen Pal,\n\nI've been thinking about..." if is_first else "Dear AI Pen Pal,\n\nThank you for your letter. In response..."
        section_title = "## Compose Your Letter" if is_first else "## Compose Your Reply"

        return (
            "",
            "Please write a letter before sending.",
            thread_history,
            "",
            "",
            gr.update(value=btn_text),
            gr.update(label=input_label, placeholder=input_placeholder),
            gr.update(value=section_title)
        )

    # Generate subject line if this is the first letter
    if conversation_state["current_subject"] is None:
        conversation_state["current_subject"] = generate_subject_line(user_letter)
        conversation_state["user_turn"] = 0
        conversation_state["ai_turn"] = 0

    # Increment turn counters
    conversation_state["user_turn"] += 1
    subject = conversation_state["current_subject"]

    # Format user letter with header
    user_header = format_letter_header(subject, "User Prompt", conversation_state["user_turn"])
    formatted_user_letter = user_header + user_letter

    # Add user letter to thread
    thread_history.append({
        "type": "user",
        "content": formatted_user_letter,
        "timestamp": datetime.now().isoformat()
    })

    # Generate AI response
    ai_response_content = generate_ai_response(user_letter, subject)

    # Increment AI turn
    conversation_state["ai_turn"] += 1

    # Format AI response with header
    ai_header = format_letter_header(subject, "AI Reply", conversation_state["ai_turn"])
    formatted_ai_response = ai_header + ai_response_content

    # Add AI response to thread
    thread_history.append({
        "type": "ai",
        "content": formatted_ai_response,
        "timestamp": datetime.now().isoformat()
    })

    # Build thread display
    thread_display = build_thread_display(thread_history)

    # Update UI labels for reply mode
    btn_text = "Send Reply"
    input_label = "Your Reply"
    input_placeholder = "Dear AI Pen Pal,\n\nThank you for your letter. In response..."
    section_title = "## Compose Your Reply"

    # Clear user input and show AI response
    return (
        "",
        formatted_ai_response,
        thread_history,
        thread_display,
        formatted_user_letter,
        gr.update(value=btn_text),
        gr.update(label=input_label, placeholder=input_placeholder),
        gr.update(value=section_title)
    )

def build_thread_display(thread_history: List) -> str:
    """Build formatted thread history display."""
    if not thread_history:
        return "*No letters yet. Start writing!*"

    thread_md = "# Letter Thread\n\n"
    for i, letter in enumerate(thread_history):
        if letter["type"] == "user":
            avatar_img = '<img src="file/images/human.png" width="40" style="border-radius: 50%; vertical-align: middle; margin-right: 10px;">'
            sender = f'{avatar_img} **You**'
        else:
            avatar_img = '<img src="file/images/ai.png" width="40" style="border-radius: 50%; vertical-align: middle; margin-right: 10px;">'
            sender = f'{avatar_img} **AI Pen Pal**'

        thread_md += f"### {sender}\n\n{letter['content']}\n\n---\n\n"

    return thread_md

def download_letter(letter_content: str, letter_type: str) -> str:
    """Prepare letter content for download."""
    if not letter_content:
        return "# No letter to download\n\nPlease send a letter first."
    return letter_content

def new_conversation():
    """Start a new conversation thread."""
    conversation_state["thread_history"] = []
    conversation_state["current_subject"] = None
    conversation_state["user_turn"] = 0
    conversation_state["ai_turn"] = 0

    return (
        "",
        "",
        [],
        "*No letters yet. Start writing!*",
        "",
        gr.update(value="Send Letter"),
        gr.update(label="Your Letter", placeholder="Dear AI Pen Pal,\n\nI've been thinking about..."),
        gr.update(value="## Compose Your Letter")
    )

# Custom CSS for letter-writing aesthetic
custom_css = """
.letter-box textarea {
    font-family: 'Georgia', 'Times New Roman', serif !important;
    font-size: 16px !important;
    line-height: 1.8 !important;
    padding: 20px !important;
}

.gradio-container {
    font-family: 'Georgia', 'Times New Roman', serif !important;
}

#thread-history {
    background-color: #f9f7f4;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #d4c5b9;
}

.letter-display {
    background-color: #fffef8;
    padding: 25px;
    border-left: 4px solid #8b7355;
}

.mic-button {
    min-width: 50px !important;
}
"""

# JavaScript for speech-to-text
speech_to_text_js = """
function setupSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert('Speech recognition is not supported in your browser. Please use Chrome, Edge, or Safari.');
        return null;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    return recognition;
}

let recognition = null;
let isRecording = false;
let fullTranscript = '';

function toggleSpeechRecognition(currentText) {
    if (!recognition) {
        recognition = setupSpeechRecognition();
        if (!recognition) return [currentText, 'Start Dictation'];
    }

    if (isRecording) {
        recognition.stop();
        isRecording = false;
        return [currentText, 'Start Dictation'];
    } else {
        fullTranscript = currentText || '';

        recognition.onresult = (event) => {
            let interimTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    fullTranscript += (fullTranscript ? ' ' : '') + transcript;
                } else {
                    interimTranscript += transcript;
                }
            }

            const textarea = document.querySelector('.letter-box textarea');
            if (textarea) {
                textarea.value = fullTranscript + (interimTranscript ? ' ' + interimTranscript : '');
                textarea.dispatchEvent(new Event('input', { bubbles: true }));
            }
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            isRecording = false;
            const button = document.querySelector('.mic-button');
            if (button) button.value = 'Start Dictation';
        };

        recognition.onend = () => {
            if (isRecording) {
                recognition.start();
            }
        };

        recognition.start();
        isRecording = true;
        return [fullTranscript, 'Stop Dictation'];
    }
}
"""

# Build Gradio interface
with gr.Blocks(css=custom_css, title="Pen Pal AI - Letter Exchange", theme=gr.themes.Soft()) as demo:
    # Header image
    gr.Image("demo-header.png", show_label=False, show_download_button=False, container=False)

    gr.Markdown("""
    Welcome to a different kind of AI conversation. Write thoughtful, long-form letters and receive detailed responses.

    **How it works:**
    1. Set your OpenAI API key below (if not already configured)
    2. Write your letter in the text area
    3. Click "Send Letter" or use dictation
    4. Receive a reply from your AI pen pal
    5. Download any letter as markdown

    This is asynchronous correspondence - take your time, be thoughtful, and enjoy the exchange!
    """)

    # API Key Configuration
    with gr.Accordion("API Key Configuration (BYOK)", open=False):
        gr.Markdown("""
        This app requires an OpenAI API key. You can get one at [platform.openai.com](https://platform.openai.com/api-keys).

        **For Hugging Face Spaces:** Set your key as a secret named `OPENAI_API_KEY` in your Space settings.

        **For local use:** You can also set it here temporarily (not saved between sessions).
        """)

        with gr.Row():
            api_key_input = gr.Textbox(
                label="OpenAI API Key",
                placeholder="sk-...",
                type="password",
                scale=3
            )
            set_key_btn = gr.Button("Set API Key", size="sm", scale=1)

        api_key_status = gr.Markdown("")

    # Hidden state for thread history
    thread_state = gr.State([])

    with gr.Row():
        with gr.Column(scale=1):
            compose_section_title = gr.Markdown("## Compose Your Letter")

            user_input = gr.Textbox(
                label="Your Letter",
                placeholder="Dear AI Pen Pal,\n\nI've been thinking about...",
                lines=15,
                elem_classes=["letter-box"]
            )

            with gr.Row():
                mic_btn = gr.Button("Start Dictation", size="sm", elem_classes=["mic-button"])

            with gr.Row():
                send_btn = gr.Button("Send Letter", variant="primary", size="lg")
                new_conv_btn = gr.Button("New Conversation", size="lg")

            gr.Markdown("---")

            gr.Markdown("### Your Last Letter")
            user_letter_display = gr.Markdown(
                value="*Your letter will appear here after sending*",
                elem_classes=["letter-display"]
            )
            download_user = gr.DownloadButton(
                label="Download Your Letter",
                size="sm"
            )

        with gr.Column(scale=1):
            gr.Markdown("## AI Reply")

            ai_response = gr.Markdown(
                value="*Waiting for your letter...*",
                elem_classes=["letter-display"]
            )

            download_ai = gr.DownloadButton(
                label="Download AI Reply",
                size="sm"
            )

    gr.Markdown("---")

    gr.Markdown("## Letter Thread")
    thread_display = gr.Markdown(
        value="*No letters yet. Start writing!*",
        elem_id="thread-history"
    )

    # Event handlers
    set_key_btn.click(
        fn=set_api_key,
        inputs=[api_key_input],
        outputs=[api_key_status]
    )

    send_btn.click(
        fn=send_letter,
        inputs=[user_input, thread_state],
        outputs=[user_input, ai_response, thread_state, thread_display, user_letter_display, send_btn, user_input, compose_section_title]
    )

    new_conv_btn.click(
        fn=new_conversation,
        inputs=[],
        outputs=[user_input, ai_response, thread_state, thread_display, user_letter_display, send_btn, user_input, compose_section_title]
    )

    # Speech-to-text handler
    mic_btn.click(
        fn=None,
        inputs=[user_input],
        outputs=[user_input, mic_btn],
        js=speech_to_text_js.replace("function toggleSpeechRecognition", "function(currentText) { return toggleSpeechRecognition")
    )

    # Download handlers
    user_letter_display.change(
        fn=lambda x: gr.DownloadButton(
            label="Download Your Letter",
            value=x if x and x != "*Your letter will appear here after sending*" else None,
            visible=bool(x and x != "*Your letter will appear here after sending*")
        ),
        inputs=[user_letter_display],
        outputs=[download_user]
    )

    ai_response.change(
        fn=lambda x: gr.DownloadButton(
            label="Download AI Reply",
            value=x if x and x != "*Waiting for your letter...*" else None,
            visible=bool(x and x != "*Waiting for your letter...*")
        ),
        inputs=[ai_response],
        outputs=[download_ai]
    )

if __name__ == "__main__":
    demo.launch(share=False)
