# FunASR 语音识别项目

这是一个使用 FunASR 进行语音识别的项目。

## 项目简介

本项目利用 FunASR (Fun Automatic Speech Recognition) 框架实现了中文语音识别功能。它提供了一个 HTTP API 服务，可以接收音频文件并返回识别结果。

## 主要特性

- 支持中文语音识别
- 提供 HTTP API 接口
- 使用 Docker 容器化部署
- 支持 GPU 加速

## 在共绩算力使用

<https://www.gongjiyun.com>

Compose 如下

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

## 在本地使用

1. 确保您的系统已安装 Docker 和 Docker Compose。

2. 克隆此仓库：

   ```
   git clone https://github.com/ComNergy/example-ffmpeg.git
   cd example-ffmpeg
   ```

3. 启动服务：

```sh
docker-compose up -d
```

4. 服务将在 `http://localhost:8000` 上运行。

## API 使用

### 音频转写

POST `/v1/audio/transcriptions`

请求体：

- `file`: 音频文件（支持多种格式）
