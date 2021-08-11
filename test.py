import requests
p={'zone': '30', 'encounter': '1047', 'metric': 'dps', 'timeframe': 'historical', 'api_key': 'fe7b33659147c216efc93755d78304a4'}
url="https://cn.fflogs.com/v1/rankings/character/西行寺雪菜/宇宙和音/CN"
html=requests.get(url,params=p)
print(html.text)
docker run --name=coolq -d -p 8080:9000 -v /root/coolq:/home/user/coolq -e VNC_PASSWD=813910 -e COOLQ_ACCOUNT=1393937441 coolq/wine-coolq
docker run -d -p 9000:9000 –restart=always -v /var/run/docker.sock:/var/run/docker.sock –name prtainer-test docker.io/portainer/portainer
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=813910 -d mysql:tag
docker run --name LxEgotist'sw -e WORDPRESS_DB_HOST=127.0.0.1:80 -e WORDPRESS_DB_USER=pjxlxt -e WORDPRESS_DB_PASSWORD=813910 -d wordpress
docker run --name=coolq --rm -p 8080:9000 -v /root/coolq-data:/home/user/coolq -e VNC_PASSWD=813910 -e COOLQ_ACCOUNT=1393937441 coolq/wine-coolq
docker run -d -p 8082:8082 --restart=always --name portainer -v /var/run/docker.sock:/var/run/docker.sock -v /root/portainer:/data docker.io/portainer/portainer
docker run -ti --rm --name=cqhttp -v /root/coolq-data:/home/user/coolq -p 9000:9000 -p 5700:5700 -e VNC_PASSWD=813910 -e COOLQ_ACCOUNT=1393937441 -e CQHTTP_POST_URL=http://127.0.0.1:8080/ -e CQHTTP_SERVE_DATA_FILES=yes richardchien/cqhttp:latest
version: "3"
services:

  cqhttp:
    image: richardchien/cqhttp:latest
    volumes:
      - "./coolq-data:/home/user/coolq" # 用于保存COOLQ文件的目录
    environment:
      - COOLQ_ACCOUNT=1393937441 # 指定要登陆的QQ号，用于自动登录
      - FORCE_ENV=true
      - CQHTTP_USE_HTTP=false
      - CQHTTP_USE_WS=false
      - CQHTTP_USE_WS_REVERSE=true
      - CQHTTP_WS_REVERSE_API_URL=ws://nonebot:8080/ws/api/
      - CQHTTP_WS_REVERSE_EVENT_URL=ws://nonebot:8080/ws/event/
    depends_on:
      - nonebot

  nonebot:
    build: ./nonebot
            FROM alpine
        RUN apk add --no-cache tzdata python3 py3-multidict py3-yarl && \
    pip3 install --no-cache-dir "nonebot[scheduler]" # 构建nonebot执行环境，Dockerfile见下面的例子
    expose:
      - "8080"
    environment:
      - TZ=Asia/Shanghai
    volumes:
      - "./LxBot:/root/LxBot" # 项目文件所在目录
    command: python3 /root/LxBot/bot.py