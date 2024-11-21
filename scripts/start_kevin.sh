#!/bin/bash

REMOTE_USER_HOST="kevinburgos@10.147.17.200"

PHP_FILE_PATH="/home/kevinburgos/Capstone-Group-03/backend2/register2.php"

# Open gnome-terminal on the remote machine
ssh -X "$REMOTE_USER_HOST" "gnome-terminal -- bash -c 'php \"$PHP_FILE_PATH\"; exec bash'"
