#!/bin/bash

sudo snap start redis

PORT=${PORT:-8080}

# Запуск ngrok у фоні і збереження PID
nohup ngrok http $PORT > ngrok.log 2>&1 &
echo $! > ngrok.pid

# Чекаємо, поки тунель з’явиться
while ! curl -s http://localhost:4040/api/tunnels | grep -q '"public_url":'; do
    sleep 1
done

# Отримуємо URL тунелю
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

# Оновлюємо або додаємо SERVER_ADDRESS у .env
if grep -q '^SERVER_ADDRESS=' .env 2>/dev/null; then
    sed -i "s|^SERVER_ADDRESS=.*|SERVER_ADDRESS=$NGROK_URL|" .env
else
    echo "SERVER_ADDRESS=$NGROK_URL" >> .env
fi

echo "Ngrok запущений: $NGROK_URL"
