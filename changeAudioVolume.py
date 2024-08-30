from pydub import AudioSegment
from pydub.playback import play

song = AudioSegment.from_mp3("louder.mp3")

print(song.dBFS)
# for attr in dir(song):
#     if not attr.startswith("_"):
#         print(getattr(song, attr))

# boost volume by 3dB
louder_song = song + 17.3

# reduce volume by 3dB
quieter_song = song - 3

# louder_song.export("louder.mp3", format="mp3")
# quieter_song.export("quieter.mp3", format="mp3")
