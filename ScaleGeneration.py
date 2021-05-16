from midiutil import MIDIFile
import random, numpy as np


class ScaleExperiment:
    
    def __init__(self, length):
        self.length=length
       
    
    def AjamScale(self,length,file_name):
        
        
         mf=MIDIFile(1,False)
         track=0
         channel=0
         
         
         pitches=[]
         duration=[]
         time=[]
         #maqaam ajam
         jins_ajam=[60,62,64,65,67]
         jins_upper_ajam=[67, 69, 71, 72]
         jins_ajam_nahawand=[72,70,69,67]
         
         duration_scale_ajam=[1,1,1,1,1]
         duration_scale_nahawand=[1,1,1,1,1]
         
         randomNote=[60,62,64,65,67,69,71,72,70]
         
         
         tempo=[1,1.5,1,1.5,1]
         scale_tempo=[1,1.5,1,1.5]
         
         
         counter=0
         for i in range(length):
             
             choice=random.choice([1,2,3,4,5])
             if(choice==1):
                 for j in range(len(jins_ajam)):
                     pitches.append(jins_ajam[j])
                     duration.append(duration_scale_ajam[j])
                     time.append(counter)
                     counter+=tempo[j]
             elif(choice==2):
                 for j in range(len(jins_ajam_nahawand)):
                     pitches.append(jins_ajam_nahawand[j])
                     duration.append(duration_scale_nahawand[j])
                     time.append(counter)
                     counter+=scale_tempo[j]
             elif(choice==2):
                 for j in range(len(jins_upper_ajam)):
                     pitches.append(jins_upper_ajam[j])
                     duration.append(duration_scale_nahawand[j])
                     time.append(counter)
                     counter+=scale_tempo[j]
             elif(choice==4 or choice==5):
                 for j in range(4):
                     pitches.append(random.choice(randomNote))
                     duration.append(duration_scale_ajam[j])
                     time.append(counter)
                     counter+=scale_tempo[j]
        
         
        
                
                         
        
         mf.addTrackName(track, 0, "Voss Track Maqaam Ajam") 
         
         
         mf.addProgramChange(track,0,0,40) #start the track with a violin on channel 1
         mf.addTempo(track,0,140) #standard tempo rate 150 BPM Considered fast
         
         
         #a loop that adds a note using mf.addNote(track, channel, pitch, time, duration, volume)
         
         for i in range(0,len(pitches)):
           # mf.addTempo(track,0,110)
            mf.addNote(track,channel,pitches[i],time[i],duration[i],100)

             
         #write it to disk
         with open(file_name+".mid", 'wb') as outf:
             mf.writeFile(outf)
    
    def CompletlyRandomPitches(self,length,file_name):
        
         mf=MIDIFile(1,False)
         track=0
         time=0
         channel=0
         
        
         mf.addTrackName(track, time, "Voss Track Random Pitches") 
         
         mf.addProgramChange(track,0,0,40) #start the track with a violin on channel 1
         mf.addTempo(track,time,140) #standard tempo rate 150 BPM Considered fast
        
         
         pitches=[]
       
         
         for i in range(length):
             p=random.randint(60,71) #4th Octave
             pitches.append(p)

         #a loop that adds a note using mf.addNote(track, channel, pitch, time, duration, volume)
         for i in range(0,len(pitches)):
            mf.addTempo(track,time,130)
            mf.addNote(track,channel,pitches[i],i,1,100)
           
            
             
         #write it to disk
         with open(file_name+".mid", 'wb') as outf:
             mf.writeFile(outf)
             
class RunExperiment:
    def main():
           
            
            try:
                print("Experiment running: ")
                
                generate=input("Enter Y to generate MIDI file and WAV file: ")
                
                #other types of experiments missing
                if(generate.lower()=="y"):
                    
                    print("Choose the rhythmic effect")
                    print("1. Ajam Arabic scale")
                    print("2. Randomized pitches ")
                 
                    expType=input("Enter here: ")
                    expType=int(expType)
                    
                    file_name=input("Enter a file name: ")
                    
                    if(expType==1):
                        length= input("Enter amount of runs in the experiment: ")
                        length=int(length)
                        Experiment= ScaleExperiment(length)
                        Experiment.AjamScale(length,file_name)
                        print("Experiment ran successfully")
                    elif(expType==2):
                        
                       length= input("Enter amount of runs in the experiment: ")
                       length=int(length)
                       Experiment= ScaleExperiment(length)
                       Experiment.CompletlyRandomPitches(length,file_name)
                       print("Experiment ran successfully")
                    
                else:
                    print("Program terminated")
            except:
                print("Something went wrong")

    main() 

