from naoqi import ALProxy

tts = ALProxy("ALTextToSpeech", "172.30.248.111", 9559)

tts.setLanguage('Dutch')
tts.say("test")

# tts.setLanguage('English')
# tts.say("Hello!")