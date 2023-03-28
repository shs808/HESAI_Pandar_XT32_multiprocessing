'''
* ***********************************************************************************************
* @author	  ChangMin An
* @prof       YoungKeun Kim
* @Mod		  2023 - 03 - 08
* @brief	  HESAI Pandar XT32 Acquirement Point Cloud Data
* @Version	  Python 3.8
* ***********************************************************************************************
'''
import socket
import time
import traceback
import numpy as np
from multiprocessing import Process, Pipe
import matplotlib.pyplot as plt

# ============= HESAI Pandar XT-32 Specification ============= #
HOST = "192.168.1.201"
PORT = 2368
DISTANCE_RESOLUTION = 0.004
AZIMUTH_UNIT = 0.01
V_ANGLE_GLB = np.arange(127999,-1,-1) % 32 - 16

# Reflectivity Mapping(0~255 -> %)
REFLECT_MAP = {
    0:0.0, 1:2.89, 2:4.08, 3:5.0, 4:5.77, 5:6.45, 6:7.07, 7:7.64, 8:8.16, 9:8.66, 10:9.13,
    11:9.57, 12:10.0, 13:10.41, 14:10.8, 15:11.18, 16:11.55, 17:11.9, 18:12.25, 19:12.58, 20:12.91,
    21:13.23, 22:13.54, 23:13.84, 24:14.14, 25:14.43, 26:14.72, 27:15.0, 28:15.28, 29:15.57, 30:15.86,
    31:16.16, 32:16.46, 33:16.77, 34:17.09, 35:17.42, 36:17.75, 37:18.1, 38:18.45, 39:18.82, 40:19.2,
    41:19.59, 42:20.0, 43:20.43, 44:20.87, 45:21.34, 46:21.84, 47:22.36, 48:22.93, 49:23.55, 50:24.23,
    51:25.0, 52:25.92, 53:27.09, 54:28.22, 55:29.35, 56:30.47, 57:31.6, 58:32.73, 59:33.86, 60:34.99,
    61:36.12, 62:37.25, 63:38.37, 64:39.5, 65:40.63, 66:41.76, 67:42.89, 68:44.02, 69:45.15, 70:46.28,
    71:47.4, 72:48.53, 73:49.66, 74:50.79, 75:51.92, 76:53.05, 77:54.18, 78:55.3, 79:56.43, 80:57.56,
    81:58.69, 82:59.82, 83:60.95, 84:62.08, 85:63.21, 86:64.33, 87:65.46, 88:66.59, 89:67.72, 90:68.85,
    91:69.98, 92:71.11, 93:72.23, 94:73.36, 95:74.49, 96:75.62, 97:76.65, 98:77.88, 99:79.01, 100:80.14,
    101:81.26, 102:82.39, 103:83.52, 104:84.65, 105:85.78, 106:86.91, 107:88.04, 108:89.16, 109:90.29, 110:91.42,
    111:92.55, 112:93.68, 113:94.81, 114:95.94, 115:97.07, 116:98.19, 117:99.32, 118:100.45, 119:101.58, 120:102.71,
    121:103.84, 122:104.97, 123:106.09, 124:107.22, 125:108.35, 126:109.48, 127:110.61, 128:111.74, 129:112.87, 130:114.0,
    131:115.12, 132:116.25, 133:117.38, 134:118.51, 135:119.64, 136:120.77, 137:121.9, 138:123.02, 139:124.15, 140:125.28,
    141:126.41, 142:127.54, 143:128.67, 144:129.8, 145:130.93, 146:132.05, 147:133.18, 148:134.31, 149:135.44, 150:136.57,
    151:137.7, 152:138.83, 153:139.95, 154:141.08, 155:142.21, 156:143.34, 157:144.47, 158:145.6, 159:146.73, 160:147.86,
    161:148.9, 162:150.11, 163:151.24, 164:152.37, 165:153.5, 166:154.63, 167:155.76, 168:156.88, 169:158.01, 170:159.14,
    171:160.27, 172:161.4, 173:162.53, 174:163.66, 175:164.79, 176:165.91, 177:167.04, 178:168.17, 179:169.3, 180:170.43,
    181:171.6, 182:172.69, 183:173.81, 184:174.94, 185:176.07, 186:177.2, 187:178.33, 188:179.46, 189:180.59, 190:181.72,
    191:182.84, 192:183.97, 193:185.1, 194:186.23, 195:187.36, 196:188.49, 197:189.62, 198:190.74, 199:191.87, 200:193.0,
    201:194.13, 202:195.26, 203:196.39, 204:197.52, 205:198.65, 206:199.77, 207:200.9, 208:202.03, 209:203.16, 210:204.29,
    211:205.42, 212:206.55, 213:207.67, 214:208.8, 215:209.93, 216:211.06, 217:212.19, 218:213.32, 219:214.45, 220:215.58,
    221:216.7, 222:217.83, 223:218.96, 224:220.09, 225:221.22, 226:222.35, 227:223.48, 228:224.6, 229:225.73, 230:226.86,
    231:227.99, 232:229.12, 233:230.25, 234:231.38, 235:232.51, 236:233.63, 237:234.76, 238:235.89, 239:237.02, 240:238.15,
    241:239.28, 242:240.41, 243:241.53, 244:242.66, 245:243.79, 246:244.92, 247:246.05, 248:247.18, 249:248.31, 250:249.44,
    251:250.56, 252:251.69, 253:252.82, 254:253.95, 255:255.08
}

