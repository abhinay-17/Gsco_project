import os
import sys

### We need the pretrained models for the deepspeech system.
TRANSL_STR 		= "deepspeech-0.9.3-models.pbmm"
SCORER_STR 		= "deepspeech-0.9.3-models.scorer"
DEEPSPEECH_DIR 	= "./project/translate/pretrained_models/asr_deepspeech/"

os.system("wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm")
os.system("wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer")
os.system("mv " + TRANSL_STR + " " + DEEPSPEECH_DIR + TRANSL_STR)
os.system("mv " + SCORER_STR + " " + DEEPSPEECH_DIR + SCORER_STR)

# pyaudioanalysis, which is a bit buggy
os.system("git clone http://github.com/pyaudioanalysis")

# install the required python packages
os.system("pip install -r requirements.txt")

