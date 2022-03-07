(ns frontend.util)

(defn console-log [& args]
  (.apply js/console.log js/console (to-array args)))

(defn to-json [data-clj]
  (js/JSON.stringify (clj->js data-clj)))

(defn parse-json [str-json]
  (js->clj (js/JSON.parse str-json)))
