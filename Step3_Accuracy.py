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

############################
#### Experiment Details ####
############################
# 1) Endogenous and exogenous attention cycling? 50% exogenous, 50% endogenous.
# Can achieve this with 2 orbiting stimuli. Orbits randomly though! Can go
# above or below 50% of the time.
# OR, when a specific fixation color, track. Otherwise, don't track. Endogenous.
# When specific target color, track. Otherwise, don't track. Exogenous.
# Counterbalance colors. Points for keeping mouse still when not tracking?
# BUT! Trial can end at any time, and must report location after RI. Click on where
# stimulus was.
# 1a) Analysis; Take frequency. Should both be 4 Hz. But, 4 Hz should be at
# different points of cycle. How to parse this?
# Analyze at what time points the endogenous and exogenous Hz occur.
# Are they significantly different at any time points when compared?
# Is their difference between frequency across time also at 4 Hz?
# Then this would suggest they are cycling.

# 2) Can feedback help tracking performance? Predict trial-by-trial accuracy
# using heatmap/fourier.

# TO DO
# Above, and add a acc_rad visualization to heatmap. Line radius = mean acc_rad,
# and circles for SD of acc_rad. 95% confidence interval?

########################
#### Quick Settings ####
########################
# Note: Position is always defined as maximum of .5, and in coordinate plane.
debug=1 #Debug mode on (1) or off (0).
debug_fps=1 #shows fps data
trial_analysis=1 #Trial-by-trial analysis, used for model-prediction.
frame_analysis=1 #Frame-by-frame analysis, used for model-prediction.

# open a white full screen window
screen_x=700
screen_y=700
framerate=60

# background color
background_color='black'

time_per_frame=1/framerate
time_per_frame_precision=time_per_frame/4

win = psychopy.visual.Window(size=[screen_x,screen_y],fullscr=False, allowGUI=True, color=background_color, units='height')

#%% up to you!
# this is where you build a trial that you might actually use one day!
# just try to make one trial ordering your lines of code according to the 
# sequence of events that happen on one trial
# if you're stuck you can use the responseExercise.py answer as a starting point 

#%% Notes
#%% To Do:
# Save data
# Heading direction data
# Variable speeds, accelerations, etc.
# Difference b/w mouse_pos and stim_pos depending on heading direction of stimulus
# Subject inputs, data saving, moving, etc.
# Instructions?

#%% Experiment Parameters
#block and trial settings
numblocks=1
numtrialsperblock=6
#mouse tracking
if debug==1:
    mouse=event.Mouse(visible=True,win=win)
else:
    mouse=event.Mouse(visible=False,win=win)
