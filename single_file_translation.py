import os, sys
import ffmpeg

from deep_translator import GoogleTranslator
from text_to_speech import speak

class sp2sp_core():

	"""
		params:
	"""
	def __init__(self):
		# SP 2 T (ASR) -> T 2 T (Machine Translate) -> T 2 SP (TTS)
		self.asr 	= "deepspeech"
		self.mt 	= "deeptranslate"
		self.tts 	= "google"

	"""
		params:
	"""
	def asr_deepspeech(self, model, scorer, audio):
		os.system("deepspeech --model " + model + " --scorer " + scorer + " --audio " + audio + " > a.txt")
		text = open("a.txt", 'r').read()
		os.system("rm a.txt")
		return text

	"""
		params:
	"""
	def txt_to_sp(self, out_file, text, lang):
		tts = gTTS(text=text, lang=lang)
		tts.save(out_file)

	"""
		params:
	"""
	def translate(self, source, slang='en', tlang='fr'):
		'''
		source: input string
		source_lang: en
		target_lang: fr
		'''
		target = GoogleTranslator(source=slang, target=tlang).translate(source)
		return target


if __name__ == '__main__':

	asr_model = "./asr_deepspeech/deepspeech-0.9.3-models.pbmm"
	asr_scorer = "./asr_deepspeech/deepspeech-0.9.3-models.scorer"

	sp2sp_handler = sp2sp_core()

	if len(sys.argv) < 3:
		print("ERROR! NOT ENOUGH ARGS!")
		print("PLEASE GIVE: \n1. INPUT AUDIO FILE \n2. DESIRED OUTPUT FILE NAME \n3. INPUT LANGUAGE (optional) \n4. OUTPUT LANGUAGE (optional)")
		sys.exit()
	# end-tab

	audio_input = 	sys.argv[1]
	audio_out 	=	sys.argv[2]
	INPUT_LANG 	= 	'en' if len(sys.argv) < 4 else sys.argv[3]
	OUTPUT_LANG = 	'fr' if len(sys.argv) < 5 else sys.argv[4]

	audio_input = os.path.basename(audio_input).split(".")[0] + ".wav"
	audio_out 	= "TEST_OUT.wav"

	text_from_speech = sp2sp_handler.asr_deepspeech(model=asr_model, scorer=asr_scorer, audio=audio_input)
	print("Transrciption: ")
	print(text_from_speech)

	text_translated = sp2sp_handler.translate(text_from_speech, INPUT_LANG, OUTPUT_LANG)
	p = str(text_translated)
	print("Translated Transcription: ")
	print(p)


	sp2sp_handler.txt_to_sp(out_file=audio_out, text=p,lang=OUTPUT_LANG)

