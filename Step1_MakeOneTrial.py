#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a trial loop Step 1
Use this template script to present one trial with your desired structure
@author: katherineduncan
"""
#%% Required set up 
# this imports everything you might need and opens a full screen window
# when you are developing your script you might want to make a smaller window 
# so that you can still see your console 
import numpy as np
import pandas as pd
import os #, sys
import shutil
import psychopy
from psychopy import visual, core, event, gui, logging
import random

# open a white full screen window
screen_x=600
screen_y=600
win = psychopy.visual.Window(size=[screen_x,screen_y],fullscr=False, allowGUI=True, color=[0,0,0], units='height')

# uncomment if you use a clock. Optional because we didn't cover timing this week, 
# but you can find examples in the tutorial code 
#trialClock = core.Clock()

#%% up to you!
# this is where you build a trial that you might actually use one day!
# just try to make one trial ordering your lines of code according to the 
# sequence of events that happen on one trial
# if you're stuck you can use the responseExercise.py answer as a starting point 

#%% Notes
#%% To Do:
# Difference b/w mouse_pos and stim_pos
# Save data
# Heading direction data
# Variable speeds, accelerations, etc.
# Difference b/w mouse_pos and stim_pos depending on heading direction of stimulus
# Keyboard inputs
# Subject inputs, data saving, moving, etc.
# Data analysis
# Possible EEG adaptations
# Possible EEG data analysis
# Instructions?
# 
#%% Experiment Parameters
#block and trial settings
numblocks=1
numtrialsperblock=4
#mouse tracking
mouse = event.Mouse(visible = True,win=win)
#object parameters
c1_rad=.02
#physical limits
spdlmt=.005
acclmt=1
poslmt=.5
acc_multiplier=.001
opp_acc_multiplier=.001
fric=.5 # higher = less friction. Used for wall-bounce only.

#%% Block Start
for block in range(numblocks):
    blocktext=psychopy.visual.TextStim(win=win,
                        name='text',text='block'+str(block),pos=(.5,.46),
                        color='white',height=.04)
    blocktext.draw()
    core.wait(1)
    #%% Trial Start
    for trial in range(numtrialsperblock):
        #clock start
        trialClock = core.Clock()
        #loop stuff
        frame_all=0
        frame_track=0
        frames_per_track=400
        #start object physics
        c1_xpos=0
        c1_ypos=0
        c1_xacc=0*acc_multiplier
        c1_yacc=0*acc_multiplier
        #trail drawing
        trail=[0]
        current_fps=[0]
        #mouse tracking per trial
        mouse.clickReset()
        mouse_pos=[[0,0,0]]
        stim_pos=[[0,0,0]]
        #%% Cue
        #fixation
        fixation=psychopy.visual.Circle(win=win,pos=(0,0),color='white',radius=.01,edges=12)
        circle=psychopy.visual.Circle(win=win,pos=(c1_xpos,c1_ypos),color='white',radius=c1_rad,edges=4)
        text=psychopy.visual.TextStim(win=win,
                    name='text',text='trial'+str(trial),pos=(.5,.46),
                    color='white',height=.04)
        # then draw all stimuli
        #fixation.draw()
        circle.draw()
        text.draw()
        # then flip your window
        win.flip()
        #%% Track
        while 1:
            current_time= trialClock.getTime()
            if current_time%.04 < .01:
                frame_all+=1
                if current_time<=1:
                    mouse.setPos([0,0])
                    mouse_pos.append([frame_all,mouse.getPos()[0],mouse.getPos()[1]])
                    stim_pos.append([frame_all,c1_xpos,c1_ypos])
                else:
                    mouse_pos.append([frame_all,mouse.getPos()[0],mouse.getPos()[1]])
                    stim_pos.append([frame_all,c1_xpos,c1_ypos])
                    if frame_track==0:
                        frame_track_start=frame_all
                        time_track_start=trialClock.getTime()
                    frame_track+=1
                    if frame_track > frames_per_track:
                        break
                    # modulate acceleration towards center by distance from center
                    c1_xacc=c1_xacc+(random.randint(-acclmt,acclmt)*acc_multiplier)+(-c1_xpos*opp_acc_multiplier)
                    c1_yacc=c1_yacc+(random.randint(-acclmt,acclmt)*acc_multiplier)+(-c1_ypos*opp_acc_multiplier)
                    #speedlimit
                    if c1_xacc>spdlmt:
                        c1_xacc=spdlmt
                    elif c1_xacc<-spdlmt:
                        c1_xacc=-spdlmt
                    if c1_yacc>spdlmt:
                        c1_yacc=spdlmt
                    elif c1_yacc<-spdlmt:
                        c1_yacc=-spdlmt
                    c1_xpos=c1_xpos+c1_xacc
                    c1_ypos=c1_ypos+c1_yacc
                    #poslimit
                    if c1_xpos>poslmt:
                        c1_xpos=poslmt
                        c1_xacc=-c1_xacc*fric
                    elif c1_xpos<-poslmt:
                        c1_xpos=-poslmt
                        c1_xacc=-c1_xacc*fric
                    if c1_ypos>poslmt:
                        c1_ypos=poslmt
                        c1_yacc=-c1_yacc*fric
                    elif c1_ypos<-poslmt:
                        c1_ypos=-poslmt
                        c1_yacc=-c1_yacc*fric
                    # maybe start by making stimulus objects (e.g. myPic = visual.ImageStim(...))  
                    #fixation=psychopy.visual.Circle(win=win,pos=(0,0),color='white',radius=.01,edges=12)
                    circle=psychopy.visual.Circle(win=win,pos=(c1_xpos,c1_ypos),color='white',radius=c1_rad,edges=15)
                    text=psychopy.visual.TextStim(win=win,
                        name='text',text='trial'+str(trial),pos=(.5,.46),
                        color='white',height=.04)
                    # draw the trail
                    trail.append(psychopy.visual.Circle(win=win,pos=(c1_xpos,c1_ypos),color='white',radius=c1_rad/6,edges=3))
                    for current_frame in range(frame_track):
                        if current_frame%3 == 0:
                            trail[current_frame+1].draw()
                # fps & trial details text
                current_fps=round(frame_track/current_time,3)
                text_fps=psychopy.visual.TextStim(win=win,
                    name='text',text='fps'+str(current_fps),pos=(.5,.42),
                    color='white',height=.02)
                text_frame=psychopy.visual.TextStim(win=win,
                    name='text',text='frame'+str(frame_all),pos=(.5,.38),
                    color='white',height=.02)
                text_stim_pos=psychopy.visual.TextStim(win=win,
                    name='text',text='stim_pos'+str(stim_pos[frame_all]),pos=(.5,.34),
                    color='white',height=.02)
                text_mouse_pos=psychopy.visual.TextStim(win=win,
                    name='text',text='mouse_pos'+str(mouse_pos[frame_all]),pos=(.5,.30),
                    color='white',height=.02)
                # then draw all stimuli
                #fixation.draw()
                circle.draw()
                text.draw()
                text_fps.draw()
                text_frame.draw()
                text_stim_pos.draw()
                text_mouse_pos.draw()
                # then flip your window
                win.flip()
                # then record your responses
        #%% RI
        #fixation=psychopy.visual.Circle(win=win,pos=(0,0),color='white',radius=.01,edges=12)
        # then draw all stimuli
        #fixation.draw()
        text.draw()
        text_fps.draw()
        text_frame.draw()
        text_stim_pos.draw()
        text_mouse_pos.draw()
        # then flip your window
        win.flip()
        core.wait(1)
        ## Performance View
        performanceClock=core.Clock()
        frame_2=0
        #%% Playback
        while 1:
            current_time_2= performanceClock.getTime()
            if current_time_2%.04 < .01:
                frame_2+=1
                if frame_2 >= frames_per_track:
                    break
                # stim pos and mouse pos
                circle_2=psychopy.visual.Circle(win=win,pos=(stim_pos[frame_2][1],stim_pos[frame_2][2]),color='white',radius=c1_rad,edges=15)
                circle_3=psychopy.visual.Circle(win=win,pos=(mouse_pos[frame_2][1],mouse_pos[frame_2][2]),color='black',radius=c1_rad/3,edges=3)
                # fps & trial details text
                text_frame=psychopy.visual.TextStim(win=win,
                    name='text',text='frame'+str(frame_2),pos=(.5,.38),
                    color='white',height=.02)
                text_stim_pos=psychopy.visual.TextStim(win=win,
                    name='text',text='stim_pos'+str(stim_pos[frame_2]),pos=(.5,.34),
                    color='white',height=.02)
                text_mouse_pos=psychopy.visual.TextStim(win=win,
                    name='text',text='stim_pos'+str(mouse_pos[frame_2]),pos=(.5,.30),
                    color='white',height=.02)
                # then draw all stimuli
                text.draw()
                circle_2.draw()
                circle_3.draw()
                text_frame.draw()
                text_stim_pos.draw()
                text_mouse_pos.draw()
                # then flip your window
                win.flip()
        #%% Save data
        # WIP

#%% Required clean up
# this cell will make sure that your window displays for a while and then 
# closes properly
core.wait(1)
win.close()

#%% your loop here
# start by copying your one trial here, then identify what needs to be
# changed on every trial.  Likely your stimuli, but you might want to change a few things


# make a list or a pd.DataFrame that contains trial-specific info (stimulus, etc)
# e.g. stim = ['1.jpg','2.jpg','3.jpg']

    # include your trial code in your loop but replace anything that should 
    # change on each trial with a variable that uses your iterater
    # e.g. thisStimName = stim[t]
    #      thisStim = visual.ImageStim(win, image=thisStimName ...)
    
    # if you're recording responses, be sure to store your responses in a list
    # or DataFrame which also uses your iterater!

