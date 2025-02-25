#!/bin/bash
HOST='ftp_server_address'
USER='ftp_username'
PASS='ftp_password'
LOCAL_DIR='/home/pi/edl_files'
REMOTE_DIR='/path/on/ftp/server'

lftp -f "
open $HOST
user $USER $PASS
lcd $LOCAL_DIR
mirror --reverse --verbose . $REMOTE_DIR
bye
"