# ============= Packet Data Size Definition ============= #
# TimeStamp_Sensor
WIN_TIMESTAMP_SIZE = 17

# Head
XT_HEAD_SIZE = 12

# Body
XT_BLOCK_NUMBER = 8
XT_BLOCK_HEADER_AZIMUTH = 2
XT_UNIT_NUM = 32
XT_UNIT_SIZE = 4
XT_BLOCK_SIZE = XT_UNIT_SIZE * XT_UNIT_NUM + XT_BLOCK_HEADER_AZIMUTH
XT_BODY_SIZE = XT_BLOCK_SIZE * XT_BLOCK_NUMBER
XT_DUAL_BLOCK_SIZE = 4
XT_SINGLE_BLOCK_SIZE = 8
XT_DUAL_BLOCK_RES = 2
XT_SINGLE_BLOCK_RES = 1
XT_AZIMUTH_SIZE = 2
XT_DISTANCE_SIZE = 2

# Tail
XT_RESERVED_SIZE = 10
XT_ENGINE_VELOCITY = 2
XT_UTC_SIZE = 6
XT_TIMESTAMP_SIZE = 4
XT_ECHO_SIZE = 1
XT_FACTORY_SIZE = 1
XT_SEQUENCE_SIZE = 4
XT_TAIL_SIZE = 28

# All
XT_DATA_SIZE = XT_HEAD_SIZE + XT_BODY_SIZE + XT_TAIL_SIZE
XT_PACKET_SIZE = XT_DATA_SIZE + WIN_TIMESTAMP_SIZE
XT_MAX_POINT_SIZE = 256

# ============= Point Cloud Data Save Funciton ============= #
# Write point cloud data to PCD Format
def writePCDFile(fname,x,y,z,i):
    numPoints= len(x)
    with open(fname, 'w') as fp:
        fp.write("VERSION .7\n")
        fp.write("FIELDS x y z intensity\n")
        fp.write("SIZE 8 8 8 8\n")
        fp.write("TYPE F F F F\n")
        fp.write("COUNT 1 1 1 1\n")
        fp.write("WIDTH "+str(numPoints)+"\n")
        fp.write("HEIGHT 1\n")
        fp.write("VIEWPOINT 0 0 0 1 0 0 0\n")
        fp.write("POINTS "+str(numPoints)+"\n")
        fp.write("DATA ascii\n")
        for index in range(numPoints):
            txtLine = "{} {} {} {}\n".format(x[index],y[index],z[index], i[index] )
            fp.write(txtLine)
        pass

