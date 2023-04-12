from configparser import ConfigParser


def __install__(package):
    __import__('subprocess').call([__import__('sys').executable, "-m", "pip", "install", package])


def safe_import(name):
    try:
        module = __import__(name)
        return module
    except ModuleNotFoundError as ex:
        if input('module ' + name + ' not installed, do you want to install?(y/n): ').upper() == 'Y':
            __install__(name)
        return safe_import(name)


def safe_import_attr(module, *attrs):
    ret_attrs = []
    for attr in attrs:
        ret_attrs.append(getattr(safe_import(module), attr))
    return ret_attrs


def _read_config(section: str, filename='config.ini') -> dict:
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


def read_db_config() -> dict:
    return _read_config('mysql')


def read_flask_config() -> dict:
    return _read_config('flask')
