# -*- coding: utf-8 -*-
# Delete the unnecessary parts of this template before publishing the script
"""
Attentional blink paradigm
Author of the demo: Gábor Lengyel
Date of the last modification: 2013 June 28

Copyright 2013 Gábor Lengyel
Licensed under the MIT License. You may obtain a copy of the License at http://opensource.org/licenses/MIT
"""

# Imports
from psychopy import visual, core, event, gui
#import analyze_log, 
import random

# Language specific components
def _(string):
    # You should use texts dictionary to strore the strings, and set exp_info['language'] to specify the language
    return texts[string][exp_info['language']]
texts = {
    'instr_experimental_condition':
        {'en':'In the following task you will see black colored numbers appearing on the display rapidly after each other. You have two tasks. First you have to detect a white letter and remember what letter it was. Second, you have to decide whether there was a black X among the letters. When all letters were presented you have to type what letter was the white one, then you have to press the "right arrow key" if there was a black X and press "left arrow key" if there was no black X. Press any key to continue.',
        'hu':u'A következőkben fekete betűket fogsz látni a képernyőn. A betűk gyorsan egymás után jelennek majd meg. Két feladatod lesz. A fekete betűk között lesz egy fehér is, és azt kell majd megmondanod, milyen betű volt a fehér betű. Aztán azt kell eldöntened, hogy látál-e feket X-et a betűk között. A betűk felvillanása le kell nyomnod azt a betűt, amilyen a fehér betű volt, majd amennyiben láttál fekete X-et nyomgd meg az "jobb kurzormozgató nyílat" gombot, ha nem láttál fekete X-et nyomd meg az "bal kurzormozgató nyílat" gombot. Nyomj egy gombot, ha kezdhetjük.'},
    'instr_control_condition':
        {'en':'In the following task you will see black colored numbers appearing on the display rapidly after each other. You have to decide whether there was a black X among the letters. After the letters you have to push "right arrow key" if there was a black X among the letters and push "left arrow key" if there was no black X. Press any key to continue.',
        'hu':u'A következőkben fekete betűket fogsz látni a képernyőn. A betűk gyorsan egymás után jelennek majd meg. Azt kell eldöntened, hogy látál-e feket X-et a betűk között. A betűk felvillanása után, amennyiben láttál fekete X-et nyomgd meg az "jobb kurzormozgató nyílat" gombot, ha nem láttál fekete X-et nyomd meg az "bal kurzormozgató nyílat" gombot. Nyomj egy gombot, ha kezdhetjük.'},
    'instr_response_target_1':
        {'en':'Please press the button that you think the white letter was.',
        'hu':u'Nyomd meg azt a billentyűt a billyentyűzeten, amilyen szerinted fehér betű volt'},
    'instr_response_target_2':
        {'en':'Please press "right arrow key" if there was an X in the letter stream, and press "left arrow key" if there was no X.',
        'hu':u'Nyomd meg a "jobb kurzormozgató nyílat", amennyiben láttál X-t a betűk között, ha nem láttál nyomd meg az "bal kurzormozgató nyílat"'},
}

exp_info = {'participant':'participant_ID',
    'language': texts.values()[0].keys(),
    'experiment':['experimental_condition', 'control_condition'],}

# Setting some parameters on GUI
dlg = gui.DlgFromDict(exp_info, title='exp_title',
   order = ['participant', 'language', 'experiment'],
    tip = {'participant':'Identifier of the participant.',
        'language':'Language of the instructions.',
        'experiment':'Experimental or control condition of the experiment'})
if not dlg.OK:
    print 'User Cancelled'
    core.quit()

# Stimuli
available_letters = map(chr, range(65, 91)) # letters of the English alphabet in uppercase
del available_letters [23] # removing X from the alphabet
random.shuffle(available_letters) # Randomize list

win = visual.Window([1200,600], allowGUI=True, fullscr=False, waitBlanking=True, monitor='testMonitor', units='pix') # Create window

# Open log file to write
file_name = exp_info['participant']+'_attention.csv'

log_file = open(file_name, 'a')
if exp_info['experiment']=='experimental_condition':
    log_file.write('participant, condition, white_letter, x_position, response_white_letter, response_x, RT_1, RT_2\n') # Heading
else:
    log_file.write('participant, condition, white_letter, x_position, response_x, RT_2\n') # Heading

# Instruction
if exp_info['experiment']=='experimental_condition':
    text_instruction = visual.TextStim(win, pos=[0,0], text=_('instr_experimental_condition'))
else:
    text_instruction = visual.TextStim(win, pos=[0,0], text=_('instr_control_condition'))
text_instruction.draw()
win.flip() # draw the instruction
event.waitKeys() # wait for key press to continue

# Experiment
letter_text = visual.TextStim(win, height=50, pos=[0,0], color = 'black')

#random factor

x_positions = [0]*16 + range(1,9)*5
random.shuffle(x_positions) # Randomize list

trial_clock = core.Clock()

fixation_duration=0.18
letter_duration=0.015
interstimulus_duration=0.075
    
for x_position in x_positions: # 10 blocks will be presented

    # Generate letter stream with colors
    letter_stream = available_letters [0: random.randrange(16, 24)] #getting the first 7-15 (random) elements of the letter stream
    colors = ['black']*len(letter_stream)
    colors[-9] = 'white'
    if x_position:
        letter_stream[-x_position] = 'X'
    print x_position, zip(letter_stream, colors)
    
    letter_text.setText('+')
    letter_text.draw()
    win.flip()
    core.wait(fixation_duration)
    for letter, color in zip(letter_stream, colors):
        letter_text.setText(letter)
        letter_text.setColor(color)
        letter_text.draw()
        win.flip()
        core.wait(letter_duration)
        win.flip()
        core.wait(interstimulus_duration)
    
    if exp_info['experiment']=='experimental_condition':
        text_instruction = visual.TextStim(win, pos=[0,0], text=_('instr_response_target_1')) # text for the answer
        text_instruction.draw()
        win.flip() # draw the instruction
        trial_clock.reset()
        response_1=event.waitKeys()[0]
        RT_1 = trial_clock.getTime()
        if response_1=='escape':
            print 'Experiment interrupted'
            core.quit()
    
    text_instruction = visual.TextStim(win, pos=[0,0], text=_('instr_response_target_2')) #text for the answer
    text_instruction.draw()
    win.flip() # draw the instruction
    trial_clock.reset()
    response_2=event.waitKeys()[0]
    RT_2= trial_clock.getTime()
    if response_2=='escape':
        print 'Experiment interrupted'
        core.quit()
    
    response_x = 1 if response_2 == 'right' else 0
    position_x = 0 if x_position <0 else x_position
    
    if exp_info['experiment']=='experimental_condition':           
        log_file.write('"%s", "%s", %s, %d, %s, %d, %.4f, %.4f\n' %(exp_info['participant'],exp_info['experiment'], letter_stream[-9], position_x, response_1, response_x, RT_1, RT_2))
    else:                   
        log_file.write('"%s", "%s", %s, %d, %d, %.4f\n' %(exp_info['participant'],exp_info['experiment'], letter_stream[-9], position_x, response_x, RT_2))
    
    event.clearEvents()
    win.flip() # show a clean window
    core.wait(0.5) # ITI

log_file.close()

# Analyze data
#analyze_log.analyze_log (filename=file_name,
#                         indep_var='x_position', dep_var='response_x', function='mean', 
#                         graph_types=['line'])