#object parameters
c1_rad=.02
#physical limits
spdlmt=.005
acclmt=1
poslmt=.5
startpos_buf=.1
acc_multiplier=.001
opp_acc_multiplier=.001
fric=.5 # higher = less friction. Used for wall-bounce only.
#permanent durations
current_fb_dur=5
iti_dur=.25
#fixation
fixation=psychopy.visual.Circle(win=win,pos=(0,0),color='white',radius=.002,edges=12)
#%% Block Start
for block in range(numblocks):
    current_block = block+1
    blocktext=psychopy.visual.TextStim(win=win,
                        name='text',text='block'+str(block),pos=(.5,.46),
                        color='white',height=.015)
    blocktext.draw()
    core.wait(1)
    #%% ADD A "START BLOCK" INPUT!!!
    #%% Trial Start
    for trial in range(numtrialsperblock):
        # current_trial
        current_trial=trial+1
        #loop stuff
        frame_all=0
        frame_track=0
        # start object physics
        c1_xpos=(random.randint(0,1000)/1000)*(poslmt-startpos_buf)
        c1_ypos=(random.randint(0,1000)/1000)*(poslmt-startpos_buf)
        c1_xacc=0*acc_multiplier
        c1_yacc=0*acc_multiplier
        #trail drawing
        trail=[0]
        current_fps=[0]
        # durations/timing/randomized times
        current_cue_dur=random.randint(500,1500)/1000
        current_track_dur=random.randint(5000,10000)/1000
        current_ri_dur=1
        # vwm reset conditions
        start_reset=random.randint(0,1)
        # mouse tracking per trial
        mouse.clickReset()
        stim_pos=[[0.0,0.0]]
        mouse_pos=[[0.0,0.0]]
        #accuracy tracking
        current_acc_x=[0.0]
        current_acc_y=[0.0]
        # INTER TRIAL INTERVAL (IVI)
        core.wait(iti_dur)
        # clock start
        trialClock=core.Clock()
        #%% Cue
        time_cue_start=trialClock.getTime()
        mouse.setPos([c1_xpos,c1_ypos])
        while 1:
            time_cue=trialClock.getTime()
            if time_cue>=current_cue_dur:
                time_cue_end=time_cue
                break
            #fixation
            tgtcircle=psychopy.visual.Circle(win=win,pos=(c1_xpos,c1_ypos),color='white',radius=c1_rad,edges=14)
            text=psychopy.visual.TextStim(win=win,
                        name='text',text='trial'+str(trial),pos=(.5,.46),
                        color='white',height=.015)
            # moving stims
            mousecircle=psychopy.visual.Circle(win=win,pos=(mouse.getPos()[0],mouse.getPos()[1]),color='grey',radius=c1_rad/3,edges=14)
            # then draw all stimuli
            fixation.draw()
            tgtcircle.draw()
            mousecircle.draw()
            text.draw()
            # then flip your window
            win.flip()
        #%% Track
        while 1:
            time_track=trialClock.getTime()
            # framerate set here... time%.004<.001
            if time_track%time_per_frame<time_per_frame_precision:
                # frame_track
                frame_track+=1
                # frame_track conditions
                # mouse/stim pos track
                stim_pos.append([c1_xpos,c1_ypos])
                mouse_pos.append([mouse.getPos()[0],mouse.getPos()[1]])
                # accuracy calculations
                current_acc_x.append(mouse_pos[frame_track][0]-stim_pos[frame_track][0])
                current_acc_y.append(mouse_pos[frame_track][1]-stim_pos[frame_track][1])
                # modulate acceleration towards center by distance from center
                c1_xacc=c1_xacc+(random.randint(-acclmt,acclmt)*acc_multiplier)+(-c1_xpos*opp_acc_multiplier)
                c1_yacc=c1_yacc+(random.randint(-acclmt,acclmt)*acc_multiplier)+(-c1_ypos*opp_acc_multiplier)
                # speedlimit
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
                # poslimit
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
                if frame_track==1:
                    time_track_start=time_track
                    # track initiation accel/reset condition
                    if start_reset==1:
                        c1_xpos=(random.randint(0,1000)/1000)*(poslmt-startpos_buf)
                        c1_ypos=(random.randint(0,1000)/1000)*(poslmt-startpos_buf)
                        c1_xacc=0*acc_multiplier
                        c1_yacc=0*acc_multiplier
                # end trial if >current_track_dur
                if time_track>=current_track_dur:
                    frame_track_end=frame_track
                    time_track_end=time_track
                    time_track_dur=time_track_end-time_track_start
                    break
                # maybe start by making stimulus objects (e.g. myPic = visual.ImageStim(...))
                if debug==1:
                    text=psychopy.visual.TextStim(win=win,
                        name='text',text='trial'+str(trial),pos=(.5,.46),
                        color='white',height=.015)
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
                        color='white',height=.015)
                    text_mouse_pos=psychopy.visual.TextStim(win=win,
                        name='text',text='mouse_pos'+str(mouse_pos[frame_track]),pos=(.5,.30),
                        color='white',height=.015)
                    text_time=psychopy.visual.TextStim(win=win,
                        name='text',text='time'+str(time_track-time_track_start),pos=(.5,.40),
                        color='white',height=.015)
                # moving stims
                tgtcircle=psychopy.visual.Circle(win=win,pos=(c1_xpos,c1_ypos),color='white',radius=c1_rad,edges=14)
                mousecircle=psychopy.visual.Circle(win=win,pos=(mouse.getPos()[0],mouse.getPos()[1]),color='grey',radius=c1_rad/3,edges=14)
                # fps & trial details text
                if debug_fps==1:
                    current_fps=round(frame_track/time_track,2)
                    text_fps=psychopy.visual.TextStim(win=win,
                        name='text',text='fps'+str(current_fps),pos=(.5,.42),
                        color='white',height=.015)
                    text_frame=psychopy.visual.TextStim(win=win,
                        name='text',text='frame'+str(frame_track),pos=(.5,.38),
                        color='white',height=.015)
                if debug==1:
                    text.draw()
                    text_stim_pos.draw()
                    text_mouse_pos.draw()
                if debug_fps==1:
                    text_fps.draw()
                    text_frame.draw()
                    text_time.draw()
                # then draw all stimuli
                fixation.draw()
                tgtcircle.draw()
                mousecircle.draw()
                # then flip your window
                win.flip()
        #%% By-trial Analysis
        # To access position data per trial:
        # d_xxx_pos[block][trial][timepoint]
        time_analysis_start=trialClock.getTime()
        trial_fps=frame_track_end/time_track_dur
        trial_tpf=time_track_dur/frame_track_end #time per frame (tpf)
        if trial_analysis==1:
            # Collapse data to 1-dimensional (i.e., radius from target).
            for current_acc in range(len(current_acc_x)):
                if current_acc==0:
                    acc_rad=[np.sqrt(current_acc_x[current_acc]**2+current_acc_y[current_acc]**2)]
                else:
                    acc_rad.append(np.sqrt(current_acc_x[current_acc]**2+current_acc_y[current_acc]**2))
            # Plot a 2d 'heatmap' of accuracy.
            for current_pix in range(len(acc_rad)):
                if current_pix==0:
                    heatmap=[psychopy.visual.Circle(win=win,pos=(current_acc_x[current_pix],current_acc_y[current_pix]),color=current_pix/len(acc_rad),colorSpace='rgb',radius=.001,edges=4)]
                else:
                    heatmap.append(psychopy.visual.Circle(win=win,pos=(current_acc_x[current_pix],current_acc_y[current_pix]),color=current_pix/len(acc_rad),colorSpace='rgb',radius=.001,edges=4))
            # Fourier transform of mouse-stim accuracy throughout trial.
            fourier_freqs=[2,4,6,8,10] #frequency in seconds of one complete fourier cycle.
            fourier_magnifier=8
            for freq in range(len(fourier_freqs)):
                if freq==0:
                    fourier_fpf=[trial_fps*fourier_freqs[freq]] #frames per fourier_freq
                    fourier_dpf=[360/fourier_fpf[freq]] #degrees per frame on 360 circular space
                else:
                    fourier_fpf.append(trial_fps*fourier_freqs[freq])
                    fourier_dpf.append(360/fourier_fpf[freq])
                for acc in range(len(acc_rad)):
                    if acc==0:
                        fourier_acc_rad_x=[np.cos(fourier_dpf[freq]*acc)*acc_rad[acc]*fourier_magnifier]
                        fourier_acc_rad_y=[np.sin(fourier_dpf[freq]*acc)*acc_rad[acc]*fourier_magnifier]
                        if fourier_freqs[freq]==4 or fourier_freqs[freq]==8:
                            fourier_graph=[psychopy.visual.Circle(win=win,pos=(fourier_acc_rad_x[acc],fourier_acc_rad_y[acc]),color=(0,0,1),colorSpace='rgb',radius=.001,edges=4)]
                        else:
                            fourier_graph=[psychopy.visual.Circle(win=win,pos=(fourier_acc_rad_x[acc],fourier_acc_rad_y[acc]),color=freq/len(fourier_freqs),colorSpace='rgb',radius=.001,edges=4)]
                    else:
                        fourier_acc_rad_x.append(np.cos(fourier_dpf[freq]*acc)*acc_rad[acc]*fourier_magnifier)
                        fourier_acc_rad_y.append(np.sin(fourier_dpf[freq]*acc)*acc_rad[acc]*fourier_magnifier)
                        if fourier_freqs[freq]==4 or fourier_freqs[freq]==8:
                            fourier_graph.append(psychopy.visual.Circle(win=win,pos=(fourier_acc_rad_x[acc],fourier_acc_rad_y[acc]),color=(0,0,1),colorSpace='rgb',radius=.001,edges=4))
                        else:
                            fourier_graph.append(psychopy.visual.Circle(win=win,pos=(fourier_acc_rad_x[acc],fourier_acc_rad_y[acc]),color=freq/len(fourier_freqs),colorSpace='rgb',radius=.001,edges=4))
                if freq==0:
                    fourier_graph_freq=[fourier_graph]
                    fourier_cog_x=[np.mean(fourier_acc_rad_x)]
                    fourier_cog_y=[np.mean(fourier_acc_rad_y)]
                    if fourier_freqs[freq]==4 or fourier_freqs[freq]==8:
                        fourier_cog_dot=[psychopy.visual.Circle(win=win,pos=(fourier_cog_x[freq],fourier_cog_y[freq]),color=(0,1,1),colorSpace='rgb',radius=.002,edges=4)]
                    else:
                        fourier_cog_dot=[psychopy.visual.Circle(win=win,pos=(fourier_cog_x[freq],fourier_cog_y[freq]),color=(1,0,0),colorSpace='rgb',radius=.002,edges=4)]
                else:
                    fourier_graph_freq.append(fourier_graph)
                    fourier_cog_x.append(np.mean(fourier_acc_rad_x))
                    fourier_cog_y.append(np.mean(fourier_acc_rad_y))
                    if fourier_freqs[freq]==4 or fourier_freqs[freq]==8:
                        fourier_cog_dot.append(psychopy.visual.Circle(win=win,pos=(fourier_cog_x[freq],fourier_cog_y[freq]),color=(0,1,1),colorSpace='rgb',radius=.002,edges=4))
                    else:
                        fourier_cog_dot.append(psychopy.visual.Circle(win=win,pos=(fourier_cog_x[freq],fourier_cog_y[freq]),color=(1,0,0),colorSpace='rgb',radius=.002,edges=4))
        # RI - time taken to do the trial analyses.
        time_analysis_dur=trialClock.getTime()-time_analysis_start
        #%% RI
        # then draw all stimuli
        fixation.draw()
        if debug==1:
            text.draw()
            text_stim_pos.draw()
            text_mouse_pos.draw()
        if debug_fps==1:
            text_fps.draw()
            text_frame.draw()
            text_time.draw()
        # then flip your window
        win.flip()
        core.wait(current_ri_dur-time_analysis_dur)
        #%% By-trial Feedback
        # Heatmap
        text_heatmap=psychopy.visual.TextStim(win=win,
            name='text',text='trial accuracy t-collapsed heatmap',pos=(.7,.4),
            color='white',height=.015)
        text_fb=psychopy.visual.TextStim(win=win,
                name='text',text=str(round(np.mean(acc_rad),2)*100),pos=(.7,.35),
                color='white',height=.015)
        #draw heatmap
        fixation.draw()
        text_fb.draw()
        for current_pix in range(len(heatmap)):
            heatmap[current_pix].draw()
        text_heatmap.draw()
        # then flip your window
        win.flip()
        core.wait(current_fb_dur/2)
        # Fourier transform
        text_fourier=psychopy.visual.TextStim(win=win,
            name='text',text='trial accuracy fourier transform',pos=(.7,.45),
            color='white',height=.015)
        text_fourier_desc=psychopy.visual.TextStim(win=win,
            name='text',text='blue 4hz 8hz, red center of gravity',pos=(.7,.4),
            color='white',height=.015)
        text_fb=psychopy.visual.TextStim(win=win,
                name='text',text=str(round(np.mean(acc_rad),2)*100),pos=(.7,.35),
                color='white',height=.015)
        #draw Fourier
        fixation.draw()
        text_fb.draw()
        text_fourier.draw()
        text_fourier_desc.draw()
        for current_freq in range(len(fourier_graph_freq)):
            for current_pix in range(len(fourier_graph)):
                fourier_graph_freq[current_freq][current_pix].draw()
                fourier_graph_freq[freq==4][current_pix].draw()
                fourier_graph_freq[freq==8][current_pix].draw()
            fourier_cog_dot[current_freq].draw()
            fourier_cog_dot[freq==4].draw()
            fourier_cog_dot[freq==8].draw()
        # then flip your window
        win.flip()
        core.wait(current_fb_dur*1.5)
        #%% Playback (For debugging)
        ## Performance View
        performanceClock=core.Clock()
        frame_2=-1
        if debug==1:
            while 1:
                time_track_2=performanceClock.getTime()
                if time_track_2%trial_tpf<time_per_frame_precision:
                    frame_2+=1
                    if frame_2>=frame_track_end:
                        break
                    # stim pos and mouse pos
                    tgtcircle_2=psychopy.visual.Circle(win=win,pos=(stim_pos[frame_2][0],stim_pos[frame_2][1]),color='white',radius=c1_rad,edges=14)
                    mousecircle_2=psychopy.visual.Circle(win=win,pos=(mouse_pos[frame_2][0],mouse_pos[frame_2][1]),color='grey',radius=c1_rad/3,edges=3)
                    # fps & trial details text
                    text_frame=psychopy.visual.TextStim(win=win,
                        name='text',text='frame'+str(frame_2),pos=(.5,.38),
                        color='white',height=.015)
                    text_stim_pos=psychopy.visual.TextStim(win=win,
                        name='text',text='stim_pos'+str(stim_pos[frame_2]),pos=(.5,.34),
                        color='white',height=.015)
                    text_mouse_pos=psychopy.visual.TextStim(win=win,
                        name='text',text='stim_pos'+str(mouse_pos[frame_2]),pos=(.5,.30),
                        color='white',height=.015)
                    text_time=psychopy.visual.TextStim(win=win,
                        name='text',text='time'+str(time_track_dur*frame_2/frame_track_end),pos=(.5,.40),
                        color='white',height=.015)
                    # then draw all stimuli
                    fixation.draw()
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
        if current_trial==1 and current_block==1:
            d_block=[current_block]
            d_trial=[current_trial]
            d_cue_dur=[current_cue_dur]
            d_track_dur=[current_track_dur]
            d_time_cue_start=[time_cue_start]
            d_time_cue_end=[time_cue_end]
            d_time_track_start=[time_track_start]
            d_time_track_end=[time_track_end]
            d_time_track_dur=[time_track_dur]
            d_frame_track_end=[frame_track_end]
            d_stim_pos=[stim_pos]
            d_mouse_pos=[mouse_pos]
            d_acc_x=[current_acc_x]
            d_acc_y=[current_acc_y]
            d_acc_rad=[acc_rad]
            d_fourier_acc_rad_x=[fourier_acc_rad_x]
            d_fourier_acc_rad_y=[fourier_acc_rad_y]
            d_fourier_cog_x=[fourier_cog_x]
            d_fourier_cog_y=[fourier_cog_y]
        else:
            d_block.append(current_block)
            d_trial.append(current_trial)
            d_cue_dur.append(current_cue_dur)
            d_track_dur.append(current_track_dur)
            d_time_cue_start.append(time_cue_start)
            d_time_cue_end.append(time_cue_end)
            d_time_track_start.append(time_track_start)
            d_time_track_end.append(time_track_end)
            d_time_track_dur.append(time_track_dur)
            d_frame_track_end.append(frame_track_end)
            d_stim_pos.append(stim_pos)
            d_mouse_pos.append(mouse_pos)
            d_acc_x.append(current_acc_x)
            d_acc_y.append(current_acc_y)
            d_acc_rad.append(acc_rad)
            d_fourier_acc_rad_x.append(fourier_acc_rad_x)
            d_fourier_acc_rad_y.append(fourier_acc_rad_y)
            d_fourier_cog_x.append(fourier_cog_x)
            d_fourier_cog_y.append(fourier_cog_y)
#%% Required clean up
# this cell will make sure that your window displays for a while and then 
# closes properly
core.wait(1)
win.close()
#%% To Do List
# After tracking phase onset, a sudden change in mouse acceleration AFTER stimulus
# starts moving AND after mouse is outside stimulus circle == RT response to stimulus
# moving start. Do we need stim to stay still at end?
## Machine learn mouse acceleration during tracking. If that algorithm can't
# predict tracking, then implied to be mouse accelerating due to object location reset,
# or lack of movement (no attention relayed to tracking).
## RT at beginning of trial serves as how much lag is expected if NO
# contribution of expectation of stimulus.
## Machine learn mouse movement during tracking (how to categorize?) as a function
# of acceleration of stimulus when timeback == 1 (acceleration avg of 1 frame) or more.
## In the end, I don't know what I am measuring but it will be cool.