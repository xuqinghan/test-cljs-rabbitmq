(ns frontend.app
  (:require
   [frontend.util :refer (console-log to-json parse-json)]
   [stomp]
   [config :refer [para_stomp]]
   [goog.string :refer (format)]
   )
  )




(def ^stomp/Client client-stomp) ;增加类型注解



(defn init []
  (console-log "Hello World")
  (console-log para_stomp)
  (set! client-stomp (new stomp/Client para_stomp))
  (console-log client-stomp)


  (aset client-stomp "onConnect"
    (fn [frame]
      (console-log "stomp connected")

      ; 登录后 订阅队列
      (.subscribe client-stomp "/queue/snapshot"
        (fn [msg]
          (console-log "recv from /queue/snapshot" msg)
          (println (parse-json msg.body))
        ))

          ;发送消息到rabitmq
      (let [body (to-json {:para1 1 :para2 2})
            para {:destination "/exchange/player-request"
                      ;; :headers {:transaction 312}
                  :body body}
            para-js-obj (clj->js para)]
        (.publish client-stomp para-js-obj))
      ))


  ;; 启动客户端
  (.activate client-stomp))
