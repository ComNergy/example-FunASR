import json
import mimetypes
import subprocess
import tempfile
import time

import aiohttp
from funasr import AutoModel
from pydantic import BaseModel

import ffmpeg

from slmasr import mimedb

# ffmpeg init
ffmpeg.init()
ffmpeg.add_to_path()

# funasr and modelscope init
pf_model = AutoModel(model="paraformer-zh", vad_model="fsmn-vad", punc_model="ct-punc")


def get_extension(content_type: str) -> str:
    file_extension = mimetypes.guess_extension(content_type)

    if file_extension is None:
        file_extension = mimedb.MIME_INFO.get(content_type)

    if file_extension is None:
        raise ValueError(f"Unsupported content type: {content_type}")

    return file_extension


async def download_file(request_params) -> str:
    chunk_size = 100 * 1024  # 100 KB
    last_print_time = 0
    async with aiohttp.ClientSession() as session:
        async with session.get(**request_params) as response:
            # get content type
            content_type = response.headers.get("Content-Type")

            # get file extension
            file_extension = get_extension(content_type)

            total_size = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)
            with open(temp_file.name, "wb") as f:
                while True:
                    chunk = await response.content.read(chunk_size)
                    downloaded += len(chunk)
                    if not chunk:
                        print(f"Downloaded {downloaded}/{total_size} bytes")
                        print("No more chunks, break")
                        print(f"Total time cost: {time.time() - last_print_time} seconds")
                        break
                    f.write(chunk)

                    if time.time() - last_print_time > 1000:
                        print(f"Downloaded {downloaded}/{total_size} bytes")
                        last_print_time = time.time()

            return temp_file.name


class TranscriptionRequest(BaseModel):
    file: dict


def get_durations(file):
    result = subprocess.check_output([
        'ffprobe', '-i', file,
        '-v', 'quiet', '-print_format', 'json', '-show_format',
    ])

    data = json.loads(result)
    duration = data['format']['duration']
    duration = float(duration)
    return duration


def do_transcription(file: str):
    start = time.time()
    result = pf_model.generate(
        input=file,
        batch_size_s=300,
    )
    result = {"result": result}
    time_cost = time.time() - start
    durations = get_durations(file)
    result['duration'] = durations
    result['statistic'] = {
        "computation_time": time_cost
    }
    return result
