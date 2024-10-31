#!/bin/bash
# Clear terminal
clear
# Load config file
config_file="src/settings/config.json"
token=$(jq -r '.token' "$config_file")
version=$(jq -r '.version' "$config_file")
main_server_id=$(jq -r '.main_server_id' "$config_file")
sync_server_id=$(jq -r '.sync_server_id' "$config_file")

# Check if all required fields are present
if [ -z "$token" ]; then
    echo "Missing required config field: token"
    exit 1
fi
if [ -z "$version" ]; then
    echo "Missing required config field: version"
    exit 1
fi
if [ -z "$main_server_id" ]; then
    echo "Missing required config field: main_server_id"
    exit 1
fi
if [ -z "$sync_server_id" ]; then
    echo "Missing required config field: sync_server_id"
    exit 1
fi

# Clear terminal
clear

# Start the bot
python3 src/bot.py