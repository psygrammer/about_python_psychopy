# -*- coding: utf-8 -*-

"""
Go/No-go
Author of the demo: Krisztina Peres
Date of the last modification: 2013 June

Copyright 2013 Krisztina Peres
Licensed under the MIT License. You may obtain a copy of the License at http://opensource.org/licenses/MIT
"""

# Imports
from psychopy import visual, core, event, gui
import random
#, analyze_log

# Language specific components
def _(string):
    # You should use texts dictionary to strore the strings, and set exp_info['language'] to specify the language
    return texts[string][exp_info['language']]
texts = {
    'instr':
        {'en':"In the following task you will see a green and a blue circle.\n\nYou have to press key 'space' just in the case, when you see the green circle.\nDon't do anything, when you see the blue circle!",
        'hu':u"A következő feladatban egy zöld és egy kék színű kört fogsz látni.\n\nCsak abban az esetben nyomd meg a 'space' billentyűt, ha a zöld kört lárod! Ne csinálj semmit, ha a kék kört látod!"},
}

exp_info = {'participant':'participant_ID',
    'language': texts.values()[0].keys()} # default parameters of the experiment

# Setting some parameters on GUI
dlg = gui.DlgFromDict(exp_info, title='Go-Nogo',
   order = ['participant', 'language'],
    tip = {'participant':'Identifier of the participant.',
        'language':'Language of the instructions.',})
if not dlg.OK:
    print 'User Cancelled'
    core.quit()

win = visual.Window([1366,768], allowGUI=True, fullscr=False, waitBlanking=True, monitor='testMonitor', units='deg') # Create window

# Open log file to write
file_name = exp_info['participant']+'_go_nogo.csv'

log_file = open(file_name, 'a')
log_file.write('participant, color, response, RT, error\n') # Heading

# Instruction
text_instruction = visual.TextStim(win, wrapWidth= 30, pos=[0,0], text=_('instr')) # Text object
text_instruction.draw()
win.flip() # draw the instruction
event.waitKeys() # wait for key press to continue

# Experiment
fix_cross = visual.TextStim(win, text="+", pos=(0,0), height=1, color='black')
stimulus = visual.Circle(win, radius=2, edges=32)
trial_clock = core.Clock() # Clock for measuring response time

core.wait(0.5)

stimuli = ['green', 'blue']*10
random.shuffle(stimuli)

for color_stim in stimuli:
    fix_cross.draw()
    win.flip()
    core.wait(0.2)

    stimulus.setFillColor(color_stim)
    stimulus.setLineColor(color_stim)
    stimulus.draw()
    win.flip()
    trial_clock.reset()
    keylist=event.waitKeys(maxWait=0.7)
    if keylist is not None:
        response=keylist[0]
        if response=='escape': # stops experiment if esc is pressed
            core.quit()
        else:
            rt = trial_clock.getTime() # store reaction time
            error = 0 if color_stim=='green' else 1
    else:
        response='none'
        rt=-1
        error = 1 if color_stim=='green' else 0
    
    win.flip()
    core.wait(0.3)
    log_file.write('%s, %s, %s, %.4f, %s\n' %(exp_info['participant'],color_stim, response, rt, error))

log_file.close()

#analyze_log.analyze_log (filename=file_name, 
#                         indep_var='color', dep_var='error', function='mean',
#                         graph_types=['bar'])
