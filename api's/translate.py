from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import io
import translate

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) configuration to allow requests from any domain
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

def translate_message(language: str, message: str):
    try:
        translator = translate.Translator(to_lang=language)
        translated_message = translator.translate(message)
        return translated_message

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def voice_assistant(language: str, message: str):
    try:
        tts = gTTS(message, lang=language)
        audio_stream = io.BytesIO()
        tts.save(audio_stream)
        audio_stream.seek(0)
        return audio_stream

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate")
async def translate_endpoint(request: Request):
    data = await request.json()
    language = data.get("language")
    message = data.get("message")

    if not language or not message:
        raise HTTPException(status_code=400, detail="Language and message are required fields.")

    translated_message = translate_message(language, message)
    return {"translated_message": translated_message}

@app.post("/voice_assistant")
async def voice_assistant_endpoint(request: Request):
    data = await request.json()
    language = data.get("language")
    message = data.get("message")

    if not language or not message:
        raise HTTPException(status_code=400, detail="Language and message are required fields.")

    audio_stream = voice_assistant(language, message)
    return Response(content=audio_stream, media_type="audio/mpeg")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
