FROM rabbitmq:3-management
LABEL author="xuqinghan"
LABEL purpose = 'stomp for browser js/cljs'

RUN rabbitmq-plugins enable rabbitmq_stream_management rabbitmq_web_stomp 
COPY ./rabbitmq.conf /etc/rabbitmq/rabbitmq.conf
