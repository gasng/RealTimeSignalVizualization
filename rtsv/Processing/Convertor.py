import os
import numpy as np
import obspy as obs
import struct as st
from dataclasses import dataclass


@dataclass
class ScoutData:
    data: np.array
    block_number: int
    quantum_time: float
    rec_line: int
    rec_picket: int
    components: int
    channel: int
    latitude: float
    longitude: float
    code_adc: float


class ScoutConvertor:
    """
    Ponasenko Svyatoslav
    26 January 2025
    Module-convertor from SCOUT data format to MiniSEED.
    When register makes estimations, it creates one file for each channel.
    """

    @staticmethod
    def _add_avg_with_border(a, avg, border):
        if a < border:
            a = avg + a
        else:
            a = avg + (a - ((border + 1) * 2))
        return a

    @staticmethod
    def _get_coordinates_from_header(header: str) -> (float, float):
        lat, lon = None, None
        for i in range(len(header)):
            if header[i] == 'N':
                lat = ''
                for j in range(2, i + 1):
                    if header[i - j] != ',':
                        lat += header[i - j]
                    else:
                        lat = round(float(lat[::-1]) / 100, 6)  # latitude
                        break

            if header[i] == 'E':
                lon = ''
                for j in range(2, i + 1):
                    if header[i - j] != ',':
                        lon += header[i - j]
                    else:
                        lon = round(float(lon[::-1]) / 100, 6)  # longitude
                        break
        return lat, lon

    @staticmethod
    def _find_head_len(file_set: str):
        start_len = 200
        with open(file_set, 'rb') as f:
            f.read(40)
            header_part = st.unpack(str(start_len) + 's', f.read(start_len))[0][:150]
            finding_str = b'\r\n'
            p1 = header_part.index(finding_str)
            p2 = header_part[p1 + len(finding_str):].index(finding_str)
            result_str = header_part[:p1 + p2 + 2 * len(finding_str)]

            return len(result_str)

    @staticmethod
    def read_scout_file(path: str, file_name: str) -> ScoutData:

        file_set = os.path.join(path, file_name)
        head_len = ScoutConvertor._find_head_len(file_set)  # было 150, 148
        data_all = np.empty(0, dtype=np.int32)  # data array

        with open(file_set, 'rb') as f:
            block_number = st.unpack('i', f.read(4))[0]
            rec_time = st.unpack('i', f.read(4))[0]  # record time in ms
            quantum_time = st.unpack('f', f.read(4))[0]
            code_adc = st.unpack('i', f.read(4))[0]
            f.read(4)
            receiving_line = st.unpack('i', f.read(4))[0]
            rec_picket = st.unpack('i', f.read(4))[0]
            components = st.unpack('i', f.read(4))[0]
            channel = st.unpack('i', f.read(4))[0]
            f.read(4)

            header_part = str(st.unpack(str(head_len) + 's', f.read(head_len))[0])[20:50]
            latitude, longitude = ScoutConvertor._get_coordinates_from_header(header_part)

            for i in range(rec_time // 1000):
                type_comp = st.unpack('b', f.read(1))[0]
                f.read(1)
                data_count = st.unpack('h', f.read(2))[0]
                avg = st.unpack('i', f.read(4))[0]

                if type_comp == 0:
                    data = np.fromfile(f, dtype='b', count=data_count)
                    data = avg + (data - ((data >= 127).astype(np.int32) * 256))
                    data_all = np.concatenate((data_all, data), axis=0)

                elif type_comp == 1:
                    data_shape = data_count + data_count // 2
                    data = np.empty(data_count, dtype=np.int32)
                    b = f.read(data_shape)
                    for k, j in zip(range(0, data_shape, 3), range(0, data_count, 2)):
                        b0, b1, b2 = b[k:k + 3]
                        a2 = ((b2 << 4) & 0b111100000000) + b1
                        a1 = ((b2 << 8) & 0b111100000000) + b0

                        a2 = ScoutConvertor._add_avg_with_border(a2, avg, 2047)
                        a1 = ScoutConvertor._add_avg_with_border(a1, avg, 2047)

                        data[j:j + 2] = a1, a2
                    data_all = np.concatenate((data_all, data))

                elif type_comp == 2:
                    data = np.fromfile(f, dtype=np.int16, count=data_count)
                    data = avg + (data - ((data >= 32767).astype(np.int32) * 65536))
                    data_all = np.concatenate((data_all, data))

                elif type_comp == 3:
                    data = np.empty(data_count, dtype=np.int32)
                    data_shape = data_count * 3
                    b = f.read(data_shape)

                    for k in range(0, data_shape, 3):
                        a3, a2, a1 = ((b[k + j] << (j * 8)) for j in range(3))
                        w = ScoutConvertor._add_avg_with_border((a1 | a2 | a3), avg, 8388607)
                        data[k // 3] = w
                    data_all = np.concatenate((data_all, data))

                else:
                    raise TypeError('bad type {}'.format(file_set))

            return ScoutData(
                data=data_all, block_number=block_number, quantum_time=quantum_time,
                rec_line=receiving_line, rec_picket=rec_picket, components=components,
                channel=channel, latitude=latitude, longitude=longitude, code_adc=code_adc
            )

    @staticmethod
    def _make_time(path: str, file: str) -> obs.UTCDateTime:
        year = int(path[-13:-9])
        month = int(path[-8:-6])
        day = int(path[-5:-3])
        hour = int(path[-2:])
        minutes = int(file[:2])
        seconds = int(file[2:4])
        return obs.UTCDateTime(year, month, day, hour, minutes, seconds)

    @staticmethod
    def scout_to_mseed_hour(path_in: str, path_out: str, stations: dict, network: str):
        all_files = os.listdir(path_in)
        channel_class = {4: 'HHZ', 2: 'HHE', 1: 'HHN'}

        # divide by components
        names_to_comps = {1: [], 2: [], 3: []}
        for file_name in all_files:
            for component in names_to_comps:
                if int(file_name[-5]) == component:
                    names_to_comps[component].append(file_name)
                    break

        # data reading and creations of arrays without bad files
        files_data = []
        for component in names_to_comps:
            files_data.append([])
            for file_name in names_to_comps[component]:
                try:
                    files_data[-1].append(
                        (
                            ScoutConvertor.read_scout_file(path_in, file_name),
                            ScoutConvertor._make_time(path_in, file_name)
                        )
                    )
                except TypeError:
                    files_data.append([])
                    print('Type error!')

        # creation traces and stream
        stream = obs.Stream()
        for trace in files_data:
            if len(trace) != 0:
                main_file = trace[0][0]
                start_time = trace[0][1]
                for j in range(1, len(trace)):
                    main_file.data = np.concatenate((main_file.data, trace[j][0].data), axis=0)

                stats = {'network': network, 'station': stations[main_file.block_number], 'location': '00',
                         'channel': channel_class[main_file.channel], 'npts': len(main_file.data),
                         'delta': main_file.quantum_time, 'starttime': start_time, 'mseed': {'dataquality': 'D'}}
                stream = stream.append(obs.Trace(data=main_file.data, header=stats))

        time_string = ScoutConvertor._make_time(path_in, all_files[0]).datetime.strftime('20%y%m%d_%H%M%S_')
        output_file_name = time_string + stream[0].stats['station']
        stream.write(os.path.join(path_out, output_file_name + '.mseed'), format='MSEED')

    @staticmethod
    def line_scout_to_mseed(path_in, path_out, stations, network):
        for s in os.listdir(path_in):
            station = os.path.join(path_in, s)
            for y in os.listdir(station):
                year = os.path.join(os.path.join(path_in, s), y)
                for m in os.listdir(year):
                    month = os.path.join(os.path.join(os.path.join(path_in, s), y), m)
                    for d in os.listdir(month):
                        day = os.path.join(os.path.join(os.path.join(os.path.join(path_in, s), y), m), d)
                        for h in os.listdir(day):
                            hour = os.path.join(
                                os.path.join(os.path.join(os.path.join(os.path.join(path_in, s), y), m), d), h)
#                             try:
                            ScoutConvertor.scout_to_mseed_hour(hour, path_out, stations, network)
#                             except TypeError:
#                                 print('Error in this time', hour)
