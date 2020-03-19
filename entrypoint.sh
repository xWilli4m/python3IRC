#!/bin/sh
chown pythonuser.pythonuser -R /opt /opt/chat && chmod 0775 -R /opt/chat
su pythonuser -c "python3 /opt/irc_chat.py ${HOST} ${PORT} ${NICK} ${PASS} ${JOIN}"
