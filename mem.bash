#!/bin/bash

# ======== ARRAYS ========
#   arr[i]=<val>
#   ${arr[i]}
#   ${arr[*]} # Все записи в массиве
#   ${!arr[*]}# Все индексы в массиве
#   ${#arr[*]}# Количество записей в массиве
#   ${#arr[0]}# Длина первой записи (нумерация с нуля)

function append_n() {
    local k=0
    local len=${#arr[*]}
    while [[ k -lt $1 ]]; do
        k=$((k + 1))
        arr[$((len + k))]=k
    done
}

OUTPUT_PATH="report.log"
N=10
LOG_EVERY=100000

echo "" > $OUTPUT_PATH

cnt=0
arr=()
while true; do
    if [[ cnt -eq LOG_EVERY ]]; then
        echo ${#arr[*]} >> $OUTPUT_PATH
        cnt=0
    else 
        cnt=$((cnt + 1))
        append_n $N
    fi
done
