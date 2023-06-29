#!/bin/bash

APP_NAME=sllm:app

start() {
  echo "Starting $APP_NAME"
  nohup uvicorn $APP_NAME --host=0.0.0.0 --port=9002 --limit-concurrency=200 > classificaitonserver.log 2>&1 &
  echo "$APP_NAME started"
}

stop() {
  echo "Stopping $APP_NAME"
  for i in {1..10}; do
      pid=`ps -ef | grep "$APP_NAME" | grep -v grep | awk '{print $2}' | head -n 1`
      if [ "x$pid" == "x" ]; then
          echo "$APP_NAME process stopped."
          break
      else
          kill $pid
          echo "kill $pid $APP_NAME process."
          sleep 1
      fi
  done
  echo "Unable to stop $APP_NAME within 10 seconds, sending SIGKILL"  
}

status() {
  pid=`ps -ef | grep "$APP_NAME" | grep -v grep | awk '{print $2}' | head -n 1`
  if [ "x$pid" == "x" ]; then
      echo "$APP_NAME process is stop."
  else
      echo "$APP_NAME process [pid:$pid] is Running"
  fi
}


case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  status)
    status
    ;;
  *)
    echo "Usage: $0 {start|stop|status}"
    exit 1
esac
