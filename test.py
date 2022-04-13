file = open("Bourdon16.ae0", "rb")

#length in bytes of binary data in ae0 file
length = {
    "aeolus": 7,    #AEOLUS\0
    "check": 2,     #0x02 (02)  << should be one but ... sinon on est décalé
    "blob1": 17,    #0x00 (00)
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

chunk = file.read(length["aeolus"]+length["check"])
try:
    chunk == "AEOLUS\002"
except Exception as e:
    print(chunk)
    raise "This files does not look like a valid aeolus file"

print("File format looks ok")

# get basic infos

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
chunk = file.read(length["copyrite"])
chunk = file.read(length["mnemonic"])
chunk = file.read(length["comments"])

# get curves

chunk = file.read(length["pipe_volume_curve"])
chunk = file.read(length["pipe_tuning_offset_curve"])
chunk = file.read(length["pipe_random_error_curve"])
chunk = file.read(length["pipe_instability_curve"])
chunk = file.read(length["pipe_attack_time_curve"])
chunk = file.read(length["pipe_attack_detune_curve"])
chunk = file.read(length["pipe_decay_time_curve"])
chunk = file.read(length["pipe_decay_detune_curve"])

# get harmonic data

chunk = file.read(length["harmonics_level"])
chunk = file.read(length["harmonics_random"])
chunk = file.read(length["harmonics_attack_time"])
chunk = file.read(length["harmonics_attack_peak"])

