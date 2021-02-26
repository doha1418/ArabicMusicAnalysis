#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 11:40:03 2020

@author: ddoohaa1234
"""

from midiutil import MIDIFile
import random, numpy as np



#===============================================
#a method that creates the dice throws 
#to generate the random numbers in a different 
#method
#==============================================
def DiceThrow(diceAmount):
    dice=[]
    
    #create a column depending on the formula 2^n/2^m 
    m=1
    for i in range(diceAmount):
        
        div=2**m
        changeBit=2**diceAmount/div
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
        while(len(full_col)<2**diceAmount): 
            full_col.extend(col_0)
            full_col.extend(col_1)
        
        dice.append(full_col)
        m+=1
       
 
    return dice


    
def CreatePitchViolin(dice):
    
    voss_constraint_tree=[]
    drange=int(128/len(dice))#determine the number of dice sides
    
    #now create the pitch (the notes), by walking in col-row order
    for i in range(len(dice[0])):#col
        for j in range(len(dice)): #row
            
            if(i==0): #if it is the very first col toss all dice
               tempPitch=random.randint(0,drange)
               voss_constraint_tree.append([tempPitch])#save each pitch to represent the top of the tree
            else:
                if(dice[j][i]!=dice[j][i-1]):
                    tempPitch=random.randint(0,drange)
                    voss_constraint_tree[j].append(tempPitch)
    return voss_constraint_tree


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
      
def MIDIGenerator(pitches,file_name):
    #create a midi file object to add the pitches to

     mf=MIDIFile(1,False)
     track=0
     time=0
     channel=0
     

     mf.addTrackName(track, time, "Voss Track") #
     
     mf.addProgramChange(track,0,0,40) #start the track with a violin on channel 1
     mf.addTempo(track,time,140) #standard tempo rate 150 BPM Considered fast
     
     #a loop that adds a note using mf.addNote(track, channel, pitch, time, duration, volume)
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
     
     for i in range(1,len(pitches)):
         #creates a monotone with no pauses
         
         mf.addTempo(track,time,140)
         mf.addNote(track,channel,pitches[i],t[i],duration[i],100)
        
     
     #write it to disk
     with open(file_name+".mid", 'wb') as outf:
         mf.writeFile(outf)
          
#use 6 dice throws
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


def AjamScale(length,file_name):
    
    
     mf=MIDIFile(1,False)
     track=0
     channel=0
     
     
     pitches=[]
     duration=[]
     time=[]
     #maqaam ajam
     jins_ajam=[60,62,64,65,67]
     jins_ajam_nahawand=[72,70,69,67]
     
     duration_scale_ajam=[0.5,0.25,0.25,0.25,0.5]
     duration_scale_nahawand=[0.5,0.25,0.25,0.5]
     
     randomNote=[60,62,64,65,67,69,71,72,70]
     
     
     tempo=[0.75,0.75,0.5,0.5,0.5]
     scale_tempo=[0.75,0.75,0.5,0.5]
     
     
     counter=0
     for i in range(length):
         
         choice=random.choice([1,2,3])
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
         elif(choice==3):
             for j in range(4):
                 pitches.append(random.choice(randomNote))
                 duration.append(duration_scale_nahawand[j])
                 time.append(counter)
                 counter+=scale_tempo[j]
     print(time)
     
    
            
                     
    
     mf.addTrackName(track, 0, "Voss Track Maqaam Ajam") 
     
     
     mf.addProgramChange(track,0,0,40) #start the track with a violin on channel 1
     mf.addProgramChange(track,1,0,40)
     mf.addTempo(track,0,140) #standard tempo rate 150 BPM Considered fast
     
     
     #a loop that adds a note using mf.addNote(track, channel, pitch, time, duration, volume)
     
     for i in range(0,len(pitches)):
       # mf.addTempo(track,0,110)
        mf.addNote(track,channel,pitches[i],time[i],duration[i],100)
        mf.addNote(track,1,pitches[i],time[i],duration[i],100)
         
     #write it to disk
     with open(file_name+".mid", 'wb') as outf:
         mf.writeFile(outf)

def CompletlyRandomPitchesPianoOnly(length,file_name):
    
     mf=MIDIFile(1,False)
     track=0
     time=0
     channel=0
     
    
     mf.addTrackName(track, time, "Voss Track Random Pitches") 
     
     mf.addProgramChange(track,0,0,0) #start the track with a violin on channel 1
     mf.addTempo(track,time,140) #standard tempo rate 150 BPM Considered fast
    
     
     pitches=[]
   
     
     for i in range(length):
         p=random.randint(60,71) #4th Octave
         pitches.append(p)
       
     
     
     #a loop that adds a note using mf.addNote(track, channel, pitch, time, duration, volume)
     for i in range(0,len(pitches)):
        mf.addTempo(track,time,130)
        mf.addNote(track,channel,pitches[i],i,1,100)
        mf.addNote(track,1,pitches[i])
        
         
     #write it to disk
     with open(file_name+".mid", 'wb') as outf:
         mf.writeFile(outf)
         
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#TODO: add a main method and 
#TODO more logical method on how to run the program through the command line
         #TODO create a function that creates the midi Track to remove redundancy
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!           

          
#debugging DiceThrow method
dice=DiceThrow(7)
pitch=CreatePitchViolin(dice)

tree_sum1=VossTreeSum(pitch)
#AjamScale(20,'Taqaseem_try2_2violin')
#CompletlyRandomPitchesPianoOnly(128,'RandomPitches_noVoss_v6_octave4and5')
#CompletlyRandomPitchesNoVossAjamScale(64,'Scale_3arrangements_ajamJinDuration')
MIDIGenerator(tree_sum1,'voss_7dice_noteTempo_try2')
#MIDIGeneratorRandomizedDuration(tree_sum,'moreduration025_6dice')
#MIDIGeneratorQuarterNotes(tree_sum,'lowerPitch_9dice_v3')
#MIDIGeneratorQuarterNotesVersion2(tree_sum1,'2instruments_150tempo_v3')