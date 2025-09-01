## Command List

Here’s a command list to test the main CLI commands, with logic and expected output for each step. These commands use the CLI interface defined in cli.py and interact with the backend and database.

### 1. Create Persons (Created while initializing)
    - Logic:

        Adds new persons (users) to the database.

    - Expected Output:

        Confirmation of person creation with their ID.

    ```bash
    python -m email_assistant person_create --full_name "John Doe" --email_address "john.doe@example.com" --phone_number "+1234567890"

    python -m email_assistant person_create --full_name "Jane Smith" --email_address "jane.smith@example.com" --phone_number "+1234567891"
    ```

### 2. Create Email Session

    - Logic:
        
        Creates a new email session between two persons.

    - Expected Output:

        Returns a session ID.

    ```bash 
    python -m email_assistant session_create --sender_id <john_id> --receiver_id <jane_id> --subject "Project Kickoff"
    ```
### 3. Add Messages to Session (session_chat)

    - Logic:

        Adds messages to the created session, simulating an email conversation.

    - Expected Output:

        Confirmation that the message was added.

    ```bash
    python -m email_assistant session_chat --session_id <session_id> --sender_id <john_id> --receiver_id <jane_id> --message_text "Hi Jane, let's discuss the project kickoff."

    python -m email_assistant session_chat --session_id <session_id> --sender_id <jane_id> --receiver_id <john_id> --message_text "Hi John, sure! When shall we start?"
    ```

### 4. Create AI Session (aisession_create)

    - Logic:

        Creates an AI session for the given email session, enabling AI-powered features.

    - Expected Output:

        Returns an AI session ID.

    ```bash
    python -m email_assistant aisession_create --esession_id <session_id>
    ```

### 5. Chat with Sox (chat_with_sox)

     - Logic:

        Sends a message to the Sox AI agent for the given AI session.

    - Expected Output:

        AI-generated response based on the email conversation and context.

    ```bash
    python -m email_assistant chat_with_sox --aisession_id <aisession_id> --message "Can you summarize the conversation so far?"
    ```

## Summary Table


|Step |	Command Example |  Output |
|-----|-----------------|---------|
|Create Person	| `person_create ...`	| Person ID |
|Create Session	| `session_create ...`	| Session ID |
|Add Message	| `session_chat ...`	| Message added confirmation |
|Create AI Session	| `aisession_create ...`	| AI Session ID |
|Chat with Sox	| `chat_with_sox ...`	| AI response (summary, reply, etc.) |

## Logic Flow:

Persons are created and stored in the database.
An email session is created between two persons.
Messages are added to the session, building the conversation.
An AI session is created for the email session, enabling AI features.
Sox AI agent can now answer questions or summarize the conversation.
For more details, see the CLI logic in cli.py and backend API in aisession_routes.py.