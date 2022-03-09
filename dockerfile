FROM rabbitmq:3-management
LABEL author="xuqinghan"
LABEL purpose = 'stomp for browser cljs'

RUN rabbitmq-plugins enable rabbitmq_web_stomp rabbitmq_stream
#COPY ./rabbitmq.conf /etc/rabbitmq/rabbitmq.conf
