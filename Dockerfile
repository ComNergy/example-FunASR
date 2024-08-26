FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-devel

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

RUN mkdir "/app"
WORKDIR /app

# install dependencies
COPY ./requirements.lock /app/
RUN sed '/^-e/d;s/torch==2.3.1+cu121/torch==2.3.1/g' requirements.lock > requirements.txt
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt

# install slmasr
COPY dist/slmasr-0.1.0-py3-none-any.whl /app
RUN pip install slmasr-0.1.0-py3-none-any.whl

# save models in image to avoid redownload error
ADD ./modelscope /root/.cache/modelscope

# expose port
EXPOSE 8000
HEALTHCHECK --interval=5m --timeout=3s --start-period=2m --retries=5 CMD curl -f http://127.0.0.1:8000/ || exit 1

CMD uvicorn slmasr:app --host 0.0.0.0