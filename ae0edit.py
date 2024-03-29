#!/usr/bin/python3

import sys
import struct
import getopt, sys
from os.path import exists

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
    "copyright": 56,     #[56] text
    "mnemonic": 8,      #[8] text
    "comments": 56,     #[56] text
    "reserved": 8,      #[8]*0x00
    "volume_curve": 48,
    "tuning_offset_curve": 48,
    "random_error_curve": 48,
    "instability_curve": 48,
    "attack_time_curve": 48,
    "attack_detune_curve": 48,
    "decay_time_curve": 48,
    "decay_detune_curve": 48,
    "harmonics_level": 3072,
    "harmonics_random": 3072,
    "harmonics_attack_time": 3072,
    "harmonics_attack_peak": 3072,    
}

pipe_ranks_text = ["32", "16", "10 2/3", "8", "5 1/3", "4", "2 2/3", "2", "1 3/5", "1 1/3", "1"]
pipe_ranks_fn = [1,1,3,1,3,2,3,4,5,6,8]
pipe_ranks_fd = [4,2,4,1,2,1,1,1,1,1,1]

def get_pipe_rank(fn,fd):
    for i in range(11):
        if ( fn == pipe_ranks_fn [i] and fd == pipe_ranks_fd[i]):
            return pipe_ranks_text[i]
    # print("rank(fn,fd)",fn,fd)
    # return pipe_ranks[fn-1][fd]

# aeolus stop class
#-------------------------

