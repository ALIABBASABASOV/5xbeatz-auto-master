from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import matchering as mg
from pedalboard import Pedalboard, Compressor, Limiter, Gain, HighpassFilter, LowpassFilter
import soundfile as sf
import os
import shutil

app = FastAPI()
templates = Jinja2Templates(directory="templates")

REFERENCE = {
    "trap": "references/ref_trap.wav",
    "drill": "references/ref_drill.wav",
    "phonk": "references/ref_phonk.wav",
    "hiphop": "references/ref_hiphop.wav",
    "lofi": "references/ref_lofi.wav",
    "pop": "references/ref_pop.wav",
    "edm": "references/ref_edm.wav",
    "techno": "references/ref_techno.wav",
    "house": "references/ref_house.wav",
    "reggaeton": "references/ref_reggaeton.wav",
    "rnb": "references/ref_rnb.wav",
    "ukgrime": "references/ref_ukgrime.wav",
    "cloudrap": "references/ref_cloudrap.wav",
    "memphis": "references/ref_memphis.wav",
    "jazzhop": "references/ref_jazzhop.wav"
}

os.makedirs("temp", exist_ok=True)
os.makedirs("mastered", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/master")
async def master(file: UploadFile = File(...), genre: str = Form("trap")):
    target_path = f"temp/{file.filename}"
    with open(target_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    ref_path = REFERENCE.get(genre.lower(), REFERENCE["trap"])

    temp_result = "temp_result.wav"
    mg.process(target=target_path, reference=ref_path, results=[mg.pcm24(temp_result)])

    board = Pedalboard([])

    g = genre.lower()

    # 20 Hz aşağı + 20 kHz yuxarı kəsmə (hər janrda eyni)
    board.append(HighpassFilter(cutoff_frequency_hz=20))
    board.append(LowpassFilter(cutoff_frequency_hz=20000))

    # ÇOX YÜNGÜL compressor (threshold yüksək, ratio aşağı – demək olar ki, heç basmır)
    if g == "trap":
        board.append(Compressor(threshold_db=-3.0, ratio=1.2, attack_ms=15, release_ms=200))
        board.append(Limiter(threshold_db=-0.5))
        board.append(Gain(gain_db=2.2))

    elif g == "drill":
        board.append(Compressor(threshold_db=-2.5, ratio=1.3, attack_ms=12, release_ms=180))
        board.append(Limiter(threshold_db=-0.6))
        board.append(Gain(gain_db=2.0))

    elif g == "phonk":
        board.append(Compressor(threshold_db=-4.0, ratio=1.1, attack_ms=20, release_ms=220))
        board.append(Limiter(threshold_db=-0.8))
        board.append(Gain(gain_db=1.8))

    elif g == "hiphop":
        board.append(Compressor(threshold_db=-3.5, ratio=1.2, attack_ms=18, release_ms=200))
        board.append(Limiter(threshold_db=-0.5))
        board.append(Gain(gain_db=2.0))

    elif g == "lofi":
        board.append(Compressor(threshold_db=-5.0, ratio=1.1, attack_ms=25, release_ms=250))
        board.append(Limiter(threshold_db=-1.0))
        board.append(Gain(gain_db=1.5))

    elif g == "pop":
        board.append(Compressor(threshold_db=-2.0, ratio=1.3, attack_ms=10, release_ms=140))
        board.append(Limiter(threshold_db=-0.4))
        board.append(Gain(gain_db=2.3))

    elif g == "edm":
        board.append(Compressor(threshold_db=-1.5, ratio=1.4, attack_ms=8, release_ms=120))
        board.append(Limiter(threshold_db=-0.3))
        board.append(Gain(gain_db=2.5))

    elif g == "techno":
        board.append(Compressor(threshold_db=-2.0, ratio=1.3, attack_ms=7, release_ms=110))
        board.append(Limiter(threshold_db=-0.4))
        board.append(Gain(gain_db=2.1))

    elif g == "house":
        board.append(Compressor(threshold_db=-2.5, ratio=1.2, attack_ms=9, release_ms=130))
        board.append(Limiter(threshold_db=-0.5))
        board.append(Gain(gain_db=2.0))

    elif g == "reggaeton":
        board.append(Compressor(threshold_db=-3.0, ratio=1.3, attack_ms=11, release_ms=150))
        board.append(Limiter(threshold_db=-0.6))
        board.append(Gain(gain_db=2.0))

    elif g == "rnb":
        board.append(Compressor(threshold_db=-4.0, ratio=1.2, attack_ms=16, release_ms=190))
        board.append(Limiter(threshold_db=-0.8))
        board.append(Gain(gain_db=1.7))

    elif g == "ukgrime":
        board.append(Compressor(threshold_db=-2.5, ratio=1.3, attack_ms=8, release_ms=120))
        board.append(Limiter(threshold_db=-0.5))
        board.append(Gain(gain_db=2.1))

    elif g == "cloudrap":
        board.append(Compressor(threshold_db=-5.0, ratio=1.1, attack_ms=25, release_ms=240))
        board.append(Limiter(threshold_db=-1.0))
        board.append(Gain(gain_db=1.6))

    elif g == "memphis":
        board.append(Compressor(threshold_db=-4.5, ratio=1.2, attack_ms=20, release_ms=210))
        board.append(Limiter(threshold_db=-0.9))
        board.append(Gain(gain_db=1.8))

    elif g == "jazzhop":
        board.append(Compressor(threshold_db=-4.5, ratio=1.2, attack_ms=18, release_ms=200))
        board.append(Limiter(threshold_db=-0.9))
        board.append(Gain(gain_db=1.7))

    else:  # default
        board.append(Compressor(threshold_db=-3.5, ratio=1.2, attack_ms=15, release_ms=180))
        board.append(Limiter(threshold_db=-0.7))
        board.append(Gain(gain_db=2.0))

    audio, sr = sf.read(temp_result)
    effected = board(audio.T, sr)
    final_path = f"mastered/{file.filename}_mastered.wav"

    # 32-bit float WAV (ən yüksək keyfiyyət)
    sf.write(final_path, effected.T, sr, subtype='FLOAT')

    for p in [target_path, temp_result]:
        if os.path.exists(p):
            os.remove(p)

    return FileResponse(final_path, media_type="audio/wav", filename=f"{file.filename}_mastered.wav")