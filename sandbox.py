from mido import MidiFile, Message
import numpy as np

def parse_midi(midi):
    file = MidiFile(midi)
    messages = []
    for message in file:
        if message.type in ['note_on', 'note_off']:
            messages.append(message)

    # print(messages)

    features = []
    deltaTime = 0

    for m in messages:
        try:
            deltaTime += m.time
        except:
            pass

        if m.type not in ['note_on']:
            continue

        #Eliminate percussion channel

        features.append([m.note, deltaTime, m.velocity])

        deltaTime = 0

    return np.array(features)


features = parse_midi("example.mid")

print(len(features))

