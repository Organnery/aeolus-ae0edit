#!/usr/bin/python3

import sys
import struct

# open file
#--------------------------

try:
    file = open(sys.argv[1], "rb")
except Exception as e:
    print("GIVE A FILENAME AS ARG1")
    raise e

#length in bytes of binary data in ae0 file
length = {
    "aeolus": 7,    #AEOLUS\0
    "check": 1,     #0x02 (02)
    "blob1": 18,    #0x00 (00)
    "n_harm": 1,    #0x40 (64)
    "blob2": 1,     #0x00 (00)
    "notemin_n0": 1,     #0x24 (36)
    "notemax_n1": 1,     #0x60 (96) manual // 0x43 (67) pedal
    "piperank_fn": 1,    #refer to table, based on pipe rank
    "piperank_fd": 1,    #refer to table, based on pipe rank
    "stopname": 32,     #[32] text
    "copyrite": 56,     #[56] text
    "mnemonic": 8,      #[8] text
    "comments": 56,     #[56] text
    "reserved": 8,      #[8]*0x00
    "pipe_volume_curve": 48,
    "pipe_tuning_offset_curve": 48,
    "pipe_random_error_curve": 48,
    "pipe_instability_curve": 48,
    "pipe_attack_time_curve": 48,
    "pipe_attack_detune_curve": 48,
    "pipe_decay_time_curve": 48,
    "pipe_decay_detune_curve": 48,
    "harmonics_level": 3072,
    "harmonics_random": 3072,
    "harmonics_attack_time": 3072,
    "harmonics_attack_peak": 3072,    
}

pipe_ranks = [
    ["8","16",0,"32"],
    ["4"],
    ["2 2/3"],
    ["2 2/3","5 1/3",0,"10 2/3"],
    ["2"],
    ["1 3/5"],
    ["1 1/3"],
    [0],
    ["1"]
]

def get_pipe_ranks(fn,fd):
    return pipe_ranks[fn-1][fd-1]

#check file format
#--------------------------

chunk = file.read(length["aeolus"])
if chunk.decode("utf-8") == "AEOLUS\0":
    print("AEOLUS format found")
else:
    raise "This files does not look like a valid aeolus file"

chunk = file.read(length["check"])
if chunk == b'\x02':
    print("Check found")
else:
    raise "This files does not look like a valid aeolus file"

# get basic infos
#--------------------------

print("--------------------------")
chunk = file.read(length["blob1"])
chunk = file.read(length["n_harm"])
chunk = file.read(length["blob2"])
chunk = file.read(length["notemin_n0"])
chunk = file.read(length["notemax_n1"])

piperank_fn = file.read(length["piperank_fn"])
piperank_fd = file.read(length["piperank_fd"])
piperank = get_pipe_ranks(int.from_bytes(piperank_fn, "big"),int.from_bytes(piperank_fd, "big"))
print("Pipe Rank : " + piperank)

stopname = file.read(length["stopname"]).decode("utf-8")
print("Stop Name : " + stopname)
copyrite = file.read(length["copyrite"]).decode("utf-8")
print("copyright : " + copyrite)
mnemonic = file.read(length["mnemonic"]).decode("utf-8")
print("mnemonic : " + mnemonic)
comments = file.read(length["comments"]).decode("utf-8")
print("comments : " + comments)
chunk = file.read(length["reserved"])
print("----")

# get curves
#--------------------------

# header bytes correspond to active points on the curve, not in order !!
# 78 72 66 60 54 48 42 36 / 0 0 0 0 0 96 90 84
# data is calculated (interpolated) even for inactive points

chunk = file.read(length["pipe_volume_curve"])
pipe_volume_curve = list(chunk)
print("Pipe volume curve :")
volume_curve = [0,0,0,0,0,0,0,0,0,0,0]
[vc1,vc2,vc3,vc4,volume_curve[0],volume_curve[1],volume_curve[2],volume_curve[3],volume_curve[4],volume_curve[5],volume_curve[6],volume_curve[7],volume_curve[8],volume_curve[9],volume_curve[10]] = struct.unpack('bbbbfffffffffff',chunk)
print(volume_curve)
print( "With header :", '{0:08b}'.format(vc1),'{0:08b}'.format(vc2),vc3,vc4)
print("----")

chunk = file.read(length["pipe_tuning_offset_curve"])
pipe_tuning_offset_curve = list(chunk)
print("Pipe tuning offset curve :")
tuning_offset_curve = [0,0,0,0,0,0,0,0,0,0,0]
[toc1,toc2,toc3,toc4,tuning_offset_curve[0],tuning_offset_curve[1],tuning_offset_curve[2],tuning_offset_curve[3],tuning_offset_curve[4],tuning_offset_curve[5],tuning_offset_curve[6],tuning_offset_curve[7],tuning_offset_curve[8],tuning_offset_curve[9],tuning_offset_curve[10]] = struct.unpack('bbbbfffffffffff',chunk)
print(tuning_offset_curve)
print( "With header :", '{0:08b}'.format(toc1),'{0:08b}'.format(toc2),toc3,toc4)
print("----")

