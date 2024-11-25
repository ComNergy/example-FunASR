import os
import shutil
import tempfile

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .helper import TranscriptionRequest, do_transcription, download_file

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://gongjiyun.com", "https://www.gongjiyun.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": 200}


@app.post("/v1/audio/transcriptions")
async def transcriptions(file: UploadFile = File()):
    # 获取文件名和扩展名
    file_name = file.filename
    _, file_extension = os.path.splitext(file_name)

    # 创建一个临时文件，保持相同的扩展名
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)

    try:
        # noinspection PyTypeChecker
        shutil.copyfileobj(file.file, temp_file)
        temp_file.close()  # 关闭文件以确保所有数据都被写入
        trans_result = do_transcription(temp_file.name)
        os.remove(temp_file.name)
        return trans_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/audio/transcriptionsA")
async def transcriptions_advanced(
        request: TranscriptionRequest,
):
    data = request.dict()
    try:
        temp_file = await download_file(data['file'])
        data['file'] = temp_file
        trans_result = do_transcription(**data)
        os.remove(temp_file)
        return trans_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
