#!/bin/bash

REMOTE_USER_HOST="jose@10.147.17.146"

PHP_FILE_PATH="/home//Capstone-Group-03//.php"

# Opens gnome-terminal on the remote machine
ssh -X "$REMOTE_USER_HOST" "gnome-terminal -- bash -c 'php \"$PHP_FILE_PATH\"; exec bash'"
