FROM python:3.8.2-alpine3.11
MAINTAINER NetherKids <git@netherkids.de>

ENV HOST="irc.chat.twitch.tv" \
    PORT="6697" \
    NICK="" \
    PASS="" \
    JOIN=""

RUN addgroup --gid 3820 pythonuser && \
	adduser --uid 3820 --ingroup pythonuser --disabled-password --gecos "" pythonuser

VOLUME /opt/chat
COPY --chown=pythonuser:pythonuser /irc_chat.py /opt
COPY --chown=pythonuser:pythonuser /entrypoint.sh /

RUN chmod 0775 /entrypoint.sh /opt/irc_chat.py && chown pythonuser.pythonuser /entrypoint.sh /opt/irc_chat.py && \
	chmod -R 0777 /opt && chown pythonuser.pythonuser -R /opt/chat

WORKDIR /opt
ENTRYPOINT ["/entrypoint.sh"] 