# Write point cloud data to Kitti Format
def writeKittiFile(_dirs, cnt, _Xyzi):
    kitti_fileName = "{}/kitti{}.bin".format(_dirs, cnt)
    np_x = np.asarray(_Xyzi)[:,0].astype(np.float32)
    np_y = np.asarray(_Xyzi)[:,1].astype(np.float32)
    np_z = np.asarray(_Xyzi)[:,2].astype(np.float32)
    np_i = np.asarray(_Xyzi)[:,3].astype(np.float32)/256
    points_32 = np.transpose(np.vstack((np_x, np_y, np_z, np_i)))
    points_32.tofile(kitti_fileName)

# ============= Process Function ============= #
# Packet Capture
def capture(port, conn):
    # Open socket & binding raw data (port: 2368)
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind(('', port))
    try:
        while 1:
            # send raw data through UDP protocol communication
            try:
                data = soc.recv(2000)
                if len(data) > 0:
                    assert len(data) == 1080, len(data)
                    conn.send(data)
                    
            except Exception as e:
                print(dir(e), e.message, e.__class__.__name__)
                traceback.print_exc(e)

    except KeyboardInterrupt as e:
        print(e)

# Save Frame Binary Data
def save_data(shared_data, conn):
    try:
        # Definition of buffer to byte array
        buffer = bytearray(XT_DATA_SIZE)

        # Definition time
        Time = time.monotonic()

        # While Loop
        while 1:
            # shared memory polling to get data
            if conn.poll():
                # Receive Data from Packet
                data = conn.recv()

                # Buffer Accumulate until 10Hz(0.1s) = 1 Frame
                buffer += data
            
            # Send LiDAR frame data to check time 0.1s(10Hz)
            if time.monotonic() - Time >= 0.1:
                # Send to Shared Memory
                shared_data[1].send(buffer)
                
                # Initialization buffer & time
                buffer = bytearray(XT_DATA_SIZE)
                Time = time.monotonic()
                
    except KeyboardInterrupt as e:
        print(e)

