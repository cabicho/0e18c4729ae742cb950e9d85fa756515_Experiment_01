import sys, struct, os

_MAGIC = 'BM'

def read_bmp(file):
    '''
    reads bitmap file and returns 
    ((magic, size, reserved, offset), info header, palette (optional), image data)
    '''
    header = ()
    magic = file.read(2)
    assert magic == _MAGIC
    size, = struct.unpack('<I', file.read(4))
    assert size == os.stat(file.name).st_size
    reserved = file.read(4)
    offset, = struct.unpack('<I', file.read(4))
    header = (magic, size, reserved, offset)
    info_header = file.read(40)
    
    if file.tell() == offset:
        return (header, info_header, file.read())
    else:
        return (header, info_header, file.read(offset - file.tell()), file.read())

def main():
    if len(sys.argv) != 4:
        print "Usage:\nmergeBMP <BMP-FILE-1> <BMP-FILE-2> <OUTPUT-FILE>"
    else:
        with open(sys.argv[1], 'rb') as fbmp1, open(sys.argv[2], 'rb') as fbmp2, open(sys.argv[3], 'wb') as fout:
            bmp1 = read_bmp(fbmp1)
            bmp2 = read_bmp(fbmp2)
            # write magic
            fout.write(bmp1[0][0])
            # write size
            img_data = bmp2[len(bmp2)-1]
            new_size = bmp1[0][1] + len(img_data)
            fout.write(struct.pack('<I', new_size))
            # write reserved fields
            fout.write(bmp1[0][2])
            # write offset
            fout.write(struct.pack('<I', os.stat(sys.argv[1]).st_size))
            # write info header
            fout.write(bmp1[1])
            # write remaining data
            fout.write(bmp1[2])
            if len(bmp1) == 4:
                fout.write(bmp1[3])
            # append image data of second bmp file
            fout.write(img_data)

if __name__ == "__main__":
    main()
