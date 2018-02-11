#-*- coding: utf-8 -*-

"""
Eriksen flanker test
Author of the demo: Krisztina Peres
Date of the first published version: 2012 November 30
Date of the last modification: 3 July 2013

Copyright 2013 Krisztina Peres
Licensed under the MIT License. You may obtain a copy of the License at http://opensource.org/licenses/MIT
"""

#Imports
from psychopy import visual, core, gui,event
import random

# Language specific components
def _(string):
    # You should use texts dictionary to strore the strings, and set exp_info['language'] to specify the language
    return texts[string][exp_info['language']]

texts = {
    'instr':
        {'en':"In the following task you will see letters. You have to pay attention only to the middle letter.\n\nIf this letter is 'S' or 'M', press key '1'!\nIf the middle letter is 'P' or 'H', press key '9'!",
        'hu':u"A következő feladatban egy-egy betűsort fogsz látni. A betűsorból csak a középső betűre kell figyelned.\n\nHa a középső betű 'S' vagy 'M', nyomd meg az '1'-es billentyűt!\nHa a középső betű 'P' vagy 'H', a 9-es billentyűd nyomd meg!"},
}


exp_info = {'participant':'participant_ID',
    'language': texts.values()[0].keys()} # default parameters of the experiment

# Setting some parameters on GUI
dlg = gui.DlgFromDict(exp_info, title='Eriksen flanker test',
   order = ['participant', 'language'],
    tip = {'participant':'Identifier of the participant.',
        'language':'Language of the instructions.',})
if not dlg.OK:
    print 'User Cancelled'
    core.quit()

#log file
file_name = exp_info['participant']+'_eriksen.csv'

log_file = open(file_name, 'a')# a simple text file with 'comma-separated-values'
log_file.write('participant, condition, stimulus, response, RT, error\n')

#create window and stimuli
win = visual.Window([1366,768],allowGUI=True, fullscr=False, waitBlanking=True, monitor='testMonitor', units='deg')
trial_clock=core.Clock()

#stimuli
instruction = visual.TextStim(win, pos=[0,2], wrapWidth=30, text=_('instr'))
fix_cross = visual.TextStim(win, text="+", pos=(0,0), height=1, color='black')
word_text = visual.TextStim(win, pos=(0,0))
letterlist=list('SMPH')
arrow = visual.ShapeStim(win, lineColor='black', lineWidth=2.0, fillColor='black', vertices=((-0.05,-0.2), (0.05, -0.2), (0.05, 0.0), (0.1, 0.0), (0, 0.2), (-0.1, 0), (-0.05, 0)), closeShape=True, pos= [0,-1], interpolate=True)

#experiment
instruction.draw()
win.flip()
event.waitKeys()

conditions = ['congruent']*20 + ['stim_incong']*10 + ['resp_incong']*10
random.shuffle(conditions)

for condition in conditions:
    # generate stimuli
    mid=random.randint(0,3) # mid=middle letter
    # flank: letters next to the middle letter (neighbour letters)
    if condition == 'congruent':# 50% of the stimuli are identical letters
        flank = mid
    elif condition == 'stim_incong': # 25% of the different letters belong to the same response group as the middle letter
        if mid==0:
            flank=1
        elif mid==1:
            flank=0
        elif mid==2:
            flank=3
        elif mid==3:
            flank=2
    elif condition == 'resp_incong': # 25% of the different letters belong to the other response group relative to the middle letter
        if mid in [0,1]:
            flank=random.randint(2,3)
        elif mid in [2,3]:
            flank=random.randint(0,1)

    text=letterlist[flank]*2 + letterlist[mid] + letterlist[flank]*2 # generated stimuli
    fix_cross.draw()
    win.flip()
    core.wait(0.2)
    word_text.setText(text)
    word_text.draw()
    arrow.draw() # indicates the target (middle) letter
    win.flip()
    trial_clock.reset()
    core.wait(0.3)
    win.flip()
    
    response=event.waitKeys()[0]
    rt = trial_clock.getTime() # store reaction time
    if response=='escape': # stops experiment if esc is pressed
        core.quit()
    correct_response = '1' if letterlist[mid] in ['S', 'M'] else '9'
    log_file.write('%s, %s,%s,%s,%s,%d\n' %(exp_info['participant'], condition, text, response, rt, correct_response!=response))
    win.flip()
    core.wait(0.5)
log_file.close()

# Analyze data
analyze_log.analyze_log (filename=file_name, 
                         indep_var='condition', dep_var='RT', function='median', filt_cond = '$error$==0',
                         graph_types=['boxplot', 'bar'])
