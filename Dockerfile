FROM alpine:3.20

# Install required packages
RUN apk add --no-cache curl git python3 py3-pip wget zip
RUN mkdir /bot
COPY . /bot
WORKDIR /bot

# Install dependencies
RUN pip3 install -r requirements.txt --break-system-packages && rm -r /root/.cache

# Run the bot
CMD ["python3", "main.py"]
