#!/bin/sh
su dotnetuser -c "python3 /opt/irc_chat.py ${HOST} ${PORT} ${NICK} ${PASS} ${JOIN}"
