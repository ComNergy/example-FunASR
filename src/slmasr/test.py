import requests

form_data_url = "http://127.0.0.1:8000/v1/audio/transcriptions"
json_data_url = "http://127.0.0.1:8000/v1/audio/transcriptionsA"
payload = {
    "file": {
        "url": "https://sns-video-hw.xhscdn.com/stream/110/258/01e44d032c7925ce0103700387ccd66a38_258.mp4"
    }
}


# def form_data_test():
#     response = requests.post(form_data_url, files={"file": open("a.mp3", "rb")})
#     print(response.status_code, response.text)


def json_data_test():
    response = requests.post(json_data_url, json=payload)
    print(response.status_code, response.text)


if __name__ == '__main__':
    # form_data_test()
    json_data_test()
