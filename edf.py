import matplotlib.pyplot as plt
import numpy as np
import os

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
        for i in range(self.number_signals):
            self.samples_per_record.append(int(chunk[counter:counter + 8]))
            counter = counter + 8

        self.reserved_lower = []
        for i in range(self.number_signals):
            self.reserved_lower.append(chunk[counter:counter + 32])
            counter = counter + 32

        self.data_record_length = 0
        for sample_len in self.samples_per_record:
            self.data_record_length = self.data_record_length + sample_len


    def get_record(self, record_number):
        file_offset = self.header_bytes + self.data_record_length*(record_number - 1)
        self.edf_file.seek(file_offset, 0)
        return self.read_EDF_bytes(self.data_record_length)

    def get_sample(self, signal_name, record_number):


e = EDF_file()
e.open_EDF("../test_vectors/test_generator_2.edf")
e.parse_header()
print(e.get_record(1))

# t = np.arange(0.0, 2.0, 0.01)
# s = 1 + np.sin(2 * np.pi * t)
# plt.plot(t, s)
#
# plt.xlabel('time (s)')
# plt.ylabel('voltage (mV)')
# plt.title('About as simple as it gets, folks')
# plt.grid(True)
# plt.savefig("test.png")
# plt.show()
