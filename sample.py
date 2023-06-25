import requests
import simpleaudio
import tempfile
import json

HOST = "127.0.0.1"
PORT = 50021

with open('./data/sample.txt') as f:
    for line in f:
        params = (("text", f"{line}"), ("speaker", 22))
        # https://puarts.com/?pid=1830

        response1 = requests.post(
            f"http://{HOST}:{PORT}/audio_query", params=params)
        response2 = requests.post(
            f"http://{HOST}:{PORT}/synthesis",
            headers={"Content-Type": "application/json"},
            params=params,
            data=json.dumps(response1.json()),
        )

        with tempfile.TemporaryDirectory() as tmp:
            with open(f"{tmp}/audi.wav", "wb") as f:
                f.write(response2.content)
                wav_obj = simpleaudio.WaveObject.from_wave_file(
                    f"{tmp}/audi.wav")
                play_obj = wav_obj.play()
                play_obj.wait_done()
