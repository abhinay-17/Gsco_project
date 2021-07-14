#standard import
import os, sys
import ffmpeg
import librosa
from moviepy.editor import *
import moviepy.editor as mp

#split silence thing
from pydub import AudioSegment
from pydub.silence import split_on_silence

#translation (google at back)
from deep_translator import GoogleTranslator 

#tts from text-to-speech
from text_to_speech import speak
from gtts import gTTS

asr_model = "/home/sooos/bothhand/project/translate/pretrained_models/asr_deepspeech/deepspeech-0.9.3-models.pbmm"
asr_scorer = "/home/sooos/bothhand/project/translate/pretrained_models/asr_deepspeech/deepspeech-0.9.3-models.scorer"

pid = os.getpid()
temp_folder = "temp_"+ str(pid) + "/"
os.system("mkdir -p "+temp_folder)


def change_format(infile, outfile):
	'''
	provide filenames with extensions
	'''
	stream = ffmpeg.input(infile)
	stream = ffmpeg.output(stream, outfile)
	ffmpeg.run(stream)

def change_audio_speed(file1, file2, outfile):

	duration_in = librosa.get_duration(filename=file1)
	duration_out = librosa.get_duration(filename=file2)

	print("duration_in:", duration_in)
	print("duration_out:", duration_out)
	ratio = duration_out/duration_in

	if ratio < 0.5:
		ratio = 0.5

	ratio = str(ratio)

#	print("ratio", ratio)

	os.system('ffmpeg -i '+file2+' -filter:a "atempo='+ratio+'" -vn '+outfile)


class Bridge(object):

	def __init__(self):
		self.asr = "deepspeech"
		self.mt = "deeptranslate"
		self.tts = "google"
		
	def asr_deepspeech(self,model, scorer, audio):
		os.system("deepspeech --model "+model+" --scorer "+scorer+" --audio "+audio+" > a.txt")
		text = open("a.txt",'r').read()
		return text

	def txt_to_sp(self, out_file, text, lang):
		tts = gTTS(text=text, lang=lang)
		tts.save(out_file)

#		speak(text, lang=langs, save=True, play=False, file=out_file)

	def translate(self, source, slang='en', tlang='es'):
		'''
		source: input string
		source_lang: en
		target_lang: fr
		'''
		target = GoogleTranslator(source=slang, target=tlang).translate(source)
		return target

	def create_final_audio(self, original, created, final):

		change_audio_speed(original, created, final)

	def create_final_video(self, original_video, audio, final):

		vclip = VideoFileClip(original_video)

		vdur = vclip.duration

		aclip = AudioFileClip(audio)

		adur = aclip.duration

		if vdur >= adur:
			vsub = vclip.subclip(0,adur)
			videoclip1 = vsub.set_audio(aclip)
			videoclip2 = vclip.subclip((vdur-adur), vdur).without_audio()
			videoclip = mp.concatenate_videoclips([videoclip1, videoclip2], method="compose")

		else:
			asub = aclip.subclip(0,vdur)
			videoclip = vclip.set_audio(asub)


		print("video clip duration", videoclip.duration)
		videoclip = vclip.set_audio(aclip)

		videoclip.write_videofile(final)

'''
# segment audio based on silence and run the bridge+merge
class Bridge_with_silences(object):

	def __init(self):

		self.br = Bridge()

	def split_chunks(self, temp_folder):

		chunks = split_on_silence(audio, min_silence_len=3000, silence_thresh=-16)
		
		chunk.export(temp_folder+"/chunk{0}.wav".format(i), format="wav")
'''

if __name__ == '__main__':

	INPUT_LANG = 'en'
	br = Bridge()


	video_input = sys.argv[1]
	OUTPUT_LANG = sys.argv[2]


	audio_input = os.path.basename(video_input).split(".")[0] + ".wav"
	audio_input = temp_folder+audio_input
	change_format(video_input, audio_input)

	#inpvideo = sys.argv[1]

	#extracted_audio = 


	text_from_speech = br.asr_deepspeech(model=asr_model, scorer=asr_scorer, audio=audio_input)
	print("Transrciption: ")
	print(text_from_speech)

	text_translated = br.translate(text_from_speech, INPUT_LANG, OUTPUT_LANG)
	p = str(text_translated)
	print("Translated Transcription: ")
	print(p)

	audio_output = temp_folder+"audio_temp.mp3"
	br.txt_to_sp(out_file=audio_output, text=p,lang=OUTPUT_LANG)

	final_audio = temp_folder+"final.mp3"
	br.create_final_audio(original=audio_input, created=audio_output, final=final_audio)


	final = temp_folder+"final.mp4"
	br.create_final_video(original_video=video_input, audio=final_audio, final=final)

