I am a huge fan of an unconventional method of prompting that doesn't really fit well into existing UIs or nomenclatures.

Conversational AI is typically implemented as a "chatbot." The UI is basically modelled after human to human chat interfaces - so the AI tool fulfills the role of a virtual human in the "conversation."

I discovered "long form" prompting when I got into voice tech (STT). I found that long prompts posed little challenge to context windows and allowed for dramatically better inference because they allowed you to seed context within the prompts - without requiring RAG etc. 

The usual flow is this; user writes as long prompt. AI is sytem prompted to instruct it to respond in one go. Often this is achieved with a completions endpoint which is separate in the API from chat. 

Here's an idea I had today and what I'd like to experiment with here:

What if the UI were modelled after ... writing letters (it could be emails, but this is more quaint!). The user has a big text area, maybe some CSS styling, and a send to AI button.

The AI tool is instructed to respond to the user with its own letter. On an actual frontend this could be animated with an inbox symbol (etc) but on Gradio we can keep it simple.

In formal letter writing, correspondents include a subject line. I would like us to use the same system. The first user prompt will get an AI generated title and then be formed to a title like Re: RAG vs API (User Prompt 1). The title will hold throughout the "letter" exchange but the suffix will change. The first AI turn will be Re: RAG vs API (AI Reply 1). The  AI tool can have an avatar. 

I would like to have a download button for each "letter" which downloads it as markdown. And ideally a thread history in which each "letter" is shown in sequence. 

The point of this experiment:

I love the single turn method but I think that its "secret sauce" is that: its single turn and has no context window. This may be too much to implement in a gradio model to be deplyoed on hugging face but we could try to implement context truncation.

At the last, my idea is to try to see what this would look like in practice: there's workflow AI (non interactive) and conversational AI. This would be a conversational but async implementation. Coupled with notifications and an actual email-like inbox system, it could actually be a very interesting method of using AI for folks (like me!) who naturally prefer this more relaxed form of corresopndence. 




