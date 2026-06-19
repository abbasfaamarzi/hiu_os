import os



def location_dir_path (path) :
    return os.path.dirname ( path )



def main_dir () :
    dirname = Path.location_dir_path ( __file__ )
    parts = Path.path_cutter ( dirname )
    try :
        app_name_index = parts.index ( "hiu_os")
        main_dir = parts[:app_name_index + 1]
        joined = Path.join ( *main_dir )
        return joined
    except Exception :
        return dirname

print(main_dir())