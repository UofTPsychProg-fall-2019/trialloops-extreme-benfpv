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

########################
#### Quick Settings ####
########################
debug=1 #Debug mode on (1) or off (0).
debug_fps=1

# open a white full screen window
screen_x=600
screen_y=600
framerate=30

time_per_frame=1/framerate
time_per_frame_precision=time_per_frame/4

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

#%% Experiment Parameters
#block and trial settings
numblocks=1
numtrialsperblock=2
frames_per_track=200
#mouse tracking
mouse = event.Mouse(visible=False,win=win)
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
    current_block = block+1
    blocktext=psychopy.visual.TextStim(win=win,
                        name='text',text='block'+str(block),pos=(.5,.46),
                        color='white',height=.04)
    blocktext.draw()
    core.wait(1)
    #%% Trial Start
    for trial in range(numtrialsperblock):
        # current_trial
        current_trial=trial+1
        #loop stuff
        frame_all=0
        frame_track=0
        #start object physics
        c1_xpos=0
        c1_ypos=0
        c1_xacc=0*acc_multiplier
        c1_yacc=0*acc_multiplier
        #trail drawing
        trail=[0]
        current_fps=[0]
        #durations/timing/randomized times
        current_cue_dur=random.randint(1000,2500)/1000
        current_track_dur=random.randint(5000,10000)/1000
        current_ri_dur=random.randint(1000,1000)/1000
        #mouse tracking per trial
        mouse.clickReset()
        stim_pos=[[0,0,0]]
        mouse_pos=[[0,0,0]]
        #clock start
        trialClock=core.Clock()
        #%% Cue
        #fixation
        #fixation=psychopy.visual.Circle(win=win,pos=(0,0),color='white',radius=.01,edges=12)
        tgtcircle=psychopy.visual.Circle(win=win,pos=(c1_xpos,c1_ypos),color='white',radius=c1_rad,edges=14)
        text=psychopy.visual.TextStim(win=win,
                    name='text',text='trial'+str(trial),pos=(.5,.46),
                    color='white',height=.04)
        # then draw all stimuli
        #fixation.draw()
        tgtcircle.draw()
        text.draw()
        # then flip your window
        win.flip()
        # cue start time
        time_cue_start=trialClock.getTime()
        #%% Track
        while 1:
            current_time=trialClock.getTime()
            # framerate set here... time%.004<.001
            if current_time%time_per_frame<time_per_frame_precision:
                frame_all+=1
                if current_time<=current_cue_dur:
                    mouse.setPos([0,0])
                else:
                    # end trial if >current_track_dur
                    if current_time>=current_track_dur:
                        frame_track_end=frame_track
                        time_track_end=current_time
                        break
                    # frame_track
                    frame_track+=1
                    # frame_track conditions
                    if frame_track==1:
                        time_track_start=trialClock.getTime()
                    stim_pos.append([frame_track,c1_xpos,c1_ypos])
                    mouse_pos.append([frame_track,mouse.getPos()[0],mouse.getPos()[1]])
                    # accuracy calculation
                    if frame_track==0:
                        current_acc_x=[stim_pos[current_trial-1][2][frame_track][1]-mouse_pos[current_trial-1][2][frame_track][1]]
                        current_acc_y=[stim_pos[current_trial-1][2][frame_track][2]-mouse_pos[current_trial-1][2][frame_track][2]]
                    else:
                        current_acc_x.append([stim_pos[current_trial-1][2][frame_track][1]-mouse_pos[current_trial-1][2][frame_track][1]])
                        current_acc_y.append([stim_pos[current_trial-1][2][frame_track][2]-mouse_pos[current_trial-1][2][frame_track][2]])
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
                    if debug==1:
                        text=psychopy.visual.TextStim(win=win,
                            name='text',text='trial'+str(trial),pos=(.5,.46),
                            color='white',height=.04)
                    # draw the trail
                    if trail==1:
                        trail.append(psychopy.visual.Circle(win=win,pos=(c1_xpos,c1_ypos),color='white',radius=c1_rad/6,edges=3))
                        for current_frame in range(frame_track):
                            if current_frame%5 == 0:
                                trail[current_frame+1].draw()
                    # position text
                    if debug==1:
                        text_stim_pos=psychopy.visual.TextStim(win=win,
                            name='text',text='stim_pos'+str(stim_pos[frame_track]),pos=(.5,.34),
                            color='white',height=.02)
                        text_mouse_pos=psychopy.visual.TextStim(win=win,
                            name='text',text='mouse_pos'+str(mouse_pos[frame_track]),pos=(.5,.30),
                            color='white',height=.02)
                # moving stims
                tgtcircle=psychopy.visual.Circle(win=win,pos=(c1_xpos,c1_ypos),color='white',radius=c1_rad,edges=14)
                mousecircle=psychopy.visual.Circle(win=win,pos=(mouse.getPos()[0],mouse.getPos()[1]),color='black',radius=c1_rad/3,edges=14)
                # fps & trial details text
                if debug_fps==1:
                    current_fps=round(frame_track/current_time,2)
                    text_fps=psychopy.visual.TextStim(win=win,
                        name='text',text='fps'+str(current_fps),pos=(.5,.42),
                        color='white',height=.02)
                    text_frame=psychopy.visual.TextStim(win=win,
                        name='text',text='frame'+str(frame_track),pos=(.5,.38),
                        color='white',height=.02)
                # then draw all stimuli
                #fixation.draw()
                tgtcircle.draw()
                mousecircle.draw()
                if debug==1:
                    text.draw()
                    text_stim_pos.draw()
                    text_mouse_pos.draw()
                if debug_fps==1:
                    text_fps.draw()
                    text_frame.draw()
                # then flip your window
                win.flip()
                # then record your responses
        #%% RI
        #fixation=psychopy.visual.Circle(win=win,pos=(0,0),color='white',radius=.01,edges=12)
        # then draw all stimuli
        #fixation.draw()
        if debug==1:
            text.draw()
            text_stim_pos.draw()
            text_mouse_pos.draw()
        if debug_fps==1:
            text_fps.draw()
            text_frame.draw()
        # then flip your window
        win.flip()
        core.wait(current_ri_dur)
        ## Performance View
        performanceClock=core.Clock()
        frame_2=-1
        #%% Playback
        if debug==1:
            while 1:
                current_time_2=performanceClock.getTime()
                if current_time%time_per_frame<time_per_frame_precision:
                    frame_2+=1
                    if frame_2>=frame_track_end:
                        break
                    # stim pos and mouse pos
                    tgtcircle_2=psychopy.visual.Circle(win=win,pos=(stim_pos[frame_2][1],stim_pos[frame_2][2]),color='white',radius=c1_rad,edges=14)
                    mousecircle_2=psychopy.visual.Circle(win=win,pos=(mouse_pos[frame_2][1],mouse_pos[frame_2][2]),color='black',radius=c1_rad/3,edges=3)
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
                    tgtcircle_2.draw()
                    mousecircle_2.draw()
                    text_frame.draw()
                    text_stim_pos.draw()
                    text_mouse_pos.draw()
                    # then flip your window
                    win.flip()
        #%% Save data!
        # To access position data per trial:
        # xxxx_pos_data[block][trial][timepoint]
        if current_trial==1:
            d_block=[current_block]
            d_trial=[current_trial]
            d_cue_dur=[current_cue_dur]
            d_track_dur=[current_track_dur]
            d_time_cue_start=[time_cue_start]
            d_time_track_start=[time_track_start]
            d_time_track_end=[time_track_end]
            d_frame_track_end=[frame_track_end]
            d_stim_pos = [[current_block,current_trial,stim_pos]]
            d_mouse_pos = [[current_block,current_trial,mouse_pos]]
            d_acc_x=[current_acc_x]
            d_acc_y=[current_acc_y]
        else:
            d_block.append(current_block)
            d_trial.append(current_trial)
            d_cue_dur.append(current_cue_dur)
            d_track_dur.append(current_track_dur)
            d_time_cue_start.append(time_cue_start)
            d_time_track_start.append(time_track_start)
            d_time_track_end.append(time_track_end)
            d_frame_track_end.append(frame_track_end)
            d_stim_pos.append([current_block,current_trial,stim_pos])
            d_mouse_pos.append([current_block,current_trial,mouse_pos])
            d_acc_x.append([current_acc_x])
            d_acc_y.append([current_acc_y])
#%% Required clean up
# this cell will make sure that your window displays for a while and then 
# closes properly
core.wait(1)
win.close()

