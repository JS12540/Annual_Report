from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from translate import Translator
from gtts import gTTS
import io
from fastapi.responses import StreamingResponse

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) configuration to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def voice_assistant(language: str, message: str):
    try:
        tts = gTTS(message, lang=language)
        audio_stream = io.BytesIO()
        tts.save(audio_stream)
        audio_stream.seek(0)
        return audio_stream

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Translation endpoint
@app.post("/translate")
async def translate_text(message: str, target_language: str):
    try:
        translator = Translator(to_lang=target_language)
        translated_text = translator.translate(message)
        return {"translation": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")

@app.post("/voice_assistant")
async def voice_assist(message: str, target_language: str):
    audio_stream = voice_assistant(target_language, message)
    return StreamingResponse(io.BytesIO(audio_stream.read()), media_type="audio/mpeg")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
