(ns backend-clojure.core
  (:gen-class)
  (:import (java.util Collections))
  (:import (com.rabbitmq.client ConnectionFactory Channel DeliverCallback CancelCallback)))

(def factory (new ConnectionFactory))
(def conn false)
(def ^:dynamic ^Channel *ch*)


(defn fn_callback_msg [consumerTag, message]
  (println (new String (.getBody message)))
  ;; (.basicAck *ch* (.. message getEnvelope getDeliveryTag) false)
  )

(defn make-fn_callback_msg []
  ;"impl DeliverCallback.handle https://rabbitmq.github.io/rabbitmq-java-client/api/current/com/rabbitmq/client/DeliverCallback.html"
  (reify DeliverCallback
    (handle [this consumerTag message]
      ; here the impl 
      (fn_callback_msg consumerTag message))))


(defn fn_consumerOK [consumerTag]
  (println "fn_consumerOK"))

(defn make-fn_consumerOK []
  (reify CancelCallback
    (handle [this consumerTag]
       ; here the impl 
      (fn_consumerOK consumerTag))))





(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println "Hello, World!")
  (let [conn (.newConnection factory)]
    (binding [*ch* (.createChannel conn)]

      (.basicQos *ch* 100)
      (.basicConsume *ch*
                     "mystream_pika"
                     false
                     (Collections/singletonMap "x-stream-offset" "first")
                     (make-fn_callback_msg)
                     (make-fn_consumerOK))))
  ;keep not exit
  ;; (println "wait 1sec")
  ;; (while true
  ;;   (Thread/sleep 1)
  ;;   (println "wait 1sec")
  ;;   (flush))

  (println "exit"))


