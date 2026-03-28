import os

def getSize(path):
    try:
        files = {}
        for f in os.listdir(path):
            fpath = os.path.join(path, f)
            size = None
            if os.path.isfile(fpath):
                size = os.path.getsize(fpath)
                files[f] = (size, None)
            elif os.path.isdir(fpath):
                files[f] = getSize(fpath)
        size = os.path.getsize(path)
        for i in files.values():
            size += i[0]
        return (size, files)
    except PermissionError as e:
        return (0, e)

def listChildrenSize(dirinfo):
    children = dirinfo[1]
    cs = []
    for i in children.keys():
        cs.append((i, children[i][0] / (1024**3)))
    cs.sort(reverse=True, key=(lambda x: x[1]))
    cs = list(map(lambda x: (x[0], f'{x[1]:.3f}GB'), cs))
    return cs

def listDirSize(path, rootinfo):
    pathComps = os.path.normpath(path).split(os.path.sep)
    pathComps = list(filter(lambda x: x != '.', pathComps))
    dirinfo = rootinfo
    for i in pathComps:
        dirinfo = dirinfo[1][i]
    return listChildrenSize(dirinfo)
