from setuptools import setup, find_packages

setup(
    name="slmasr",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.9.5",
        "fastapi>=0.111.0",
        "ffmpeg-binaries>=1.0.0",
        "funasr>=1.0.25",
        "modelscope>=1.14.0",
        "pydantic>=2.7.1",
        "python-multipart>=0.0.9",
        "uvicorn>=0.29.0",
    ],
    extras_require={
        "dev": [
            "pytest",
            "requests",
        ],
    },
    python_requires=">=3.7",
    author="YooLeon",
    author_email="qyleon4264@gmail.com",
    description="A FastAPI-based ASR service using FunASR",
    url="https://github.com/ComNergy/example-FunASR",
) 