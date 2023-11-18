import speech_recognition as sr
import pygame
import youtube_dl

def play_music(song_query):
    # Search for the song on YouTube
    with youtube_dl.YoutubeDL({}) as ydl:
        info_dict = ydl.extract_info(song_query, download=False)
        url = info_dict['formats'][0]['url']

    pygame.mixer.init()
    pygame.mixer.music.load(url)
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def main():
    recognizer = sr.Recognizer()
    music_playing = False

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)

            recognized_text = recognizer.recognize_google(audio).lower()

            print("You said:", recognized_text)

            if "music" in recognized_text and not music_playing:
                print("What song do you want to play?")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                song_query = recognizer.recognize_google(audio).lower()
                print("Searching for:", song_query)
                play_music(song_query)
                music_playing = True
            elif "stop" in recognized_text and music_playing:
                print("Stopping music...")
                stop_music()
                music_playing = False
            elif "next" in recognized_text and music_playing:
                print("Stopping current song...")
                stop_music()
                print("What song do you want to play next?")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                song_query = recognizer.recognize_google(audio).lower()
                print("Searching for:", song_query)
                play_music(song_query)

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print("Error occurred; {0}".format(e))
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
