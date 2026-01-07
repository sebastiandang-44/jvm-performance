# Record CPU usage of all java processes every second
while true; do
  date +"%H:%M:%S" >> cpu_log.csv
  ps -p <executor_pid> -o %cpu >> cpu_log.csv
  sleep 1
done