chunk = file.read(length["pipe_random_error_curve"])
pipe_random_error_curve = list(chunk)
print("Pipe random error curve :")
random_error_curve = [0,0,0,0,0,0,0,0,0,0,0]
[rec1,rec2,rec3,rec4,random_error_curve[0],random_error_curve[1],random_error_curve[2],random_error_curve[3],random_error_curve[4],random_error_curve[5],random_error_curve[6],random_error_curve[7],random_error_curve[8],random_error_curve[9],random_error_curve[10]] = struct.unpack('bbbbfffffffffff',chunk)
print(random_error_curve)
print( "With header :", '{0:08b}'.format(rec1),'{0:08b}'.format(rec2),rec3,rec4)
print("----")

chunk = file.read(length["pipe_instability_curve"])
pipe_instability_curve = list(chunk)
print("Pipe instability curve :")
instability_curve = [0,0,0,0,0,0,0,0,0,0,0]
[ic1,ic2,ic3,ic4,instability_curve[0],instability_curve[1],instability_curve[2],instability_curve[3],instability_curve[4],instability_curve[5],instability_curve[6],instability_curve[7],instability_curve[8],instability_curve[9],instability_curve[10]] = struct.unpack('bbbbfffffffffff',chunk)
print(instability_curve)
print( "With header :", '{0:08b}'.format(ic1),'{0:08b}'.format(ic2),ic3,ic4)
print("----")

chunk = file.read(length["pipe_attack_time_curve"])
pipe_attack_time_curve = list(chunk)
print("Pipe attack time curve :")
attack_time_curve = [0,0,0,0,0,0,0,0,0,0,0]
[at1,at2,at3,at4,attack_time_curve[0],attack_time_curve[1],attack_time_curve[2],attack_time_curve[3],attack_time_curve[4],attack_time_curve[5],attack_time_curve[6],attack_time_curve[7],attack_time_curve[8],attack_time_curve[9],attack_time_curve[10]] = struct.unpack('bbbbfffffffffff',chunk)
print(attack_time_curve)
print( "With header :", '{0:08b}'.format(at1),'{0:08b}'.format(at2),at3,at4)
print("----")

chunk = file.read(length["pipe_attack_detune_curve"])
pipe_attack_detune_curve = list(chunk)
print("Pipe attack detune curve :")
attack_detune_curve = [0,0,0,0,0,0,0,0,0,0,0]
[ad1,ad2,ad3,ad4,attack_detune_curve[0],attack_detune_curve[1],attack_detune_curve[2],attack_detune_curve[3],attack_detune_curve[4],attack_detune_curve[5],attack_detune_curve[6],attack_detune_curve[7],attack_detune_curve[8],attack_detune_curve[9],attack_detune_curve[10]] = struct.unpack('bbbbfffffffffff',chunk)
print(attack_detune_curve)
print( "With header :", '{0:08b}'.format(ad1),'{0:08b}'.format(ad2),ad3,ad4)
print("----")

chunk = file.read(length["pipe_decay_time_curve"])
pipe_decay_time_curve = list(chunk)
print("Pipe decay time curve :")
decay_time_curve = [0,0,0,0,0,0,0,0,0,0,0]
[dt1,dt2,dt3,dt4,decay_time_curve[0],decay_time_curve[1],decay_time_curve[2],decay_time_curve[3],decay_time_curve[4],decay_time_curve[5],decay_time_curve[6],decay_time_curve[7],decay_time_curve[8],decay_time_curve[9],decay_time_curve[10]] = struct.unpack('bbbbfffffffffff',chunk)
print(decay_time_curve)
print( "With header :", '{0:08b}'.format(dt1),'{0:08b}'.format(dt2),dt3,dt4)
print("----")

chunk = file.read(length["pipe_decay_detune_curve"])
pipe_decay_detune_curve = list(chunk)
print("Pipe decay detune curve :")
decay_detune_curve = [0,0,0,0,0,0,0,0,0,0,0]
[dd1,dd2,dd3,dd4,decay_detune_curve[0],decay_detune_curve[1],decay_detune_curve[2],decay_detune_curve[3],decay_detune_curve[4],decay_detune_curve[5],decay_detune_curve[6],decay_detune_curve[7],decay_detune_curve[8],decay_detune_curve[9],decay_detune_curve[10]] = struct.unpack('bbbbfffffffffff',chunk)
print(decay_detune_curve)
print( "With header :", '{0:08b}'.format(dd1),'{0:08b}'.format(dd2),dd3,dd4)
print("----")

# get harmonic data
#--------------------------

harmonics_level = file.read(length["harmonics_level"])
harmonics_random = file.read(length["harmonics_random"])
harmonics_attack_time = file.read(length["harmonics_attack_time"])
harmonics_attack_peak = file.read(length["harmonics_attack_peak"])

# check if we have something to do

if sys.argv[2] == "+3" :
    print("going +3")
else:
    print("nothing more")

# pour calculer l'interpolation
# partir de la gauche ?
# trouver le premier point actif (il y en a forcément 1 minimum)
    # remplir les valeurs à gauche éventuelles avec la valeur du point
    # tant qu'on est pas arrivé au dernier point
        #chercher le point suivant à droite
            #si décalage > 1
                # calculer les valeurs intermédiaires
    # remplir les valeurs à droite restantes avec la valeur du dernier point
