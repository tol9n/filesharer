def convert_path(path, name):
    path = path.replace('-','/')
    key = f'{path}/{name}'
    return key