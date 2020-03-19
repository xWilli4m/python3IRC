FROM python:3.8.2-alpine3.11
MAINTAINER NetherKids <git@netherkids.de>

ENV HOST="irc.chat.twitch.tv" \
    PORT="6697" \
    NICK="" \
    PASS="" \
    JOIN=""

RUN addgroup --gid 3820 python3alpine && \
	adduser --uid 3820 --ingroup python3alpine --disabled-password --disabled-login --gecos "" python3alpine

VOLUME /home/python3alpine/_chats
COPY --chown=python3alpine:python3alpine /irc.py /home/python3alpine/

RUN chmod 0775 /home/python3alpine/irc.py && chown python3alpine.python3alpine /home/python3alpine/irc.py && \
	chmod -R 0777 /home/python3alpine/_chats && chown python3alpine.python3alpine -R /home/python3alpine/_chats

WORKDIR /opt
ENTRYPOINT ["python3 /home/python3alpine/irc.py ${HOST} ${PORT} ${NICK} ${PASS} ${JOIN}"] 
