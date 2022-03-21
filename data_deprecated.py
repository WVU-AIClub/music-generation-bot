from mido import MidiFile, Message, MidiTrack
import mido
import numpy as np
import os

def load_midi(midi):
    '''
    Converts midi into a list of notes, where each note it represente as a list [pitch, deltaTime, velocity]

    midi - path to midi file to be converted

    returns 2D array of notes
    '''

    file = MidiFile(midi)
    messages = []
    for message in file:
        if message.type in ['note_on', 'note_off']:
            messages.append(message)

    # print(messages)

    features = []
    deltaTime = 0.0

    for m in messages:
        try:
            deltaTime += m.time
        except:
            pass

        if m.type not in ['note_on']:
            continue

        #Eliminate percussion channel

        features.append([m.note, deltaTime, m.velocity])

        deltaTime = 0.0

    return np.array(features)

def export_midi(features, filename='new_song.mid'):
    '''
    Converts song features to MIDI file and saves to root directory

    features - List of notes where each note is defined as a list [pitch, deltaTime, velocity]
    '''

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    features_expanded = []
    time_from_start = 0

    for n in features:
        time_from_start += n[1] #Add deltaTime to tfs

        features_expanded.append(['note_on', n[0], n[1], n[2], time_from_start])

    curr_time = 0.0
    for m in features_expanded:
        prev_time = curr_time
        curr_time = float(m[4])

        t = curr_time - prev_time
        tempo = mido.bpm2tempo(152)
        t = mido.second2tick(t, 400, tempo) #Seconds, ticks_per_beat, tempo

        # track.append(Message(type=m[0], note=int(round(m[1])), velocity=int(round(m[3])), time=abs(int(round(t)))))
        track.append(Message(type=m[0], note=int(round(m[1])), velocity=int(round(m[3])), time=abs(round(t))))


    mid.save(filename)

def load_data(path):
    '''
    Loads all midi files into memory.

    path - path to directory containing individual midi files - 
           expects direct access to midi files (no subfolders)

    returns 3D array of songs
    '''

    data = []
    for file in os.listdir(path):
        if file.endswith('mid') or file.endswith('midi'):
            data.append(load_midi(file))

        else:
            print("Ignoring unrecognized file")

    
    return np.array(data)

###########
#Test code#
###########

features = load_midi("example.mid")
print(features[0])
export_midi(features)
# print(len(features))

print("done!")

