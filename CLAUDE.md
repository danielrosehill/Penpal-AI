# CLAUDE.md - Pen Pal AI Project

## Project Concept

Pen Pal AI is an experimental Gradio interface that reimagines conversational AI through the metaphor of letter writing. Instead of typical chatbot interfaces, this creates an asynchronous, thoughtful correspondence experience.

## Core Philosophy

### Long-Form Prompting
- User writes substantial, detailed prompts (like composing a letter)
- AI responds comprehensively in a single turn (like writing a reply letter)
- Focus on thoughtful, asynchronous communication rather than rapid chat exchanges

### Inspiration
The project stems from discovering that long-form prompts:
- Pose no challenge to modern context windows
- Allow dramatically better inference by seeding context within prompts
- Eliminate the need for RAG or other complex context management
- Work particularly well with voice-to-text input (STT)

## UI/UX Design

### Letter-Writing Interface
- Large text area for composing letters (styled like writing paper)
- "Send to AI" button (conceptually like mailing a letter)
- Subject line system based on formal correspondence conventions
- Letter headers showing: `Re: [Topic] (User Prompt N)` or `Re: [Topic] (AI Reply N)`

### Thread Management
- First user prompt triggers AI-generated subject line
- Subject line persists throughout the exchange
- Turn numbering: User Prompt 1, AI Reply 1, User Prompt 2, AI Reply 2, etc.
- Thread history displays all letters in sequence

### Features
- **Download functionality**: Each letter can be downloaded as markdown
- **Thread history**: Visual display of all letters in the conversation
- **AI avatar**: Visual representation for the AI correspondent
- **Inbox concept**: Future enhancement could include inbox symbols/animations

## Technical Implementation

### Context Window Strategy
The "secret sauce" is single-turn interaction with no persistent context window:
- Each letter is treated as an independent interaction
- Optional: Context truncation to enforce this paradigm
- Prevents the AI from building up conversation history
- Encourages users to be thorough in each letter

### Technology Stack
- **Frontend**: Gradio (for rapid prototyping and Hugging Face deployment)
- **LLM**: OpenAI API (completions endpoint preferred for single-turn responses)
- **Format**: Markdown for letter content and downloads

## Use Cases

### Conversational but Asynchronous
This sits between two paradigms:
- **Workflow AI**: Non-interactive, task-oriented
- **Conversational AI**: Interactive, real-time chat

Pen Pal AI creates a third category:
- Conversational (back-and-forth exchange)
- Asynchronous (thoughtful, non-real-time)
- Relaxed correspondence style

### Target Users
Ideal for people who:
- Prefer thoughtful, detailed communication over rapid chat
- Want to explore ideas in depth
- Appreciate the ritual of letter writing
- Use voice-to-text for input (natural fit for long-form)

## Future Enhancements

### Notification System
- Email-like notifications when "letter arrives"
- Actual inbox interface showing received letters
- Could integrate with email for true async correspondence

### Context Management
- Optional context truncation settings
- User control over how much history AI can "remember"
- Experimentation with single-turn vs. limited context

## Deployment

### Local Testing
- Gradio interface for rapid iteration
- OpenAI API integration for testing

### Hugging Face Spaces
- Deploy as public Hugging Face Space
- Use Hugging Face Secrets for API key management
- Share as experimental interface for community feedback

## Project Goals

1. **Validate the concept**: Does letter-writing metaphor resonate with users?
2. **Test single-turn paradigm**: Is this more effective than traditional chat?
3. **Gather feedback**: Learn what works and what doesn't
4. **Explore async AI**: Create a new category of AI interaction

## Development Notes

- Keep Gradio implementation simple for initial prototype
- Focus on core letter-writing experience first
- Add advanced features (context control, notifications) after validation
- Prioritize markdown formatting for readability
- Ensure clean download functionality for archiving letters
