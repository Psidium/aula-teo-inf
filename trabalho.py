import RLE
import sys
from dahuffman import HuffmanCodec
import dahuffman
import lz4.frame
import pdb
import umsgpack
import argparse

parser = argparse.ArgumentParser(description='Compact or decompact data')

parser.add_argument('--encode', dest='is_encode', action='store_true')
parser.add_argument('--decode', dest='is_encode', action='store_false')
parser.add_argument('--input', dest='input_filename', required=True)
parser.add_argument('--output', dest='output_filename', required=True)

args = parser.parse_args()

handlers = {
    dahuffman.huffmancodec._EndOfFileSymbol: lambda obj: umsgpack.Ext(0x30, b'1')
}
huffmann_counter = 0
lz4_counter = 0
def pack_smaller(first, huffman):
    first_packed = umsgpack.packb(first)
    second_packed = umsgpack.packb(huffman, ext_handlers=handlers)
    if sys.getsizeof(first_packed) > sys.getsizeof(second_packed):
        global lz4_counter
        lz4_counter += 1
        return first
    else:
        global huffmann_counter
        huffmann_counter += 1
        return huffman

CHUNK = 2 ** 10
filename = sys.argv[1]
if args.is_encode:
    with open(args.input_filename, 'rb') as input_file:
       pedaco = input_file.read(CHUNK)
       output = []
       while pedaco:
          # pdb.set_trace()
           ped_lz4 = {
               'a': 4,
               'd': lz4.frame.compress(pedaco)
           }
           codec_huff = HuffmanCodec.from_data(pedaco)
           ped_huff = {
               'a': 'h',
               'd': codec_huff.encode(pedaco),
               't': codec_huff.get_code_table()
           }
           small_dict = pack_smaller(ped_lz4, ped_huff)
           output.append(small_dict)
           #do stuff
           pedaco = input_file.read(CHUNK)
       with open(args.output_filename, 'wb') as output_file:
           umsgpack.pack(output, output_file, ext_handlers=handlers)
print('huffman %d' % huffmann_counter)
print('lz4 %d' % lz4_counter)
