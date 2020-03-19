#!/bin/sh
chown dotnetuser.dotnetuser -R /opt
su pythonuser -c "python3 /opt/irc_chat.py ${HOST} ${PORT} ${NICK} ${PASS} ${JOIN}"
