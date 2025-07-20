import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound # Đảm bảo bạn đã cài đặt: pip install playsound

def translate_speech_continuous():
    r = sr.Recognizer()
    translator = Translator()

    print("🎤 Bắt đầu phiên dịch liên tục. Hãy nói tiếng Việt. (Nói 'dừng lại' để kết thúc)")
    print("----------------------------------------------------------------------")

    while True:
        with sr.Microphone() as source:
            print("\n🎧 Đang lắng nghe... (Listening...)")
            r.adjust_for_ambient_noise(source, duration=0.5) # Điều chỉnh tiếng ồn xung quanh
            try:
                audio = r.listen(source, timeout=1)
            except sr.WaitTimeoutError:
                print("⏳ Không nghe thấy gì. Đang đợi lần nói tiếp theo. (No speech detected. Waiting for next input.)")
                continue # Bỏ qua lần này và tiếp tục vòng lặp

        try:
            # Nhận diện giọng nói tiếng Việt
            text_vi = r.recognize_google(audio, language="vi-VN")
            print(f"📝 Bạn đã nói (You said): {text_vi}")

            # Kiểm tra lệnh dừng
            if "dừng lại" in text_vi.lower() or "dừng" in text_vi.lower() or "stop" in text_vi.lower():
                print("👋 Lệnh 'dừng lại' được phát hiện. Kết thúc chương trình. (Stop command detected. Exiting program.)")
                break # Thoát khỏi vòng lặp

            # Dịch tiếng Việt sang tiếng Anh
            text_en = translator.translate(text_vi, src='vi', dest='es').text
            print(f"🌐 Dịch sang tiếng Anh (Translated to english): {text_en}")

            # Chuyển văn bản tiếng Anh thành giọng nói
            tts = gTTS(text_en, lang='es')
            audio_file_path = "output.mp3"
            tts.save(audio_file_path)
            print("🔊 Đang phát bản dịch (Playing translation)...")

            # Phát file âm thanh
            playsound(audio_file_path)

            # Dọn dẹp: xóa file âm thanh tạm thời
            os.remove(audio_file_path)
            print("✅ Hoàn tất lượt dịch. (Translation turn completed.)")

        except sr.UnknownValueError:
            print("❌ Xin lỗi, không nhận diện được giọng nói của bạn. Vui lòng nói rõ hơn. (Sorry, I could not understand your speech. Please speak more clearly.)")
        except sr.RequestError as e:
            print(f"❌ Không thể kết nối với dịch vụ Google Speech Recognition; vui lòng kiểm tra kết nối mạng của bạn: {e} (Could not request results from Google Speech Recognition service; please check your network connection).")
        except Exception as e:
            print(f"❌ Đã xảy ra lỗi không mong muốn: {e} (An unexpected error occurred).")

    print("\nChương trình đã kết thúc.")

if __name__ == '__main__':
    # pip install speechrecognition googletrans gtts playsound
    translate_speech_continuous()