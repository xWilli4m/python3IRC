FROM python:3.8.2-alpine3.11
MAINTAINER NetherKids <git@netherkids.de>

ENV HOST="irc.chat.twitch.tv" \
    PORT="6697" \
    NICK="" \
    PASS="" \
    JOIN=""

RUN addgroup --gid 3820 pythonuser && \
	adduser --uid 3820 --ingroup pythonuser --disabled-password --gecos "" pythonuser

VOLUME /opt
COPY --chown=pythonuser:pythonuser /irc.py /

RUN chmod 0775 /irc.py && chown pythonuser.pythonuser /irc.py && \
	chmod -R 0777 /opt && chown pythonuser.pythonuser -R /opt

WORKDIR /opt
ENTRYPOINT ["python3 /irc.py ${HOST} ${PORT} ${NICK} ${PASS} ${JOIN}"] 