class AeolusStop(object):
    """docstring for AeolusStop"""
    n_harm = 64
    notemin_n0 = 36

    def __init__(self, target):
        # super(AeolusStop, self).__init__()
        self.target = target #manual or pedal
        if (self.target == "manual"):
            self.notemax_n1 = 96 #0x60 (96) manual // 0x43 (67) pedal
        elif (self.target == "pedal"):
            self.notemax_n1 = 67 #0x60 (96) manual // 0x43 (67) pedal
        else:
            raise "AeolusStop type must be either manual or pedal"
        self.rank = "8"
        self.stopname = ""
        self.copyright = ""
        self.mnemonic = ""
        self.comments = ""
        self.volume_curve = ["0","0",0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.tuning_offset_curve = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.random_error_curve = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.instability_curve = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.attack_time_curve = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.attack_detune_curve = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.decay_time_curve = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.decay_detune_curve = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.harmonics_level = 0
        self.harmonics_random = 0
        self.harmonics_attack_time = 0
        self.harmonics_attack_peak= 0

    def load(self, file_path):
        try:
            file = open(file_path, "rb")
        except Exception as e:
            print("could not open",file_path)
            raise e

        #check file format
        #--------------------------

        ae0file = file.read(length["aeolus"])
        if ae0file.decode("utf-8") != "AEOLUS\0":
            print("This files does not look like a valid aeolus file")
            sys.exit(2)

        check = file.read(length["check"])
        if check != b'\x02':
            print("This files does not look like a valid aeolus file")
            sys.exit(2)

        # get basic infos
        #--------------------------

        self.blob1 = file.read(length["blob1"])
        self.n_harm = file.read(length["n_harm"])
        self.blob2 = file.read(length["blob2"])
        self.notemin_n0 = file.read(length["notemin_n0"])
        self.notemax_n1 = file.read(length["notemax_n1"])

        self.piperank_fn = file.read(length["piperank_fn"])
        self.piperank_fd = file.read(length["piperank_fd"])
        self.piperank = get_pipe_rank(int.from_bytes(self.piperank_fn, "big"),int.from_bytes(self.piperank_fd, "big"))

        self.stopname = file.read(length["stopname"]).decode("utf-8")
        self.copyright = file.read(length["copyright"]).decode("utf-8")
        self.mnemonic = file.read(length["mnemonic"]).decode("utf-8")
        self.comments = file.read(length["comments"]).decode("utf-8")
        self.reserved = file.read(length["reserved"])

        # get curves
        #--------------------------

        chunk = file.read(length["volume_curve"])
        [self.volume_curve[0],self.volume_curve[1],self.volume_curve[2],self.volume_curve[3],self.volume_curve[4],self.volume_curve[5],self.volume_curve[6],self.volume_curve[7],self.volume_curve[8],self.volume_curve[9],self.volume_curve[10],self.volume_curve[11],self.volume_curve[12],self.volume_curve[13],self.volume_curve[14]] = struct.unpack('BBBBfffffffffff',chunk)
        chunk = file.read(length["tuning_offset_curve"])
        [self.tuning_offset_curve[0],self.tuning_offset_curve[1],self.tuning_offset_curve[2],self.tuning_offset_curve[3],self.tuning_offset_curve[4],self.tuning_offset_curve[5],self.tuning_offset_curve[6],self.tuning_offset_curve[7],self.tuning_offset_curve[8],self.tuning_offset_curve[9],self.tuning_offset_curve[10],self.tuning_offset_curve[11],self.tuning_offset_curve[12],self.tuning_offset_curve[13],self.tuning_offset_curve[14]] = struct.unpack('BBBBfffffffffff',chunk)
        chunk = file.read(length["random_error_curve"])
        [self.random_error_curve[0],self.random_error_curve[1],self.random_error_curve[2],self.random_error_curve[3],self.random_error_curve[4],self.random_error_curve[5],self.random_error_curve[6],self.random_error_curve[7],self.random_error_curve[8],self.random_error_curve[9],self.random_error_curve[10],self.random_error_curve[11],self.random_error_curve[12],self.random_error_curve[13],self.random_error_curve[14]] = struct.unpack('BBBBfffffffffff',chunk)
        chunk = file.read(length["instability_curve"])
        [self.instability_curve[0],self.instability_curve[1],self.instability_curve[2],self.instability_curve[3],self.instability_curve[4],self.instability_curve[5],self.instability_curve[6],self.instability_curve[7],self.instability_curve[8],self.instability_curve[9],self.instability_curve[10],self.instability_curve[11],self.instability_curve[12],self.instability_curve[13],self.instability_curve[14]] = struct.unpack('BBBBfffffffffff',chunk)
        chunk = file.read(length["attack_time_curve"])
        [self.attack_time_curve[0],self.attack_time_curve[1],self.attack_time_curve[2],self.attack_time_curve[3],self.attack_time_curve[4],self.attack_time_curve[5],self.attack_time_curve[6],self.attack_time_curve[7],self.attack_time_curve[8],self.attack_time_curve[9],self.attack_time_curve[10],self.attack_time_curve[11],self.attack_time_curve[12],self.attack_time_curve[13],self.attack_time_curve[14]] = struct.unpack('BBBBfffffffffff',chunk)
        chunk = file.read(length["attack_detune_curve"])
        [self.attack_detune_curve[0],self.attack_detune_curve[1],self.attack_detune_curve[2],self.attack_detune_curve[3],self.attack_detune_curve[4],self.attack_detune_curve[5],self.attack_detune_curve[6],self.attack_detune_curve[7],self.attack_detune_curve[8],self.attack_detune_curve[9],self.attack_detune_curve[10],self.attack_detune_curve[11],self.attack_detune_curve[12],self.attack_detune_curve[13],self.attack_detune_curve[14]] = struct.unpack('BBBBfffffffffff',chunk)
        chunk = file.read(length["decay_time_curve"])
        [self.decay_time_curve[0],self.decay_time_curve[1],self.decay_time_curve[2],self.decay_time_curve[3],self.decay_time_curve[4],self.decay_time_curve[5],self.decay_time_curve[6],self.decay_time_curve[7],self.decay_time_curve[8],self.decay_time_curve[9],self.decay_time_curve[10],self.decay_time_curve[11],self.decay_time_curve[12],self.decay_time_curve[13],self.decay_time_curve[14]] = struct.unpack('BBBBfffffffffff',chunk)
        chunk = file.read(length["decay_detune_curve"])
        [self.decay_detune_curve[0],self.decay_detune_curve[1],self.decay_detune_curve[2],self.decay_detune_curve[3],self.decay_detune_curve[4],self.decay_detune_curve[5],self.decay_detune_curve[6],self.decay_detune_curve[7],self.decay_detune_curve[8],self.decay_detune_curve[9],self.decay_detune_curve[10],self.decay_detune_curve[11],self.decay_detune_curve[12],self.decay_detune_curve[13],self.decay_detune_curve[14]] = struct.unpack('BBBBfffffffffff',chunk)

        # get harmonic data
        #--------------------------

        self.harmonics_level = file.read(length["harmonics_level"])
        self.harmonics_random = file.read(length["harmonics_random"])
        self.harmonics_attack_time = file.read(length["harmonics_attack_time"])
        self.harmonics_attack_peak = file.read(length["harmonics_attack_peak"])

    def print_curve(self, curve):
        print(curve)
        print(str(getattr(self, curve)))
        print("----")

    def save(self, file_path):
        try:
            file = open(file_path, "wb")
        except Exception as e:
            print("could not open",file_path)
            raise e

        print("Saving curent data to file ",file_path)

        # Write Header

        file.write(bytearray("AEOLUS\0","utf-8"))
        file.write(bytearray('\x02',"utf-8"))
        file.write(bytearray('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',"utf-8"))
        file.write(bytearray('\x40',"utf-8"))
        file.write(bytearray('\x00',"utf-8"))
        file.write(bytearray(self.notemin_n0))
        file.write(bytearray(self.notemax_n1))
        file.write(bytearray(self.piperank_fn))
        file.write(bytearray(self.piperank_fd))

        # Write bloc 1

        if len(self.stopname) != length["stopname"]: print("not good stopname length")
        else: file.write(bytearray(self.stopname,"utf-8"))
        if len(self.copyright) != length["copyright"]: print("not good copyright length")
        else: file.write(bytearray(self.copyright,"utf-8"))
        if len(self.mnemonic) != length["mnemonic"]: print("not good mnemonic length")
        else: file.write(bytearray(self.mnemonic,"utf-8"))
        if len(self.comments) != length["comments"]: print("not good comments length")
        else: file.write(bytearray(self.comments,"utf-8"))

        file.write(bytearray('\x00\x00\x00\x00\x00\x00\x00\x00',"utf-8"))
        
        # write curves data

        mybytes = struct.pack("BBBBfffffffffff",self.volume_curve[0],self.volume_curve[1],self.volume_curve[2],self.volume_curve[3],self.volume_curve[4],self.volume_curve[5],self.volume_curve[6],self.volume_curve[7],self.volume_curve[8],self.volume_curve[9],self.volume_curve[10],self.volume_curve[11],self.volume_curve[12],self.volume_curve[13],self.volume_curve[14])
        if len(mybytes) != length["volume_curve"]: print("not good volume_curve",len(mybytes),length["volume_curve"])
        else: file.write(mybytes)
        mybytes = struct.pack("BBBBfffffffffff",self.tuning_offset_curve[0],self.tuning_offset_curve[1],self.tuning_offset_curve[2],self.tuning_offset_curve[3],self.tuning_offset_curve[4],self.tuning_offset_curve[5],self.tuning_offset_curve[6],self.tuning_offset_curve[7],self.tuning_offset_curve[8],self.tuning_offset_curve[9],self.tuning_offset_curve[10],self.tuning_offset_curve[11],self.tuning_offset_curve[12],self.tuning_offset_curve[13],self.tuning_offset_curve[14])
        if len(mybytes) != length["tuning_offset_curve"]: print("not good tuning_offset_curve",len(mybytes),length["tuning_offset_curve"])
        else: file.write(mybytes)
        mybytes = struct.pack("BBBBfffffffffff",self.random_error_curve[0],self.random_error_curve[1],self.random_error_curve[2],self.random_error_curve[3],self.random_error_curve[4],self.random_error_curve[5],self.random_error_curve[6],self.random_error_curve[7],self.random_error_curve[8],self.random_error_curve[9],self.random_error_curve[10],self.random_error_curve[11],self.random_error_curve[12],self.random_error_curve[13],self.random_error_curve[14])
        if len(mybytes) != length["random_error_curve"]: print("not good random_error_curve",len(mybytes),length["random_error_curve"])
        else: file.write(mybytes)
        mybytes = struct.pack("BBBBfffffffffff",self.instability_curve[0],self.instability_curve[1],self.instability_curve[2],self.instability_curve[3],self.instability_curve[4],self.instability_curve[5],self.instability_curve[6],self.instability_curve[7],self.instability_curve[8],self.instability_curve[9],self.instability_curve[10],self.instability_curve[11],self.instability_curve[12],self.instability_curve[13],self.instability_curve[14])
        if len(mybytes) != length["instability_curve"]: print("not good instability_curve",len(mybytes),length["instability_curve"])
        else: file.write(mybytes)
        mybytes = struct.pack("BBBBfffffffffff",self.attack_time_curve[0],self.attack_time_curve[1],self.attack_time_curve[2],self.attack_time_curve[3],self.attack_time_curve[4],self.attack_time_curve[5],self.attack_time_curve[6],self.attack_time_curve[7],self.attack_time_curve[8],self.attack_time_curve[9],self.attack_time_curve[10],self.attack_time_curve[11],self.attack_time_curve[12],self.attack_time_curve[13],self.attack_time_curve[14])
        if len(mybytes) != length["attack_time_curve"]: print("not good attack_time_curve",len(mybytes),length["attack_time_curve"])
        else: file.write(mybytes)
        mybytes = struct.pack("BBBBfffffffffff",self.attack_detune_curve[0],self.attack_detune_curve[1],self.attack_detune_curve[2],self.attack_detune_curve[3],self.attack_detune_curve[4],self.attack_detune_curve[5],self.attack_detune_curve[6],self.attack_detune_curve[7],self.attack_detune_curve[8],self.attack_detune_curve[9],self.attack_detune_curve[10],self.attack_detune_curve[11],self.attack_detune_curve[12],self.attack_detune_curve[13],self.attack_detune_curve[14])
        if len(mybytes) != length["attack_detune_curve"]: print("not good attack_detune_curve",len(mybytes),length["attack_detune_curve"])
        else: file.write(mybytes)
        mybytes = struct.pack("BBBBfffffffffff",self.decay_time_curve[0],self.decay_time_curve[1],self.decay_time_curve[2],self.decay_time_curve[3],self.decay_time_curve[4],self.decay_time_curve[5],self.decay_time_curve[6],self.decay_time_curve[7],self.decay_time_curve[8],self.decay_time_curve[9],self.decay_time_curve[10],self.decay_time_curve[11],self.decay_time_curve[12],self.decay_time_curve[13],self.decay_time_curve[14])
        if len(mybytes) != length["decay_time_curve"]: print("not good decay_time_curve",len(mybytes),length["decay_time_curve"])
        else: file.write(mybytes)
        mybytes = struct.pack("BBBBfffffffffff",self.decay_detune_curve[0],self.decay_detune_curve[1],self.decay_detune_curve[2],self.decay_detune_curve[3],self.decay_detune_curve[4],self.decay_detune_curve[5],self.decay_detune_curve[6],self.decay_detune_curve[7],self.decay_detune_curve[8],self.decay_detune_curve[9],self.decay_detune_curve[10],self.decay_detune_curve[11],self.decay_detune_curve[12],self.decay_detune_curve[13],self.decay_detune_curve[14])
        if len(mybytes) != length["decay_detune_curve"]: print("not good decay_detune_curve",len(mybytes),length["decay_detune_curve"])
        else: file.write(mybytes)

        # write harmonics data

        file.write(bytearray(self.harmonics_level))
        file.write(bytearray(self.harmonics_random))
        file.write(bytearray(self.harmonics_attack_time))
        file.write(bytearray(self.harmonics_attack_peak))

    def showinfo(self):
        print("--------------------------")
        print("Pipe Rank : " + self.piperank)

        print("Stop Name : " + self.stopname)
        print("copyright : " + self.copyright)
        print("mnemonic : " + self.mnemonic)
        print("comments : " + self.comments)
        print("----")

    def showdata(self):
        self.print_curve("volume_curve")
        self.print_curve("tuning_offset_curve")
        self.print_curve("random_error_curve")
        self.print_curve("instability_curve")
        self.print_curve("attack_time_curve")
        self.print_curve("attack_detune_curve")
        self.print_curve("decay_time_curve")
        self.print_curve("decay_detune_curve")

    def set_volume_curve(self, delta):
        # header bytes correspond to active points on the curve, not in order !!
        # 78 72 66 60 54 48 42 36 / 0 0 0 0 0 96 90 84
        # data is calculated (interpolated) even for inactive points
        # data ranges from max 0 to min -100 float (=dB)

        curve_map = [8,7,6,5,4,3,2,1,11,10,9]
        active_points = [int(n) for n in bin(self.volume_curve[0])[2:].zfill(8)]
        active_points2 = [int(n) for n in bin(self.volume_curve[1])[2:].zfill(3)]
        active_points.extend(active_points2)
        # reorder active points
        active_points_real = [0,0,0,0,0,0,0,0,0,0,0]
        for point in range(11):
            active_points_real[curve_map[point]-1] = active_points[point] 

        # calculate values
        delta = float(delta)
        print("updating volume curve with delta %sdb"%delta)
        print("current volume curve :",self.volume_curve)
        first_point = 99
        current_point = 99
        target_point = 99
        ramp = 0
        for point in range(11):
            # print("calculating point : ",point+1)
            # if active_points_real[point]: print("ACTIVE")
            # print("  current value : ",self.volume_curve[point+4])
            # print("  target value : ","")

            # partir de la gauche
            # trouver le premier point actif (il y en a forcément 1 minimum)
            print("Checking point ",point+1," with value ",active_points_real[point])
            if active_points_real[point] == 0:
                next
            else:
                if first_point == 99: 
                    print("First active point found at position ",point+1)
                    first_point = point
                    current_point = point
                # remplir les éventuelles valeurs à gauche avec la valeur du point + delta
                if (0 < first_point < 11) and (point == first_point):
                    print("  Updating point values's before position ",point+1)
                    for n in range(first_point+1):
                        print("   current point",n+1," value : ",self.volume_curve[point+4-n])
                        #vérifier si valeur actuelle + delta NOT >0
                        temp = (self.volume_curve[point+4-n] + delta)
                        if (temp > 0.0) or (temp < -100.0):
                            sys.exit("***********ERROR your delta is out of range !!!**************")
                        self.volume_curve[point+4-n] = self.volume_curve[point+4-n] + delta
                        print("   updating point",n+1," with value ",self.volume_curve[point+4-n])
                #chercher le point suivant à droite
                elif (0 < first_point < 11) and (0 < current_point < 11):
                    target_point = point
                    #vérifier si valeur actuelle + delta NOT >0
                    temp = self.volume_curve[point+4] + delta
                    if (temp > 0.0) or (temp < -100.0):
                        sys.exit("***********ERROR your delta is out of range !!!**************")
                    # calculer les valeurs intermédiaires
                    step = delta/(target_point-current_point)
                    print("  ramping from point",current_point+1,"to point",target_point+1,"with step",step)
                    for n in range(target_point-current_point):
                        print("    ramping point",current_point+n+2,"from value",self.volume_curve[current_point+4+n+1],"to value",self.volume_curve[current_point+4+n+1]+step)
                        self.volume_curve[current_point+4+n+1] = self.volume_curve[current_point+4+n+1] + step
                    current_point = point
            # remplir les valeurs à droite restantes avec la valeur du dernier point
            if (point == 10) and (target_point < 10):
                print("updating values after point",target_point+1)
                #vérifier si valeur actuelle + delta NOT >0
                temp = self.volume_curve[target_point+4] + delta
                if (temp > 0.0) or (temp < -100.0):
                    sys.exit("***********ERROR your delta is out of range !!!**************")
                for n in range(11-target_point-1):
                    print("   current point",target_point+n+2," value : ",self.volume_curve[target_point+4+n+1])
                    print("   updating point",target_point+n+2," with value ",self.volume_curve[target_point+4],"of target point",target_point+1)
                    self.volume_curve[target_point+4+n+1] = self.volume_curve[target_point+4]
            # s'il n'y avait qu'un seul point en position 1, tout mettre au même niveau après le point
            if (point == 10) and (target_point == 99):
                print("Single point, updating values after point",current_point+1)
                #vérifier si valeur actuelle + delta NOT >0
                temp = self.volume_curve[current_point+4] + delta
                if (temp > 0.0) or (temp < -100.0):
                    sys.exit("***********ERROR your delta is out of range !!!**************")
                for n in range(11-current_point):
                    print("   current point",current_point+n+1," value : ",self.volume_curve[current_point+4+n],"updating with value ",temp)
                    self.volume_curve[current_point+4+n] = temp
                self.volume_curve[current_point+4] = temp
        print("Final volume curve :",self.volume_curve)

    def get_max_volume(self):
        print("Maximum Volume value :",max(self.volume_curve[4:]))


#--------------------------

def usage():
    print(" --Aeolus ae0 file command line manipulator--")
    print("---------------------------------------------")
    print("usage : %s [-h|-i|-p|-s|-m|-v|--volume nn] [file.ae0]"%sys.argv[0])
    print("options :")
    print("  -h, --help : show this help")
    print("  -i, --info : open a .ae0 file and show basic information")
    print("  -p, --print : open a .ae0 file and show contents in structured format")
    print("  -s : saves (OVERWRITE) the changes")
    print("  -m : get maximum volume curve value and print it")
    print("  -v, --volume +/-nn : change global pipe volume -nndB or +nndB")
    print("")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hpismv:", ["help", "print", "info", "volume="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    mystop = AeolusStop("manual")
    save = False
    if opts == []:
        usage()
    # the last argument should be the file to deal with
    if args and args[0] != '-':
        if exists(args[0]):
            print("Opening file ", args[0])
            mystop.load(args[0])
        else:
            print("File %s does not exist"%args[0])
            sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-p", "--print"):
            mystop.showinfo()
            mystop.showdata()
        if o in ("-i", "--info"):
            mystop.showinfo()
        if o in ("-v","--volume"):
            mystop.set_volume_curve(a)
        if o == "-s":
            save = True
        if o == "-m":
            mystop.get_max_volume()
        # else:
        #     assert False, "unhandled option"
    if save:
        mystop.save(args[0])

if __name__ == "__main__":
    main()
