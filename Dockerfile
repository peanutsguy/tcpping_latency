FROM alpine:latest

WORKDIR /app

RUN apk add --no-cache python3 traceroute
ADD --chmod=+x https://raw.githubusercontent.com/deajan/tcpping/refs/heads/master/tcpping tcpping
ADD script.py .

ENTRYPOINT [ "python3", "script.py" ]