# Unpacking LiDAR Binary Data in frame
def unpack(shared_data, shared_XYZ):
    # Definition raw data
    raw_data = []
    Time = time.monotonic()

    # While Loop
    while 1:
        # Polling shared data
        if shared_data[0].poll():
            raw_data = shared_data[0].recv()

            # Calculate number of packet
            N = len(raw_data) / 1080

            # Definition Azimuth, Distance, Reflection, Channel Array
            int_azim_0 = np.empty(int(XT_MAX_POINT_SIZE * N), dtype=np.uint8)
            int_azim_1 = np.empty(int(XT_MAX_POINT_SIZE * N), dtype=np.uint8)
            int_dist_0 = np.empty(int(XT_MAX_POINT_SIZE * N), dtype=np.uint8)
            int_dist_1 = np.empty(int(XT_MAX_POINT_SIZE * N), dtype=np.uint8)
            int_refl   = np.empty(int(XT_MAX_POINT_SIZE * N), dtype=np.uint8)

            # For Loop to slice azimuth, distance, reflection
            for i in np.arange(0, N):
                i_pck = int(XT_DATA_SIZE * i)
                body = raw_data[i_pck + XT_HEAD_SIZE : i_pck + XT_HEAD_SIZE + XT_BODY_SIZE]
                i_bin = int(XT_MAX_POINT_SIZE * i)

                # Azimuth, Distance, Reflection Frame Packet Store 
                int_azim_0[i_bin : i_bin + XT_MAX_POINT_SIZE] = [body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],body[0],\
                                                                 body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],body[130],\
                                                                    body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],body[260],\
                                                                        body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],body[390],\
                                                                            body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],body[520],\
                                                                                body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],body[650],\
                                                                                    body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],body[780],\
                                                                                        body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910],body[910]]
                
                int_azim_1[i_bin : i_bin + XT_MAX_POINT_SIZE] = [body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],body[1],\
                                                                 body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],body[131],\
                                                                    body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],body[261],\
                                                                        body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],body[391],\
                                                                            body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],body[521],\
                                                                                body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],body[651],\
                                                                                    body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],body[781],\
                                                                                        body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911],body[911]]
                
                int_dist_0[i_bin : i_bin+XT_MAX_POINT_SIZE] = [body[2],body[6],body[10],body[14],body[18],body[22],body[26],body[30],body[34],body[38],body[42],body[46],body[50],body[54],body[58],body[62],body[66],body[70],body[74],body[78],body[82],body[86],body[90],body[94],body[98],body[102],body[106],body[110],body[114],body[118],body[122],body[126],\
                                                               body[132],body[136],body[140],body[144],body[148],body[152],body[156],body[160],body[164],body[168],body[172],body[176],body[180],body[184],body[188],body[192],body[196],body[200],body[204],body[208],body[212],body[216],body[220],body[224],body[228],body[232],body[236],body[240],body[244],body[248],body[252],body[256],\
                                                                body[262],body[266],body[270],body[274],body[278],body[282],body[286],body[290],body[294],body[298],body[302],body[306],body[310],body[314],body[318],body[322],body[326],body[330],body[334],body[338],body[342],body[346],body[350],body[354],body[358],body[362],body[366],body[370],body[374],body[378],body[382],body[386],\
                                                                    body[392],body[396],body[400],body[404],body[408],body[412],body[416],body[420],body[424],body[428],body[432],body[436],body[440],body[444],body[448],body[452],body[456],body[460],body[464],body[468],body[472],body[476],body[480],body[484],body[488],body[492],body[496],body[500],body[504],body[508],body[512],body[516],\
                                                                        body[522],body[526],body[530],body[534],body[538],body[542],body[546],body[550],body[554],body[558],body[562],body[566],body[570],body[574],body[578],body[582],body[586],body[590],body[594],body[598],body[602],body[606],body[610],body[614],body[618],body[622],body[626],body[630],body[634],body[638],body[642],body[646],\
                                                                            body[652],body[656],body[660],body[664],body[668],body[672],body[676],body[680],body[684],body[688],body[692],body[696],body[700],body[704],body[708],body[712],body[716],body[720],body[724],body[728],body[732],body[736],body[740],body[744],body[748],body[752],body[756],body[760],body[764],body[768],body[772],body[776],\
                                                                                body[782],body[786],body[790],body[794],body[798],body[802],body[806],body[810],body[814],body[818],body[822],body[826],body[830],body[834],body[838],body[842],body[846],body[850],body[854],body[858],body[862],body[866],body[870],body[874],body[878],body[882],body[886],body[890],body[894],body[898],body[902],body[906],\
                                                                                    body[912],body[916],body[920],body[924],body[928],body[932],body[936],body[940],body[944],body[948],body[952],body[956],body[960],body[964],body[968],body[972],body[976],body[980],body[984],body[988],body[992],body[996],body[1000],body[1004],body[1008],body[1012],body[1016],body[1020],body[1024],body[1028],body[1032],body[1036]]
                
                int_dist_1[i_bin : i_bin+XT_MAX_POINT_SIZE] = [body[3],body[7],body[11],body[15],body[19],body[23],body[27],body[31],body[35],body[39],body[43],body[47],body[51],body[55],body[59],body[63],body[67],body[71],body[75],body[79],body[83],body[87],body[91],body[95],body[99],body[103],body[107],body[111],body[115],body[119],body[123],body[127],\
                                                               body[133],body[137],body[141],body[145],body[149],body[153],body[157],body[161],body[165],body[169],body[173],body[177],body[181],body[185],body[189],body[193],body[197],body[201],body[205],body[209],body[213],body[217],body[221],body[225],body[229],body[233],body[237],body[241],body[245],body[249],body[253],body[257],\
                                                                body[263],body[267],body[271],body[275],body[279],body[283],body[287],body[291],body[295],body[299],body[303],body[307],body[311],body[315],body[319],body[323],body[327],body[331],body[335],body[339],body[343],body[347],body[351],body[355],body[359],body[363],body[367],body[371],body[375],body[379],body[383],body[387],\
                                                                    body[393],body[397],body[401],body[405],body[409],body[413],body[417],body[421],body[425],body[429],body[433],body[437],body[441],body[445],body[449],body[453],body[457],body[461],body[465],body[469],body[473],body[477],body[481],body[485],body[489],body[493],body[497],body[501],body[505],body[509],body[513],body[517],\
                                                                        body[523],body[527],body[531],body[535],body[539],body[543],body[547],body[551],body[555],body[559],body[563],body[567],body[571],body[575],body[579],body[583],body[587],body[591],body[595],body[599],body[603],body[607],body[611],body[615],body[619],body[623],body[627],body[631],body[635],body[639],body[643],body[647],\
                                                                            body[653],body[657],body[661],body[665],body[669],body[673],body[677],body[681],body[685],body[689],body[693],body[697],body[701],body[705],body[709],body[713],body[717],body[721],body[725],body[729],body[733],body[737],body[741],body[745],body[749],body[753],body[757],body[761],body[765],body[769],body[773],body[777],\
                                                                                body[783],body[787],body[791],body[795],body[799],body[803],body[807],body[811],body[815],body[819],body[823],body[827],body[831],body[835],body[839],body[843],body[847],body[851],body[855],body[859],body[863],body[867],body[871],body[875],body[879],body[883],body[887],body[891],body[895],body[899],body[903],body[907],\
                                                                                    body[913],body[917],body[921],body[925],body[929],body[933],body[937],body[941],body[945],body[949],body[953],body[957],body[961],body[965],body[969],body[973],body[977],body[981],body[985],body[989],body[993],body[997],body[1001],body[1005],body[1009],body[1013],body[1017],body[1021],body[1025],body[1029],body[1033],body[1037]]
                
                int_refl[i_bin : i_bin+XT_MAX_POINT_SIZE] = [body[4],body[8],body[12],body[16],body[20],body[24],body[28],body[32],body[36],body[40],body[44],body[48],body[52],body[56],body[60],body[64],body[68],body[72],body[76],body[80],body[84],body[88],body[92],body[96],body[100],body[104],body[108],body[112],body[116],body[120],body[124],body[128],\
                                                             body[134],body[138],body[142],body[146],body[150],body[154],body[158],body[162],body[166],body[170],body[174],body[178],body[182],body[186],body[190],body[194],body[198],body[202],body[206],body[210],body[214],body[218],body[222],body[226],body[230],body[234],body[238],body[242],body[246],body[250],body[254],body[258],\
                                                                body[264],body[268],body[272],body[276],body[280],body[284],body[288],body[292],body[296],body[300],body[304],body[308],body[312],body[316],body[320],body[324],body[328],body[332],body[336],body[340],body[344],body[348],body[352],body[356],body[360],body[364],body[368],body[372],body[376],body[380],body[384],body[388],\
                                                                    body[394],body[398],body[402],body[406],body[410],body[414],body[418],body[422],body[426],body[430],body[434],body[438],body[442],body[446],body[450],body[454],body[458],body[462],body[466],body[470],body[474],body[478],body[482],body[486],body[490],body[494],body[498],body[502],body[506],body[510],body[514],body[518],\
                                                                        body[524],body[528],body[532],body[536],body[540],body[544],body[548],body[552],body[556],body[560],body[564],body[568],body[572],body[576],body[580],body[584],body[588],body[592],body[596],body[600],body[604],body[608],body[612],body[616],body[620],body[624],body[628],body[632],body[636],body[640],body[644],body[648],\
                                                                            body[654],body[658],body[662],body[666],body[670],body[674],body[678],body[682],body[686],body[690],body[694],body[698],body[702],body[706],body[710],body[714],body[718],body[722],body[726],body[730],body[734],body[738],body[742],body[746],body[750],body[754],body[758],body[762],body[766],body[770],body[774],body[778],\
                                                                                body[784],body[788],body[792],body[796],body[800],body[804],body[808],body[812],body[816],body[820],body[824],body[828],body[832],body[836],body[840],body[844],body[848],body[852],body[856],body[860],body[864],body[868],body[872],body[876],body[880],body[884],body[888],body[892],body[896],body[900],body[904],body[908],\
                                                                                    body[914],body[918],body[922],body[926],body[930],body[934],body[938],body[942],body[946],body[950],body[954],body[958],body[962],body[966],body[970],body[974],body[978],body[982],body[986],body[990],body[994],body[998],body[1002],body[1006],body[1010],body[1014],body[1018],body[1022],body[1026],body[1030],body[1034],body[1038]]
            # Unpacking Azimuth, Range, Reflection to use buffer    
            azim = (np.uint16(int_azim_1) << 8) | int_azim_0
            range = (np.uint16(int_dist_1) << 8) | int_dist_0

            # Find the index of an array with a nonzero value
            i_valid = np.where(range != 0)

            # Transformation azimuth, vertical angle, range, reflection through specification about HESAI XT32 (AZIMUTH UNIT: 0.01, DISTANCE_RESOLUTION: 0.004)
            azim = np.deg2rad(azim[i_valid] * AZIMUTH_UNIT)
            v_angle = np.deg2rad(V_ANGLE_GLB[i_valid])
            range = range[i_valid] * DISTANCE_RESOLUTION
            int_refl = int_refl[i_valid]

            # Calculation X, Y, Z, I to use matrix element product
            X = np.multiply(range, np.multiply(np.cos(v_angle), np.sin(azim)))
            Y = np.multiply(range, np.multiply(np.cos(v_angle), np.cos(azim)))
            Z = np.multiply(range, np.sin(v_angle))
            
            # Transposition about X, Y, Z to XYZ array (:, 3)
            points_32 = np.transpose(np.vstack((X, Y, Z)))

            # Send XYZ Data using multiprocessing.Pipe()
            shared_XYZ[1].send(points_32)

            # Print the point size and del time
            print(f"point_size: {len(points_32)} del_time: {time.monotonic() - Time}")

            # Time Update
            Time = time.monotonic()

