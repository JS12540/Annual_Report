from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
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

@app.post("/translate")
async def translate(request: Request):
    data = await request.json()
    language = data.get("language")
    message = data.get("message")
    
    if not language or not message:
        raise HTTPException(status_code=400, detail="Language and message are required fields.")
    
    translated_message = translate_message(language, message)
    return {"translated_message": translated_message}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
