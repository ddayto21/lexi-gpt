#!/bin/bash
# llm_client.sh - A CLI client for interacting with the DeepSeek API with real-time SSE parsing,
# aesthetic terminal output, and Markdown rendering via glow.

# Exit code definitions
EXIT_SUCCESS=0
EXIT_FAILURE=1
EXIT_INVALID_INPUT=2
EXIT_API_ERROR=3

# Load environment variables from .env file (if present)
if [ -f .env ]; then
    source .env
fi

# Verify that DEEPSEEK_API_KEY is set
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo -e "\033[31mError: DEEPSEEK_API_KEY environment variable is not set.\033[0m" >&2
    exit $EXIT_FAILURE
fi

# Check for jq dependency
if ! command -v jq >/dev/null 2>&1; then
    echo -e "\033[31mError: jq is not installed. Please install jq to continue.\033[0m" >&2
    exit $EXIT_FAILURE
fi

# Check for glow dependency; warn if not installed
if ! command -v glow >/dev/null 2>&1; then
    echo -e "\033[33mWarning: glow is not installed. Markdown rendering will be disabled.\033[0m" >&2
fi

# Initialize default variables.
MODEL="deepseek-chat"
TEMPERATURE=0.7
ASYNC_MODE=true

# Function: read_multiline_input
# Reads multi-line input from the user until they type "/send" on a new line.
read_multiline_input() {
    echo -e "\033[36mEnter your prompt (type '/send' on a new line when finished):\033[0m"
    local input=""
    while true; do
        echo -ne "\033[33m> \033[0m"
        read -r line
        if [[ "$line" == "/send" ]]; then
            break
        fi
        input+="$line"$'\n'
    done
    if [ -z "$input" ]; then
        echo -e "\033[31mError: Input cannot be empty.\033[0m" >&2
        exit $EXIT_INVALID_INPUT
    fi
    echo -n "$input"
}

# Function: get_token_balance
# Retrieves the token balance from the DeepSeek API using curl.
get_token_balance() {
    local response
    response=$(curl -s --no-buffer --max-time 10 -X GET "https://api.deepseek.com/user/balance" \
         -H "Content-Type: application/json" \
         -H "Authorization: Bearer $DEEPSEEK_API_KEY")
    if [ $? -ne 0 ] || [ -z "$response" ]; then
        echo -e "\033[31mError: Failed to retrieve token balance.\033[0m" >&2
        exit $EXIT_API_ERROR
    fi
    echo "$response"
}

# Function: display_token_balance_menu
# Formats and renders the token balance as a Markdown snippet using glow.
display_token_balance_menu() {
    local token_balance_json
    token_balance_json=$(get_token_balance)
    local markdown_output
    markdown_output=$(cat <<EOF
# Token Balance

\`\`\`json
$token_balance_json
\`\`\`
EOF
)
    if command -v glow >/dev/null 2>&1; then
        echo "$markdown_output" | glow -s dark
    else
        echo "$markdown_output"
    fi
}

# Function: display_task_menu
# Renders the task selection menu as a Markdown snippet using glow.
display_task_menu() {
    local menu_md
    menu_md=$(cat <<EOF
# Select a Task

- **1:** Coding (Temperature: 0.0)
- **2:** Data Cleaning (Temperature: 1.0)
- **3:** Translation (Temperature: 1.3)
- **4:** Creative Writing (Temperature: 1.5)
EOF
)
    if command -v glow >/dev/null 2>&1; then
        echo "$menu_md" | glow -s dark
    else
        echo "$menu_md"
    fi
}

# Function: send_deepseek_prompt
# Sends a prompt to the DeepSeek API and returns the raw streamed response.
send_deepseek_prompt() {
    local prompt="$1"
    local temperature="$2"
    local async_mode="$3"

    # Construct messages JSON using jq.
    local messages
    messages=$(jq -n --arg content "$prompt" '[{"role": "user", "content": $content}]')
    if [ $? -ne 0 ]; then
        echo -e "\033[31mError: Failed to construct JSON payload.\033[0m" >&2
        exit $EXIT_FAILURE
    fi

    if [[ "$async_mode" == "true" ]]; then
        curl -s --no-buffer -X POST "https://api.deepseek.com/v1/chat/completions" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
            -d "{\"model\": \"${MODEL}\", \"messages\": ${messages}, \"temperature\": ${temperature}, \"stream\": true}"
    else
        curl -s --no-buffer -X POST "https://api.deepseek.com/v1/chat/completions" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
            -d "{\"model\": \"${MODEL}\", \"messages\": ${messages}, \"temperature\": ${temperature}, \"stream\": false}"
    fi
}


# Processes the streamed SSE response by parsing each chunk to extract the "content" field,
# and prints each chunk immediately.
process_sse_stream() {
    send_deepseek_prompt "$1" "$TEMPERATURE" "$ASYNC_MODE" |
    while IFS= read -r line; do
        if [[ "$line" =~ ^data:\ (.*)$ ]]; then
            local json_part="${BASH_REMATCH[1]}"
            # Remove carriage returns and newlines.
            json_part=$(echo "$json_part" | tr -d '\r\n')
            # Check if the final marker is detected (either as plain text or JSON object).
            if [[ "$json_part" == "[DONE]" || "$json_part" == '{"done": true}' ]]; then
                break
            fi
            # Use jq to extract the "content" field.
            local content
            content=$(echo "$json_part" | jq -r '.choices[0].delta.content // empty' 2>/dev/null)
            if [ $? -ne 0 ]; then
                echo -e "\033[31mWarning: Failed to parse JSON response: $json_part\033[0m" >&2
                continue
            fi
            if [ -n "$content" ]; then
                # Print each content chunk immediately.
                echo -ne "$content"
            fi
        fi
    done
    echo -e "\n\033[36m--------------\033[0m\n"
}

# Main interactive REPL loop.
main() {
    # Display token balance as a formatted Markdown menu.
    display_token_balance_menu
    echo

    # Display the task selection menu.
    display_task_menu
    echo
    read -r -p $'\033[36mEnter a number (1-4): \033[0m' task_choice
    if ! [[ "$task_choice" =~ ^[1-4]$ ]]; then
        echo -e "\033[31mError: Invalid task choice. Please enter a number between 1 and 4.\033[0m" >&2
        exit $EXIT_INVALID_INPUT
    fi
    case $task_choice in
        1) TEMPERATURE=0.0 ;;
        2) TEMPERATURE=1.0 ;;
        3) TEMPERATURE=1.3 ;;
        4) TEMPERATURE=1.5 ;;
        *) TEMPERATURE=0.7 ;; # Should not reach here.
    esac
    echo -e "\033[32mTemperature set to $TEMPERATURE.\033[0m\n"

    # Interactive REPL loop.
    while true; do
        local user_prompt
        user_prompt=$(read_multiline_input)
        # Exit if the user types "quit" (case-insensitive).
        if [[ "$user_prompt" =~ ^[qQ]uit$ ]]; then
            echo -e "\033[35mExiting interactive session.\033[0m"
            break
        fi
        echo -e "\033[36m--- Answer ---\033[0m"
        process_sse_stream "$user_prompt"
    done
}

main