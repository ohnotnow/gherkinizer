import os
from datetime import datetime

from gepetto import mistral, gpt, groq, claude, ollama

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

    return response.message

def get_user_stories(user_request, initial_thoughts):
    system_prompt = """
        You are an AI assistant who is an expert at reading a non-IT user request for new software features, an initial breakdown of the
        feature request and then turning that into a series of Gherkin Syntax User Stories. You must make sure that the User Stories are
        written in the correct format and that they cover all the possible edge-cases and error conditions that the user probably didn't
        think about. Please format each user story in Gherkin Syntax using markdown syntax.  You MUST reply with only the correctly
        formatted User Stories - no extra chat or explanation is required.  The output will be passed to another software tool which will
        break if there is any extra text.

        <example-output>
        # Feature: As a user I want to sign in so I can see my marketing campaigns

        ## Scenario: User supplies correct user name and password
        - Given that I am on the sign-in page
        - When I enter my user name and password correctly
        - And click 'Sign In'
        - Then I am taken to the dashboard

        ## Scenario: User does NOT supply correct user name and password
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

    return response.message

def main():
    request = input("Enter your feature request:\n")
    final_output = ""
    initial_thoughts = get_initial_thoughts(request)
    final_output = f"Initial Thoughts:\n{initial_thoughts.strip()}\n\n"
    print(final_output)
    user_stories = get_user_stories(request, initial_thoughts)
    final_output += f"User Stories:\n{user_stories.strip('```markdown').strip('```').strip()}"
    print(f"User Stories:\n{user_stories.strip()}")
    # save output to a file called 'user_stories_2024_01_01_12_00_00.md' (replace with current date and time)
    filename = f"user_stories_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.md"
    with open(filename, "w") as f:
        f.write(final_output)
        print(f"\n\nUser Stories saved to file : {filename}\n\n")


if __name__ == "__main__":
    main()
