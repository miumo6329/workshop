from pydub import AudioSegment

tones = {}
for string in range(1, 7):
    for flet in range(0, 5):
        tone = AudioSegment.from_mp3("mp3/tone_"+str(string)+"-"+str(flet)+".mp3")
        tone = tone - 5
        tones[str(string)+"-"+str(flet)] = tone

print("complete load mp3.")

code_g_maj = [tones["6-3"], tones["5-2"], tones["4-0"], tones["3-0"], tones["2-0"], tones["1-3"]]
code_c_maj = [tones["5-3"], tones["4-2"], tones["3-0"], tones["2-1"], tones["1-0"]]
code_d_maj = [tones["4-0"], tones["3-2"], tones["2-3"], tones["1-2"]]
code_ds_dim = [tones["4-1"], tones["3-2"], tones["2-1"], tones["1-2"]]
code_e_min7 = [tones["6-0"], tones["5-2"], tones["4-0"], tones["3-0"], tones["2-0"], tones["1-0"]]

down = 0
up = 1
slur = 2
mute = 3

stroke_pattern_a = [down, slur, slur, slur,
                    slur, slur, up, slur,
                    slur, slur, up, slur,
                    down, slur, up, slur]

stroke_pattern_b = [down, up, down, up,
                    down, mute, mute, mute,
                    mute, mute, up, mute,
                    mute, mute, up, slur]

stroke_pattern_c = [down, slur, slur, slur,
                    down, slur, slur, slur,
                    down, slur, slur, slur,
                    slur, slur, up, slur]

stroke_pattern = stroke_pattern_c + \
                 stroke_pattern_c + \
                 stroke_pattern_c + \
                 stroke_pattern_c

score = [code_g_maj for i in range(16)] + \
        [code_c_maj for i in range(16)] + \
        [code_d_maj for i in range(8)] + \
        [code_ds_dim for i in range(8)] + \
        [code_e_min7 for i in range(16)]


def down_stroke(tones, interval):
    base = AudioSegment.silent(duration=10*1000)  # 10sec
    cord = base
    for i, tone in enumerate(tones):
        cord = cord.overlay(tone, i*interval)
    return cord


def up_stroke(tones, interval):
    base = AudioSegment.silent(duration=10*1000)  # 10sec
    cord = base
    for i, tone in enumerate(reversed(tones)):
        cord = cord.overlay(tone, i*interval)
    return cord


bpm = 180
note_quarter = ((60 / bpm) * 1000)  # bpmに対する4分音符のmsec
note_16nd = note_quarter / 4  # 16分音符のmsec

stroke_interval = 5  # msec


base = AudioSegment.silent(duration=0)
now_cord = AudioSegment.silent(duration=0)
length = 0
# for pattern, cord in zip(stroke_pattern, score):
#     if pattern == down:
#         base += now_cord[:length]
#         now_cord = down_stroke(cord, stroke_interval)
#         length = note_16nd
#     elif pattern == up:
#         base += now_cord[:length]
#         now_cord = up_stroke(cord, stroke_interval)
#         length = note_16nd
#     elif pattern == slur:
#         length += note_16nd
#     elif pattern == mute:
#         base += now_cord[:length]
#         now_cord = AudioSegment.silent(duration=10*1000)  # 10sec
#         length = note_16nd

margin = 5
base = AudioSegment.silent(duration=margin)
now_cord = AudioSegment.silent(duration=margin)
for pattern, cord in zip(stroke_pattern, score):
    if pattern == down:
        now_cord = now_cord[:length+margin]
        base = base.append(now_cord, crossfade=margin)
        now_cord = down_stroke(cord, stroke_interval)
        length = note_16nd
    elif pattern == up:
        now_cord = now_cord[:length+margin]
        base = base.append(now_cord, crossfade=margin)
        now_cord = up_stroke(cord, stroke_interval)
        length = note_16nd
    elif pattern == slur:
        length += note_16nd
    elif pattern == mute:
        now_cord = now_cord[:length+margin]
        base = base.append(now_cord, crossfade=margin)
        now_cord = AudioSegment.silent(duration=10*1000)  # 10sec
        length = note_16nd

base += now_cord[:length]
base.export("sound.mp3", format="mp3")
print(len(base))

