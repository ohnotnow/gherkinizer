# Gherkin-Style User Story Generator

This Python script is designed to assist in converting non-IT user feature requests into detailed Gherkin-style user stories. It utilizes a selection of AI chatbot models to first break down the natural language feature requests into initial thoughts, and then transform these thoughts into structured user stories in Gherkin syntax.

## Installation

To run this script, you'll need Python installed on your machine along with several dependencies.

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/ohnotnow/gherkinizer.git
    cd gherkinizer
    ```

2. **Install Dependencies:**

    This script requires specific Python libraries. You can install them using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Before running the script, ensure that the environment variable `BOT_PROVIDER` is set to the chatbot model you intend to use (`mistral`, `groq`, `claude`, or `ollama`). If it's not set, the script defaults to using `gpt.GPTModelSync()`.  You will also need an API key for your chosen model provider. Eg, `export OPENAI_API_KEY=sk-......`

## Usage

To use this script:

1. **Run the Script:**

    ```bash
    python main.py
    ```

2. **Enter a Feature Request:**

    When prompted, enter the non-IT user feature request. The script will then output the initial thoughts and the Gherkin-style user stories.

3. **User Stories Output:**

    The generated user stories are printed to the console and also saved to a markdown file named with the current date and time (e.g., `user_stories_2024_01_01_12_00_00.md`).

## Features

- Supports multiple AI chatbot models.
- Converts natural language feature requests into Gherkin-style user stories.
- Saves user stories in a markdown file for easy access and documentation.

## Contributing

If you'd like to contribute to the project, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Licensing

MIT License.
