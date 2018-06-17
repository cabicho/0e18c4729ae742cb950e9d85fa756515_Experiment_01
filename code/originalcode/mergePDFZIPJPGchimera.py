import sys, struct, binascii
from datetime import datetime
from os.path import basename

_JPG_MAGIC = b"\xFF\xD8"
_JPG_APP0 = b"\xFF\xE0"
_JPG_COM = b"\xFF\xFE"
_JPG_SOF_BASELINE = b"\xFF\xC0"
_JPG_SOF_PROGRESSIVE = b"\xFF\xC2"
_JPG_JFIF = b"JFIF\x00" # zero terminated
_JPG_EOF = b"\xFF\xD9"

_PDF_MAGIC = b"\x25PDF-1.7\n"
_PDF_CATALOG = b"1 0 obj <</Type /Catalog /Pages 2 0 R>>\nendobj\n"
_PDF_PAGES = b"2 0 obj <</Type /Pages /Kids [3 0 R] /Count 1>>\nendobj\n"
_PDF_PAGE = b"3 0 obj <</Type /Page /MediaBox [0 0 {} {}] /Parent 2 0 R /Resources <</XObject <</Img1 4 0 R>>>> /Contents 5 0 R>>\nendobj\n"
_PDF_LFH_DUMMY_START = b"10 0 obj <</Length 30>>\nstream\n" # length always 30
_PDF_LFH_DUMMY_END = b"\nendstream\nendobj\n"
_PDF_IMAGE_START = b"4 0 obj <</Name /Img1 /Type /XObject /Subtype /Image /Intent /Perceptual /Width {} /Height {} /Length {} /Filter /DCTDecode /ColorSpace /DeviceRGB /BitsPerComponent 8>>\nstream\n"
_PDF_IMAGE_END = b" endstream\nendobj\n"
_PDF_CDFH_DUMMY_START = b"11 0 obj <</Length 80>>\nstream\n"
_PDF_CDFH_DUMMY_END = b"\nendstream\nendobj\n"
_PDF_DRAW_IMG_OBJ = b"5 0 obj <</Length {}>>\nstream\nq {} 0 0 {} 0 0 cm /Img1 Do Q\nendstream\nendobj\n"
_PDF_XREF = b"xref\n"+\
            "0 6\n"+\
            "0000000000 65535 f\n"+\
            "{0} 00000 n\n"+\
            "{1} 00000 n\n"+\
            "{2} 00000 n\n"+\
            "{3} 00000 n\n"+\
            "{4} 00000 n\n"+\
            "trailer <</Size 6 /Root 1 0 R>>\n"+\
            "startxref\n{5}\n"+\
            "%%EOF\n"

_ZIP_MAGIC = b"PK"
_ZIP_LFH = b"\x03\x04"
_ZIP_VERSION_NEEDED_TO_EXTRACT = b"\x14\x00"
_ZIP_GENERAL_PURPOSE = b"\x00\x00"
_ZIP_COMPRESSION = b"\x00\x00"
_ZIP_EXTRA_FIELD_LEN = b"\x00\x00"
_ZIP_CDFH_START = b"\x01\x02\x00\x00" + _ZIP_VERSION_NEEDED_TO_EXTRACT + _ZIP_GENERAL_PURPOSE + _ZIP_COMPRESSION
_ZIP_EOCDFH_START = b"\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00" # numb. of this disc (2 bytes), disk where central directory starts (2 bytes), number of central directory records on this disk (2 bytes), total number of central directory records (2 bytes)

class Image: pass

def read_jpg(file):
    image = Image()
    jpg_bytes = file.read() # read all bytes for crc32 checksum
    file.seek(0, 0)
    assert file.read(2) == _JPG_MAGIC, "JPG magic signature not at offset 0"
    assert file.read(2) == _JPG_APP0, "First marker of JPG file has to be APP0 (JFIF File)"
    assert struct.unpack(">H", file.read(2))[0] == 16, "APP0 header has to be exactly 16 bytes long"
    assert file.read(5) == _JPG_JFIF
    image.filename = basename(file.name)
    image.crc32 = struct.pack("<I", binascii.crc32(jpg_bytes) % 0x100000000)
    image.size = struct.pack("<I", len(jpg_bytes))
    image.version = [file.read(1), file.read(1)]
    image.units = file.read(1)
    image.xdensity = file.read(2)
    image.ydensity = file.read(2)
    file.seek(2, 1) # skip thumbnail resolution
    # temporarily save remaining bytes to be able to search for Start Of Image (SOI) marker
    data = file.read()
    # find SOF marker to read width and height of image
    i_sof = data.find(_JPG_SOF_BASELINE)
    if i_sof == -1:
        i_sof = data.find(_JPG_SOF_PROGRESSIVE)
    assert i_sof != -1, "No start of frame marker (SOF) found"
    image.height = data[i_sof+5:i_sof+7]
    image.width = data[i_sof+7:i_sof+9]
    # truncate appended bytes (bytes after EOF marker)
    i_eof = data.find(_JPG_EOF)
    assert i_eof != -1, "No end of image (EOF) marker found in JPG file"
    image.data = data
    return image

def build_header(image):
    return  _JPG_MAGIC +\
            _JPG_APP0 +\
            struct.pack(">H", 16) +\
            _JPG_JFIF +\
            image.version[0] +\
            image.version[1] +\
            image.units +\
            image.xdensity +\
            image.ydensity +\
            b"\x00" + \
            b"\x00"

