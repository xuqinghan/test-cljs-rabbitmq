(ns frontend.app
  (:require
   [frontend.util :refer (console-log)]
   [stomp]
   )
  )

(def client-stomp (new stomp/Client {"brokerURL" "ws://127.0.0.1:15674/ws"
                                     "connectHeaders" {"login" "guest"
                                                      "passcode" "guest"}
                                     "reconnectDelay" 5000
                                     "heartbeatIncoming" 4000
                                     "heartbeatOutgoing" 4000}))




(defn init []
  (console-log "Hello World")
  (aset client-stomp "onConnect" (fn [frame] (console-log "stomp connected")))
  (console-log client-stomp)
  (console-log client-stomp)
  (.activate client-stomp [])
  )