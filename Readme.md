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
    python -mvenv venv
    source venv/bin/activate
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

## Example

**User request**
> I would like to add a new import to our Student Project web app.  It should let me upload an Excel file containing a project ID and a second supervisor GUID. Once uploaded I should be able to see the second supervisor listed in a table alongside the project and primary supervisor.  When students log in they should be able to see the second supervisor in brackets next to the primary supervisor for each project they can see.

**Result**
```
**Initial Thoughts:**
Certainly! Let's break down your feature request for the Student Project web app into individual components and considerations:

1. **Excel File Upload Functionality:**
   - A new interface element for users to upload Excel files.
   - File type and format validation to ensure the uploaded file is indeed an Excel file (.xls, .xlsx).
   - Size limitation checks to prevent very large files from being uploaded.
   - Security measures to scan for potentially malicious files.

2. **Data Extraction from Excel:**
   - Parsing the Excel file to read the contents.
   - Identifying and extracting the relevant columns: Project ID and Second Supervisor GUID.
   - Handling different Excel versions and formats to ensure compatibility.
   - Data validation to ensure that the Project ID and Second Supervisor GUID are in the correct format and are valid entries within the system's context.

3. **Database Integration:**
   - Updating the database schema if necessary to accommodate the second supervisor information.
   - Writing the logic to insert or update the second supervisor's details in the database based on the Project ID.
   - Handling cases where the Project ID does not exist or is incorrect.
   - Ensuring data integrity and preventing duplication of entries.

4. **User Interface Updates for Admin View:**
   - Modifying the admin view to include a new column or section in the existing table to display the second supervisor's information.
   - Ensuring that the display of the second supervisor is clear and distinguishable from the primary supervisor.
   - Providing feedback to the user after the upload process is complete, such as success or error messages.

5. **User Interface Updates for Student View:**
   - Adjusting the student view to show the second supervisor in brackets next to the primary supervisor.
   - Ensuring this information is displayed in a user-friendly manner.
   - Making sure that the additional information does not clutter the interface or overwhelm the student users.

6. **Access Control and Permissions:**
   - Confirming that only authorized users (e.g., admins or staff) can upload and modify the second supervisor information.
   - Ensuring that students have read-only access to this information and cannot alter it.

7. **Error Handling and Edge Cases:**
   - Providing meaningful error messages for various failure scenarios (e.g., upload failure, incorrect data format, invalid Project ID).
   - Handling edge cases such as multiple entries for the same Project ID with different second supervisors.
   - Deciding on the behavior if a second supervisor GUID does not match any existing user in the system.

8. **Testing and Validation:**
   - Creating test cases to cover the happy path as well as the edge cases and error conditions.
   - Testing the feature across different browsers and devices to ensure compatibility.

9. **Documentation and User Help:**
   - Updating any existing documentation to include the new feature.
   - Providing instructions or a help section for users to understand how to use the new import functionality.

10. **Feedback Mechanism:**
    - Implementing a way for users to report issues or provide feedback on the new feature.

By considering these components and conditions, the development team can ensure a comprehensive approach to implementing the feature, which can then be translated into user stories for development.

**User Stories:**
# Feature: Import Second Supervisor Information

## Scenario: Admin successfully uploads a valid Excel file with second supervisor data
- Given I am logged in as an admin
- And I am on the 'Import Second Supervisor' page
- When I select a valid Excel file with project ID and second supervisor GUID
- And I click the 'Upload' button
- Then the file should be processed without errors
- And I should see a success message 'File uploaded successfully.'
- And the second supervisor should be listed alongside the project and primary supervisor in the admin table

## Scenario: Admin attempts to upload an invalid file type
- Given I am logged in as an admin
- And I am on the 'Import Second Supervisor' page
- When I select a file that is not an Excel file
- And I click the 'Upload' button
- Then I should see an error message 'Invalid file type. Please upload an Excel file.'

## Scenario: Admin attempts to upload an Excel file with incorrect column structure
- Given I am logged in as an admin
- And I am on the 'Import Second Supervisor' page
- When I select an Excel file with incorrect columns
- And I click the 'Upload' button
- Then I should see an error message 'Incorrect Excel format. Please ensure the file has the required columns.'

## Scenario: Admin uploads an Excel file with an invalid Project ID
- Given I am logged in as an admin
- And I am on the 'Import Second Supervisor' page
- When I select an Excel file with an invalid Project ID
- And I click the 'Upload' button
- Then I should see an error message 'Invalid Project ID(s) found. Please correct the data and try again.'

## Scenario: Admin uploads an Excel file with a non-existent second supervisor GUID
- Given I am logged in as an admin
- And I am on the 'Import Second Supervisor' page
- When I select an Excel file with a non-existent second supervisor GUID
- And I click the 'Upload' button
- Then I should see an error message 'Second supervisor GUID not found in the system. Please check the GUID(s) and try again.'

## Scenario: Student views project with primary and second supervisor listed
- Given I am logged in as a student
- And I am on the 'Available Projects' page
- When I look at the list of projects
- Then I should see the second supervisor's name in brackets next to the primary supervisor's name for each project
```

## Contributing

If you'd like to contribute to the project, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Licensing

MIT License.
