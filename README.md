---
title: Pen Pal AI
emoji: 📮
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
license: mit
---

# Pen Pal AI - Letter Exchange

![alt text](image.png)

An experimental AI interface that reimagines conversational AI through the timeless metaphor of letter writing. Instead of rapid-fire chatbot exchanges, Pen Pal AI encourages thoughtful, long-form correspondence with an AI pen pal.

## 🎯 Concept

Traditional conversational AI is modeled after instant messaging - quick back-and-forth exchanges. Pen Pal AI explores a different paradigm:

- **Asynchronous**: Take your time composing thoughtful letters
- **Long-form**: Write detailed, context-rich prompts without worrying about length
- **Single-turn focus**: Each letter gets a complete, comprehensive response
- **Relaxed correspondence**: More like writing to a friend than querying a chatbot

## ✨ Features

- 📝 **Letter-writing interface** with serif fonts and comfortable styling
- 📬 **Automatic subject line generation** for each conversation thread
- 🔢 **Turn tracking** - User Prompt 1, AI Reply 1, User Prompt 2, etc.
- 📚 **Thread history** showing all letters in chronological order
- 💾 **Markdown downloads** for each letter (preserve your correspondence!)
- 🔄 **New conversation** button to start fresh threads

## 🚀 Quick Start

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/danielrosehill/Penpal-AI.git
   cd Penpal-AI
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Open your browser** to the URL shown in the terminal (typically `http://localhost:7860`)

## 🔑 API Key Setup

This application uses OpenAI's API. You'll need:

1. An OpenAI API account ([sign up here](https://platform.openai.com/signup))
2. An API key ([get one here](https://platform.openai.com/api-keys))
3. Add the key to your `.env` file:
   ```
   OPENAI_API_KEY=sk-...your-key-here
   ```

## 📖 How to Use

1. **Compose your letter** in the text area on the left
2. Click **"📮 Send Letter"**
3. Your letter appears in the "Your Last Letter" section
4. The AI's reply appears on the right side
5. View the **complete thread history** at the bottom
6. Download any letter using the **💾 Download** buttons
7. Start a **new conversation** anytime with the 🔄 button

## 💡 Tips for Best Results

- **Write naturally** - compose as if writing to a thoughtful friend
- **Provide context** - since each letter is self-contained, include relevant background
- **Ask complex questions** - this format excels at exploring ideas in depth
- **Take your time** - this isn't instant messaging, it's correspondence
- **Use voice-to-text** - long-form prompts work wonderfully with STT

## 🎨 The Philosophy

This project explores what happens when we:
- Reject the chat interface paradigm
- Embrace asynchronous, thoughtful communication
- Encourage long-form, context-rich prompts
- Treat AI interaction more like correspondence than commands

The hypothesis: This approach might work better for certain types of thinking, exploration, and creative work.

## 🌐 Deployment to Hugging Face

### Option 1: Deploy via Hugging Face Spaces UI

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose "Gradio" as the SDK
4. Upload `app.py` and `requirements.txt`
5. Add your `OPENAI_API_KEY` in Settings → Repository Secrets
6. Your space will build and deploy automatically!

### Option 2: Deploy via Git

1. Create a new Space on Hugging Face
2. Clone the Space repository:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME
   cd SPACE_NAME
   ```
3. Copy files:
   ```bash
   cp /path/to/Penpal-AI/app.py .
   cp /path/to/Penpal-AI/requirements.txt .
   ```
4. Commit and push:
   ```bash
   git add app.py requirements.txt
   git commit -m "Initial deployment of Pen Pal AI"
   git push
   ```
5. Add `OPENAI_API_KEY` in Space Settings → Repository Secrets

## 🛠️ Technical Details

- **Framework**: Gradio 5.49.1
- **LLM**: OpenAI GPT-4o (for responses) and GPT-4o-mini (for subject generation)
- **Language**: Python 3.12+
- **Deployment**: Compatible with Hugging Face Spaces

## 🤔 Why This Exists

The creator discovered that long-form prompting, especially with voice-to-text input, produces better AI interactions than traditional chat. This interface explores that insight by creating a UI that encourages and celebrates long-form correspondence.

It sits between:
- **Workflow AI** (non-interactive, task-oriented)
- **Conversational AI** (interactive chat)

Creating a third category: **Correspondence AI** (conversational but asynchronous)

## 🔮 Future Ideas

- Email-style notifications when "letters arrive"
- Context truncation controls (experiment with memory vs. fresh-start)
- User-selectable AI "personalities" or writing styles
- Export entire threads as formatted PDFs
- Integration with actual email for true async correspondence

## 📝 License

MIT License

## 🙏 Acknowledgments

Inspired by the art of letter writing and the belief that slower, more thoughtful communication can be powerful even (or especially) with AI.

## 📧 Contact

For questions, suggestions, or to share your experience:
- **Website**: danielrosehill.com
- **Email**: public@danielrosehill.com

---

*Built with ✉️ by Daniel Rosehill*
