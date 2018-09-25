import RLE
import sys
from dahuffman import HuffmanCodec
import lz4.frame

CHUNK = 2 ** 10
filename = sys.argv[1]
with open(filename, 'rb') as arquivo:
   pedaco = arquivo.read(CHUNK)
   while pedaco:
       print(pedaco)
       ped_lz4 = lz4.frame.encode(pedaco)
       codec_huff = HuffmanCodec.from_data(pedaco)
       ped_huff = codec_huff.encode(pedaco)
       ped_huff_table = codec_huff.get_code_table()
       #do stuff
       pedaco = arquivo.read(CHUNK)
