(ns frontend.util)

(defn console-log [& args]
  (.apply js/console.log js/console (to-array args)))