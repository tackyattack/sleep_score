import matplotlib.pyplot as plt
import numpy as np
import os
import struct

def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

class EDF_file():
    edf_file = ""

    def open_EDF(self, file_name):

        if os.path.exists(file_name):
            self.edf_file = open(file_name, "rb")
        else:
            print("EDF file path does not exist")

    def read_EDF_bytes(self, byte_count):
        buffer = self.edf_file.read(byte_count)
        return buffer

    def parse_header(self):
        # https://www.edfplus.info/specs/edf.html

        # -- upper header parse --
        self.edf_file.seek(0, 0)            # go to beginning
        chunk = self.read_EDF_bytes(256)    # upper header
        self.version = int(chunk[0:8])
        self.patient_ID = str(chunk[8:88])
        self.recording_info = str(chunk[88:168])
        self.startdate = str(chunk[168:176])
        self.starttime = str(chunk[176:184])
        self.header_bytes = int(chunk[184:192])
        self.reserved = str(chunk[192:236])
        self.num_data_records = int(chunk[236:244])
        self.data_record_duration = int(chunk[244:252])
        self.number_signals = int(chunk[252:256])

        # -- lower header parse --
        self.edf_file.seek(256, 0)
        chunk = self.read_EDF_bytes(self.header_bytes - 256)
        self.signal_labels = []
        counter = 0
        for i in range(self.number_signals):
            self.signal_labels.append(chunk[counter:counter+16])
            counter = counter + 16

        self.transducer_types = []
        for i in range(self.number_signals):
            self.transducer_types.append(chunk[counter:counter + 80])
            counter = counter + 80

        self.physical_dimensions = []
        for i in range(self.number_signals):
            self.physical_dimensions.append(chunk[counter:counter + 8])
            counter = counter + 8

        self.physical_minimums = []
        for i in range(self.number_signals):
            self.physical_minimums.append(chunk[counter:counter + 8])
            counter = counter + 8

        self.physical_maximums = []
        for i in range(self.number_signals):
            self.physical_maximums.append(chunk[counter:counter + 8])
            counter = counter + 8

        self.digital_minimums = []
        for i in range(self.number_signals):
            self.digital_minimums.append(chunk[counter:counter + 8])
            counter = counter + 8

        self.digital_maximums  = []
        for i in range(self.number_signals):
            self.digital_maximums.append(chunk[counter:counter + 8])
            counter = counter + 8

        self.prefilterings = []
        for i in range(self.number_signals):
            self.prefilterings.append(chunk[counter:counter + 80])
            counter = counter + 80

        self.samples_per_record = []
        self.signal_offsets = []
        for i in range(self.number_signals):
            sample_cnt = int(chunk[counter:counter + 8])
            self.samples_per_record.append(sample_cnt)
            counter = counter + 8
            if(i > 0):
                self.signal_offsets.append(self.signal_offsets[i-1]+sample_cnt)
            else:
                self.signal_offsets.append(0)

        self.reserved_lower = []
        for i in range(self.number_signals):
            self.reserved_lower.append(chunk[counter:counter + 32])
            counter = counter + 32

        self.data_record_length = 0
        for sample_len in self.samples_per_record:
            self.data_record_length = self.data_record_length + sample_len


    def get_signal_number(self, name):
        for i in range(self.number_signals):
            if name in self.signal_labels[i]:
                return i

    def get_record(self, record_number):
        record_len_bytes = self.data_record_length*2
        file_offset = self.header_bytes + record_len_bytes*(record_number)
        self.edf_file.seek(file_offset, 0)
        return bytearray(self.read_EDF_bytes(record_len_bytes))

    def get_signal_samples(self, offset, size, signal_name):
        signal = []
        signal_number = self.get_signal_number(signal_name)
        ints_left = size
        current_record = offset / self.samples_per_record[signal_number]
        current_offset = offset

        while(ints_left > 0):
            record = self.get_record(current_record)
            signal_offset = self.signal_offsets[signal_number]
            pos = current_offset % self.samples_per_record[signal_number]
            loops = self.samples_per_record[signal_number] - pos
            if(loops > ints_left):
                loops = ints_left

            loops = loops*2 # two bytes per sample
            i = 0
            while(i < loops):
                lo = record[i + pos*2 + signal_offset*2]
                i = i + 1
                hi = record[i + pos*2 + signal_offset*2]
                i = i + 1
                val = (hi << 8) | lo
                if (val & 0x8000):
                    val = -0x10000 + val
                signal.append(val)
                ints_left = ints_left - 1

            current_record = current_record + 1
            current_offset = current_offset + loops/2

        return signal


e = EDF_file()
e.open_EDF("../test_vectors/test_generator_2.edf")
e.parse_header()
samples = e.get_signal_samples(0, 500, "ECG")
#print(samples)

plt.plot(samples)
plt.show()
