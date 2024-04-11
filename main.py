import os
from datetime import datetime
from gepetto import mistral, gpt, groq, claude, ollama
from yaspin import yaspin

def get_chatbot():
    chatbot = None
    if os.getenv("BOT_PROVIDER") == 'mistral':
        chatbot = mistral.MistralModelSync()
    elif os.getenv("BOT_PROVIDER") == 'groq':
        chatbot = groq.GroqModelSync()
    elif os.getenv("BOT_PROVIDER") == 'claude':
        chatbot = claude.ClaudeModelSync()
    elif os.getenv("BOT_PROVIDER") == 'ollama':
        chatbot = ollama.OllamaModelSync()
    else:
        chatbot = gpt.GPTModelSync()
    return chatbot

@yaspin(text="Getting initial thoughts...", color="yellow")
def get_initial_thoughts(user_request):
    system_prompt = """
        You are an AI assistant who is an expert at breaking down a non-IT users natural language feature requests for software
        applications and figuring out the individual parts of the request. You spend time thinking of the both the 'happy path' features required
         and also edge-cases and error conditions which the user probably doesn't think about. The goal is to provide a detailed breakdown of
         the feature request so that it can then be turned into User Stories.  You should not attempt to write the user stories yourself,
        but just provide the detailed breakdown of the feature request.
    """

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"Could you help me with a feature request?\n\n <request>{user_request}</request>"
        }
    ]

    bot = get_chatbot()
    response = bot.chat(messages)

    return response

@yaspin(text="Getting user stories...", color="yellow")
def get_user_stories(user_request, initial_thoughts):
    system_prompt = """
        You are an AI assistant who is an expert at reading a non-IT user request for new software features, an initial breakdown of the
        feature request and then turning that into a series of Gherkin Syntax User Stories. You must make sure that the User Stories are
        written in the correct format and that they cover all the possible edge-cases and error conditions that the user probably didn't
        think about. Please format each user story in Gherkin Syntax using markdown syntax.  You MUST reply with only the correctly
        formatted User Stories - no extra chat or explanation is required.  The output will be passed to another software tool which will
        break if there is any extra text.

        <example-output>
        ### Feature: As a user I want to sign in so I can see my marketing campaigns

        #### Scenario: User supplies correct user name and password
        - Given that I am on the sign-in page
        - When I enter my user name and password correctly
        - And click 'Sign In'
        - Then I am taken to the dashboard

        #### Scenario: User does NOT supply correct user name and password
        - Given that I am on the sign-in page
        - When I enter my user name and password incorrectly
        - and click 'Sign In'
        - Then I see an error message 'Sorry, incorrect user name or password.'

        </example-output>
    """

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"Could you help me with a feature request?\n\n <initial-request>{user_request}</initial-request>\n\n <initial-breakdown>{initial_thoughts}</initial-breakdown>"
        }
    ]

    bot = get_chatbot()
    response = bot.chat(messages)

    return response

def main():
    total_cost = 0
    request = input("Enter your feature request:\n")
    final_output = f"# User Request\n\n> {request}\n\n"
    finished_asking_clarifying_questions = False
    conversation = [
        {
            "role": "system",
            "content": f"You are an AI assistant who is an expert at asking clarifying questions ONE AT A TIME about non-IT users natural language feature requests for software applications.  You should ask questions to get more information about the feature request in order to help developers understand the exact nature of the request. Remember to only ask them one question at a time so they are not overwhelmed. The USER is non-technical so might not be able to answer a technically worded question. If you do not need to ask any more questions please reply with simple the word 'COMPLETE'."
        },
        {
            "role": "user",
            "content": f"I need a feature to be developed.  Could you help me by asking some clarifying questions?  My feature request is : {request}"
        },
    ]
    bot = get_chatbot()
    start_time_clarifying = datetime.now()
    while not finished_asking_clarifying_questions:
        response = bot.chat(conversation)
        total_cost += response.cost
        if response.message.startswith("COMPLETE"):
            finished_asking_clarifying_questions = True
            break
        print(f"\n\nQ. {response.message}\n\n")
        answer = input("A. ")
        conversation.append(
            {"role": "assistant", "content": response.message}
        )
        conversation.append(
            {"role": "user", "content": answer}
        )
        if len(conversation) > 14:
            finished_asking_clarifying_questions = True
            break

    if len(conversation) > 2:
        final_output += f"## Clarifying Questions\n\n"
        for i in range(2, len(conversation), 2):
            final_output += f"**Q. {conversation[i]['content']}**\n\n**A.** {conversation[i+1]['content']}\n\n"

    stop_time_clarifying = datetime.now()
    start_time_llm = datetime.now()
    response = get_initial_thoughts(final_output)
    total_cost += response.cost
    initial_thoughts = response.message
    final_output += f"## Initial Thoughts:\n{initial_thoughts.strip()}\n\n"
    response = get_user_stories(request, initial_thoughts)
    total_cost += response.cost
    user_stories = response.message
    final_cost = f"\n\n#### Stats\n\n- Total Cost: US${round(total_cost, 4)}"
    final_output += f"## User Stories:\n{user_stories.strip('```markdown').strip('```').strip()}"
    final_output += final_cost
    end_time_llm = datetime.now()
    total_time_taken = round((end_time_llm - start_time_clarifying).total_seconds(), 2)
    total_time_clarifying = round((stop_time_clarifying - start_time_clarifying).total_seconds(), 2)
    total_time_llm = round((end_time_llm - start_time_llm).total_seconds(), 2)
    final_output += f"\n\n- Time taken: {total_time_taken} seconds (Clarifying: {total_time_clarifying} seconds, LLM: {total_time_llm} seconds)\n\n"
    filename = f"user_stories_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.md"
    with open(filename, "w") as f:
        f.write(final_output)
        print(f"\n\nResults saved to file : {filename}\n\n")


if __name__ == "__main__":
    main()