# Visualization Point Cloud Data to BEV(bird eye view)    
def visualization(shared_XYZ):
    # X, Y, Z, I Definition
    Xyz = np.empty((0,3), dtype=np.float32)
    np_x = np.asarray(Xyz)[:,0].astype(np.float32)
    np_y = np.asarray(Xyz)[:,1].astype(np.float32)

    # Visualization Specification
    _, ax = plt.subplots()
    sc = ax.scatter(np_x, np_y, s=0.01)
    plt.xlim([-3, 3])
    plt.ylim([-3, 3])
    plt.draw()

    # Data Update Function
    def update_point_cloud(_Xyz):
        new_point_cloud = _Xyz[:, 0:2]
        sc.set_offsets(new_point_cloud)
        plt.pause(0.01)

    while 1:
        # Receive XYZ coordinate information using polling to prevent a communication conflict
        if shared_XYZ[0].poll():
            Xyz = shared_XYZ[0].recv()
        
        # Update XYZ data in BEV
        if Xyz != []:
            update_point_cloud(Xyz)

            
# ============= Multiprocessing Pipeline Main Loop ============= #
if __name__ == '__main__':

    # Definition Shared Memory using multiprocessing.Pipe()
    # conn1, conn2: Packet data(1080bytes)
    # shared_data : 1 frame data(1080 * N bytes)
    # shared_XYZ  : X, Y, Z coordinate information through unpacking shared data
    conn1, conn2 = Pipe()
    shared_data = Pipe()
    shared_XYZ = Pipe()
    
    # Multiprocessing capture, save data, unpacking, visualization
    processA = Process(target = capture, args = (PORT, conn1))
    processA.start()
    processB = Process(target = save_data, args = (shared_data, conn2))
    processB.start()
    processC = Process(target = unpack, args=(shared_data, shared_XYZ))
    processC.start()
    processD = Process(target = visualization, args=(shared_XYZ,))
    processD.start()