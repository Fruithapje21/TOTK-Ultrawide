import os
import SarcLib
import zstandard as zstd

def decompress_zs(zs_path, blarc_path, zsdic_path):
    with open(zsdic_path, 'rb') as f:
        dict_data = zstd.ZstdCompressionDict(f.read())
    dctx = zstd.ZstdDecompressor(dict_data=dict_data)
    with open(zs_path, 'rb') as ifh, open(blarc_path, 'wb') as ofh:
        decompressed_data = dctx.decompress(ifh.read())
        ofh.write(decompressed_data)
     
def compress_zs(blarc_path, zs_path, zsdic_path):
    with open(zsdic_path, 'rb') as f:
        dict_data = zstd.ZstdCompressionDict(f.read())
    cctx = zstd.ZstdCompressor(dict_data=dict_data, level=14)
    with open(blarc_path, 'rb') as ifh, open(zs_path, 'wb') as ofh:
        compressed_data = cctx.compress(ifh.read())
        ofh.write(compressed_data)

def extract_blarc(blarc_path, out_dir):
    
    with open(blarc_path, "rb") as f:
        inb = f.read()
    
    arc = SarcLib.SARC_Archive()
    arc.load(inb)
    
    root = out_dir
    if not os.path.isdir(root):
        os.mkdir(root)
    
    files = []
    
    def getAbsPath(folder, path):
        nonlocal root
        nonlocal files
    
        for checkObj in folder.contents:
            if isinstance(checkObj, SarcLib.File):
                files.append(["/".join([path, checkObj.name]), checkObj.data])
            else:
                path_ = os.path.join(root, "/".join([path, checkObj.name]))
                if not os.path.isdir(path_):
                    os.mkdir(path_)
                getAbsPath(checkObj, "/".join([path, checkObj.name]))
    
    for checkObj in arc.contents:
        if isinstance(checkObj, SarcLib.File):
            files.append([checkObj.name, checkObj.data])
        else:
            path = os.path.join(root, checkObj.name)
            if not os.path.isdir(path):
                os.mkdir(path)
            getAbsPath(checkObj, checkObj.name)
    
    for file, fileData in files:
        with open(os.path.join(root, file), "wb") as out:
            out.write(fileData)

def repack_blarc(root, out_file):
    """
    Pack the files and folders in the root folder.
    """
    if "\\" in root:
        root = "/".join(root.split("\\"))

    if root[-1] == "/":
        root = root[:-1]

    arc = SarcLib.SARC_Archive(endianness='>')
    lenroot = len(root.split("/"))

    for path, dirs, files in os.walk(root):
        if "\\" in path:
            path = "/".join(path.split("\\"))

        lenpath = len(path.split("/"))

        if lenpath == lenroot:
            path = ""
        else:
            path = "/".join(path.split("/")[lenroot - lenpath:])

        for file in files:
            if path:
                filename = ''.join([path, "/", file])
            else:
                filename = file


            fullname = ''.join([root, "/", filename])

            i = 0
            for folder in filename.split("/")[:-1]:
                if not i:
                    exec("folder%i = SarcLib.Folder(folder + '/'); arc.addFolder(folder%i)".replace('%i', str(i)))
                else:
                    exec("folder%i = SarcLib.Folder(folder + '/'); folder%m.addFolder(folder%i)".replace('%i', str(i)).replace('%m', str(i - 1)))

                i += 1

            with open(fullname, "rb") as f:
                inb = f.read()

            hasFilename = True
            if file[:5] == "hash_":
                hasFilename = False

            if not i:
                arc.addFile(SarcLib.File(file, inb, hasFilename))

            else:
                exec("folder%m.addFile(SarcLib.File(file, inb, hasFilename))".replace('%m', str(i - 1)))

    data, maxAlignment = arc.save()

    with open(out_file, "wb+") as output:
        output.write(data)
        
