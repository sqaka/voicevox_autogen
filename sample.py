import requests, simpleaudio, tempfile, json

host = "127.0.0.1"
port = 50021

params = (("text", "こんにちは、ずんだもんです。"), ("speaker", 3))
# https://github.com/VOICEVOX/voicevox_resource/search?q=styleId

response1 = requests.post(f"http://{host}:{port}/audio_query", params=params)

response2 = requests.post(
    f"http://{host}:{port}/synthesis",
    headers={"Content-Type": "application/json"},
    params=params,
    data=json.dumps(response1.json()),
)

with tempfile.TemporaryDirectory() as tmp:
    with open(f"{tmp}/audi.wav", "wb") as f:
        f.write(response2.content)
        wav_obj = simpleaudio.WaveObject.from_wave_file(f"{tmp}/audi.wav")
        play_obj = wav_obj.play()
        play_obj.wait_done()
