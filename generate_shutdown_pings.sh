#!/bin/sh
# Opens Firefox nightly with a "nightly" profile, which is preconfigured to
# send UT pings to a local gzipServer instance
#
# $1 number of iterations to run
# $2 time to leave each instance open, in seconds
for i in $(seq 1 $1)
do
  echo "Starting instance $i"
  /Applications/FirefoxNightly.app/Contents/MacOS/firefox-bin -P "nightly" &
  pid=$!
  echo "Waiting for telemetry to start for instance $i"
  sleep $2
  echo "Pings should have sent for instance $i"
  kill -9 $pid
  echo "Killing instance $i"
  sleep 10
done
