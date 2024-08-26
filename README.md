# funasr

共绩算力 funasr 例子

## Compose 如下

```yml
services:
  slmasr:
    image: harbor.suanleme.cn/admin/slmasr
    build:
      context: .
    ports:
      - 8000:8000
    volumes:
      - ./modelscope:/root/.cache/modelscope
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [ gpu ]
```
