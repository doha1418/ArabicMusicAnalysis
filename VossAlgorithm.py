#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 11:40:03 2020

@author: ddoohaa1234
"""

from midiutil import MIDIFile
import random, numpy as np

class VossExperiment:
    
    
    def _init_(self, diceAmount):
        self.diceAmount=diceAmount

    #===============================================
    #a method that creates the dice throws 
    #to generate the random numbers in a different 
    #method
    #==============================================
    def DiceThrowTable(self):
        dice=[]
        
        #create a column depending on the formula 2^n/2^m 
        m=1
        for i in range(self.diceAmount):
            
            div=2**m
            changeBit=2**self.diceAmount/div
            count=0
            col_0=[]
            col_1=[]
            full_col=[]
            #bit change for each column
            while(count<changeBit):
                col_0.append(0)
                col_1.append(1)
                count+=1
                
            #create the column
            while(len(full_col)<2**self.diceAmount): 
                full_col.extend(col_0)
                full_col.extend(col_1)
            
            dice.append(full_col)
            m+=1
           
     
        return dice
    
    
        
    def CreateVossTree(truthTable):
        
        voss_constraint_tree=[]
        drange=int(128/len(truthTable))#determine the maximum number on the dice
        
        #now create the pitch (the notes), by walking in col-row order
        for i in range(len(truthTable[0])):#col
            for j in range(len(truthTable)): #row
                
                if(i==0): #if it is the very first col toss all dice
                   tempPitch=random.randint(0,drange)
                   voss_constraint_tree.append([tempPitch])#save each pitch to represent the top of the tree
                else:
                    if(truthTable[j][i]!=truthTable[j][i-1]):
                        tempPitch=random.randint(0,drange)
                        voss_constraint_tree[j].append(tempPitch)
            #print(voss_constraint_tree)
        return voss_constraint_tree
    
        
    #sum of tree returns an array with length equal to the bottom of the tree
    def VossTreeSum(tree):
        
        temp=[]
        left_tree=[]
        right_tree=[]
        
        
        #optained the left subtree but upside down
        for i in range(len(tree)-1,0,-1): #row traversal
            
            #col traversal to find the left tree
            for j in range(int(len(tree[i])/2)): 
                temp.append(tree[i][j])
            left_tree.append(temp)
            temp=[]
            
            #col traversal to find right tree
            for j in range(int(len(tree[i])/2),len(tree[i])):
                temp.append(tree[i][j])
            right_tree.append(temp)
            temp=[]
                
        left_tree.append([tree[0][0]])
        right_tree.append([tree[0][1]])
          
        
        left=[]
        right=[]
        left_sum=0
        right_sum=0
        t=0
        i=0
        j=0
        
        #left tree dimentions=right tree dimentions
        while(t<len(left_tree[0])): #repeat computations until all leafs are visited
            
            while(i<len(left_tree) and j<len(left_tree[i])):
                
                
                left_sum+=left_tree[i][j]
                right_sum+=right_tree[i][j]
                
                i+=1
                j/=2
                j=int(j)
            
            left.append(left_sum)
            right.append(right_sum)
            
            left_sum=0
            right_sum=0
                
            t+=1
            j=t
            i=0
        return left+right
    
    #modify this function!!
    def CreateDurationWRandomly(dice):
        
        voss_constraint_tree=[]
        drange=2 #determine the number of dice sides
        
        #now create the pitch (the notes), by walking in col-row order
        for i in range(len(dice[0])):#col
            for j in range(len(dice)): #row
                
                if(i==0): #if it is the very first col toss all dice
                   tempPitch=random(0,drange)
                   voss_constraint_tree.append([tempPitch])#save each pitch to represent the top of the tree
                else:
                    if(dice[j][i]!=dice[j][i-1]):
                        tempPitch=random(0,drange)
                        voss_constraint_tree[j].append(tempPitch)
         
            
        return voss_constraint_tree  
    
    #uses a rythem to play each note from the Voss experiment     
    def MIDIGeneratorSetTempoDuration(pitches,file_name):
        
        #create a midi file object to add the pitches to
         mf=MIDIFile(1,False)
         track=0
         time=0
         channel=0
         
    
         mf.addTrackName(track, time, "Voss Track") #
         
        #start the track with a violin on channel 1
         mf.addProgramChange(track,0,0,40) 
        #standard tempo rate 150 BPM Considered fast
         mf.addTempo(track,time,140) 
         
        
         scale_tempo=[1,1.5,1,1,1.5,1.5]
         note_duration=[1,0.5,0.5,1,0.5,1]
         t=[]
         duration=[]
         
         counter=0
         
         for i in range(int(len(pitches)/4)):
             for j in range(len(scale_tempo)):
                 t.append(counter)
                 counter+=scale_tempo[j]
                 duration.append(note_duration[j])
                
        #a loop that adds a note using mf.addNote(track, channel, pitch, time, duration, volume)
         for i in range(1,len(pitches)):  
             mf.addTempo(track,time,140)
             mf.addNote(track,channel,pitches[i],t[i],duration[i],100)
            
         
         #write it to disk
         with open(file_name+".mid", 'wb') as outf:
             mf.writeFile(outf)
              
    #Random note duration
    def MIDIGeneratorRandomizedDuration(part1pitches,file_name):
        
         mf=MIDIFile(1,False)
         track=0
         time=0
         channel=0
         
    
         mf.addTrackName(track, time, "Voss Track Random Durations") #
         
         mf.addProgramChange(track,0,0,40) #start the track with a violin on channel 1
         mf.addTempo(track,time,140) #standard tempo rate 150 BPM Considered fast
         
    
         #a loop that adds a note using mf.addNote(track, channel, pitch, time, duration, volume)
         for i in range(1,len(part1pitches)):
             #play each 
            
            mf.addTempo(track,time,140)
            duration=random.choice([1,1.25])
            if(duration==1):
                mf.addNote(track,channel,part1pitches[i],i,duration,100)
            else:
                mf.addNote(track,channel,part1pitches[i],i+0.25,duration,100)
             
         
         #write it to disk
         with open(file_name+".mid", 'wb') as outf:
             mf.writeFile(outf)
    
    #all notes set as quarter notes, no rythem         
    def MIDIGeneratorQuarterNotes(part1pitches,file_name):
        
         mf=MIDIFile(1,False)
         track=0
         time=0
         channel=0
         
    
         mf.addTrackName(track, time, "Voss Track 1.25 Duration") #
         
         mf.addProgramChange(track,0,0,40) #start the track with a violin on channel 1
         mf.addTempo(track,time,140) #standard tempo rate 150 BPM Considered fast
         
         #a loop that adds a note using mf.addNote(track, channel, pitch, time, duration, volume)
         for i in range(0,len(part1pitches)):
             #play each 
            
            mf.addTempo(track,time,140)
            mf.addNote(track,channel,part1pitches[i],i+0.25,1.25,100)
             
                      
            
         
         #write it to disk
         with open(file_name+".mid", 'wb') as outf:
             mf.writeFile(outf)
             
    
    def MIDIGeneratorQuarterNotesVersion2(part1pitches,file_name):
        
         mf=MIDIFile(1,False)
         track=0
         time=0
         channel=0
       
         
    
         mf.addTrackName(track, time, "Voss Track") 
         
         mf.addProgramChange(track,0,0,0) #start the track with a violin on channel 1
         mf.addTempo(track,time,140) #standard tempo rate 150 BPM Considered fast
         mf.addProgramChange(track,1,0,40)
         #a loop that adds a note using mf.addNote(track, channel, pitch, time, duration, volume)
         j=0
         for i in range(1,len(part1pitches)):
             #play each 
            if(j<8):
                mf.addTempo(track,time,140)
                mf.addNote(track,channel,part1pitches[i],i+0.25,1.25,100)
                mf.addNote(track,1,part1pitches[i],i+0.25,1.25,100)
                j+=1
            else:
                mf.addTempo(track,time,140)
                mf.addNote(track,channel,part1pitches[i],i+0.25,1,100)
                mf.addNote(track,1,part1pitches[i],i+0.25,1.25,100)
                j=0
             
                      
         #write it to disk
         with open(file_name+".mid", 'wb') as outf:
             mf.writeFile(outf)
    
    
    
             
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #TODO: add a main method and 
    #TODO more logical method on how to run the program through the command line
             #TODO create a function that creates the midi Track to remove redundancy
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!           
class runVossExperiment:
    def main():
        
        print("Experiment running: ")
        diceAmount= input("Enter amount of dice to run in the experiment")
        diceAmount=int(diceAmount)
        
        Experiment= VossExperiment(diceAmount)
        
        #create a truth table based on the number of dice required
        truthTable=Experiment.DiceThrowTable()
        tree=Experiment.CreateVossTree(truthTable)
        
        pitches=Experiment.VossTreeSum(tree)
        
        print("Experiment ran successfully")
        generate=input("Enter Y to generate MIDI file and WAV file: ")
        
        
        if(generate.lower()=="y"):
            file_name=input("Enter a file name: ")
            Experiment.MIDIGeneratorSetTempoDuration(pitches,file_name)
        
                
    
    
         
#debugging DiceThrow method
#dice=DiceThrow(3)
#print(dice)
#pitch=CreatePitchViolin(dice)
#print(pitch)
#tree_sum=VossTreeSum(pitch)
#print(tree_sum)
#MIDIGeneratorSetTempoDuration(tree_sum,'voss_7dice_noteTempo_try2')
#MIDIGeneratorRandomizedDuration(tree_sum,'moreduration025_6dice')
#MIDIGeneratorQuarterNotes(tree_sum,'lowerPitch_9dice_v3')
#MIDIGeneratorQuarterNotesVersion2(tree_sum,'2instruments_150tempo_v3')
