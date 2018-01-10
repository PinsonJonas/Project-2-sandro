from naoqi import ALProxy

tts = ALProxy("ALTextToSpeech", "192.168.43.192", 9559)

tts.setLanguage('Dutch')
tts.say("test")

# tts.setLanguage('English')
# tts.say("Hello!")