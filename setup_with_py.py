import os
import sys

TRANSL_STR 		= ""
SCORER_STR 		= ""
DEEPSPEECH_DIR 	= "./project/translate/pretrained_models/asr_deepspeech/"

os.system("git clone http://github.com/pyaudioanalysis")
os.system("git clone http://github.com/deepspeech")
os.system("mv " + TRANSL_STR + " " + DEEPSPEECH_DIR + TRANSL_STR)
os.system("mv " + SCORER_STR + " " + DEEPSPEECH_DIR + SCORER_STR)
os.system("rm -r deepspeech/")


