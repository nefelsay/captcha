import pydub
import speech_recognition as sr

def audio_to_text(name_audio_file):
    with open(f'{name_audio_file}', 'rb') as files:

        # Указываем пусть к файлу
        path_to_mp3 = name_audio_file

        # Указываем имя нового файла в формате wav
        path_to_wav = 'audio_file_wav.wav'

        # Создаем объект аудио с данными из mp3 файла который будет использован для дальнейшей обработки
        sound = pydub.AudioSegment.from_file(path_to_mp3, 'mp3')

        #Экспортируем аудио данные объекта в новый файл
        sound.export(path_to_wav, format="wav")

        #Cоздаем экземпляр класса AudioFile из библиотеки SpeechRecognition(sr)
        #Этот объект используется далее как источник данных для распознавания речи
        sample_audio = sr.AudioFile(path_to_wav)

        #Создаём экземпляр класса для дальнейшего распознавания речи с использованием Google Speech Recognition API.
        r = sr.Recognizer()
        with sample_audio as source:
            #Записанный аудио будет использован для распознавания речи
            audio = r.record(source)
            key = r.recognize_google(audio, show_all=True)
            # transcription = key['alternative'][0]['transcript']
            # print(key['alternative'][0]['transcript'])
            #Возвращаем первый элемераспознанный тект
            return key['alternative'][0]['transcript']

print(audio_to_text("payload.mp3"))
