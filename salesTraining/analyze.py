import re
import os
from empath import Empath
from numpy import record
import spacy
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import numpy as np

lexicon = Empath()
pattern = r"[.?!]"




r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                
                whole_text += text
    # return the text for all chunks detected
    return whole_text

def analyzeSpeech(model,recordingFile):
    recordingText = get_large_audio_transcription(recordingFile)
    sentences=re.split(pattern, recordingText)
    if len(sentences)==0:
        
        return "error"
    empathDict=lexicon.analyze("testing")
    depDict={}
    nlp = spacy.load('en_core_web_sm')
    depList=["ROOT", "acl", "acomp", "advcl", "advmod", "agent", "amod", "appos", "attr", "aux", "auxpass", "case", "cc", "ccomp", "compound", "conj", "csubj", "csubjpass", "dative", "dep", "det", "dobj", "expl", "intj", "mark", "meta", "neg", "nmod", "npadvmod", "nsubj", "nsubjpass", "nummod", "oprd", "parataxis", "pcomp", "pobj", "poss", "preconj", "predet", "prep", "prt", "quantmod", "relcl", "xcomp"]
    for i in depList:
        depDict[i]=0.0
    for i,value in empathDict.items():
        empathDict[i]=0.0


    for i in range(len(sentences)-1,-1,-1):
        
        sentences[i]=sentences[i].strip()
        if not sentences[i]:
            sentences.pop(i)
            continue
        sentenceDict=lexicon.analyze(sentences[i])
        total=0
        for j,value in sentenceDict.items():
            
            total+=value
        if total==0:
            total=1
        
        for j,value in sentenceDict.items():

            empathDict[j]+=value/total
        
        doc=nlp(sentences[i])
        sentenceDepDict={}
        for depName in depList:
            sentenceDepDict[depName]=0.0
        for token in doc:
           
            if token.dep_ in sentenceDepDict.keys():
                sentenceDepDict[token.dep_]+=1
        
        total=0
        for j,value in sentenceDepDict.items():
            
            total+=value
        
        
        for j,value in sentenceDepDict.items():
            if j in depDict.keys():
                depDict[j]+=value/total
            
    if len(sentences)==0:
        
        return "error"
            
        
    
    total=0
    for i,value in empathDict.items():
        empathDict[i]=value/len(sentences)
        total+=empathDict[i]

    
    total=0
    for i,value in depDict.items():
        depDict[i]=value/len(sentences)
        total+=depDict[i]

    
    
    X=np.array(list(empathDict.values())+list(depDict.values())).reshape(1,-1)
    
    return bool(model.predict(X)[0])