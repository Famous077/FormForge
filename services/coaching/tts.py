from io import BytesIO
from gtts import gTTS

class TextToSpeech:
    def speak(self, text, lang="en"):
        cleaned = (text or "").strip()

        if not cleaned:
            return
        
        buffer = BytesIO()
        try:
            gTTS(text=cleaned, lang=lang).write_to_fp(buffer)
        except Exception:
            return

        buffer.seek(0)

        return buffer.read()
      