def fill_values(image):
    global _PDF_PAGE
    global _PDF_IMAGE_START
    global _PDF_DRAW_IMG_OBJ
    
    _PDF_PAGE = _PDF_PAGE.format(struct.unpack(">H", image.width)[0], struct.unpack(">H", image.height)[0])
    _PDF_IMAGE_START = _PDF_IMAGE_START.format(struct.unpack(">H", image.width)[0], struct.unpack(">H", image.height)[0], len(build_header(image)) + len(image.data))
    
    _PDF_DRAW_IMG_OBJ = _PDF_DRAW_IMG_OBJ.format("{}", struct.unpack(">H", image.width)[0], struct.unpack(">H", image.height)[0])
    i_stream = _PDF_DRAW_IMG_OBJ.find("stream\n")
    i_endstream = _PDF_DRAW_IMG_OBJ.find("\nendstream")
    length = i_endstream - i_stream - 7 # 7 is the length of "stream "
    _PDF_DRAW_IMG_OBJ = _PDF_DRAW_IMG_OBJ.format(length)

def fill_xref(data, startxref):
    global _PDF_XREF
    data_str = "".join(data)
    obj_indices = [
                    data_str.find(_PDF_CATALOG),\
                    data_str.find(_PDF_PAGES),\
                    data_str.find(_PDF_PAGE),\
                    data_str.find(_PDF_IMAGE_START),\
                    data_str.find(_PDF_DRAW_IMG_OBJ)
                ]
    assert -1 not in obj_indices, "Could not find all 5 objects"
    padded_indices = ["{0:0>10}".format(x) for x in obj_indices]
    params = padded_indices + [startxref]
    _PDF_XREF = _PDF_XREF.format(*params)

def create_chimera(fout, image):
    output = []
    now = datetime.now()
    year, month, day, hours, minutes, seconds = now.year, now.month, now.day, now.hour, now.minute, now.second
    fill_values(image)
    # JPG header
    jpg_header = build_header(image)
    output.append(jpg_header)
    # start of JPG comment
    output.append(_JPG_COM)
    jpg_comment = _PDF_MAGIC +\
                _PDF_CATALOG +\
                _PDF_PAGES +\
                _PDF_PAGE +\
                _PDF_LFH_DUMMY_START +\
                _ZIP_MAGIC +\
                _ZIP_LFH +\
                _ZIP_VERSION_NEEDED_TO_EXTRACT +\
                _ZIP_GENERAL_PURPOSE +\
                _ZIP_COMPRESSION +\
                struct.pack('<H', int(bin(hours)[2:].zfill(5) + bin(minutes)[2:].zfill(6) + bin(seconds/2)[2:].zfill(5), 2)) +\
                struct.pack('<H', int(bin(year-1980)[2:].zfill(7) + bin(month)[2:].zfill(4) + bin(day)[2:].zfill(5), 2)) +\
                image.crc32 +\
                image.size +\
                image.size +\
                struct.pack('<H', len(_PDF_LFH_DUMMY_END) + len(_PDF_IMAGE_START)) +\
                _ZIP_EXTRA_FIELD_LEN +\
                _PDF_LFH_DUMMY_END +\
                _PDF_IMAGE_START +\
                jpg_header
    output.append(struct.pack(">H", len(jpg_comment)))
    output.append(jpg_comment)
    output.append(image.data)
    output.append(_PDF_IMAGE_END)
    output.append(_PDF_CDFH_DUMMY_START)
    output.append(_ZIP_MAGIC)
    output.append(_ZIP_CDFH_START)
    output.append(struct.pack('<H', int(bin(hours)[2:].zfill(5) + bin(minutes)[2:].zfill(6) + bin(seconds/2)[2:].zfill(5), 2)))
    output.append(struct.pack('<H', int(bin(year-1980)[2:].zfill(7) + bin(month)[2:].zfill(4) + bin(day)[2:].zfill(5), 2)))
    output.append(image.crc32)
    output.append(image.size)
    output.append(image.size)
    output.append(struct.pack("<H", len(image.filename)))
    output.append(_ZIP_EXTRA_FIELD_LEN)
    output.append(b"\x00\x00") # file comment length
    output.append(b"\x00\x00") # disk number where file starts
    output.append(b"\x00\x00\x00\x00\x00\x00") # internal and external file attributes
    offset_LFH = "".join(output).find(_ZIP_MAGIC + _ZIP_LFH)
    assert offset_LFH != -1, "Local file header (LFH) not found"
    output.append(struct.pack("<I", offset_LFH)) # relative offset of local file header
    output.append(image.filename)
    output.append(_ZIP_MAGIC)
    output.append(_ZIP_EOCDFH_START)
    output.append(struct.pack("<I", 46 + len(image.filename))) # length of CDFH
    offset_CDFH = "".join(output).find(_ZIP_MAGIC + _ZIP_CDFH_START)
    assert offset_CDFH != -1, "Central directory file header (CDFH) not found"
    output.append(struct.pack(">I", offset_CDFH))
    # we need to insert the length of the remaining bytes at this point
    # but we will do this AFTER we appended the remaining bytes so we can
    # calculate how many bytes we actually appended
    i_comment_start = len(output)
    output.append(_PDF_CDFH_DUMMY_END)
    output.append(_PDF_DRAW_IMG_OBJ)
    startxref = len("".join(output))
    fill_xref(output, startxref)
    output.append(_PDF_XREF)
    output.append(b"\x25") # "%" symbol, line comment in pdf
    output.append(_JPG_EOF)
    output.insert(i_comment_start, struct.pack(">H", len(output) - i_comment_start)) # insert length of remaining bytes here
    fout.write("".join(output))

def main():
    if len(sys.argv) != 3:
        print "Usage:\nmergePDFZIPJPGchimera.py <JPG-FILE> <OUTPUT-FILE>"
    else:
        with open(sys.argv[1], 'rb') as fjpg:
            image = read_jpg(fjpg)
        with open(sys.argv[2], 'wb') as fout:
            create_chimera(fout, image)

if __name__ == "__main__":
    main()
