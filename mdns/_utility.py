class Index():
    def __init__(self, value = 0):
        '''
        :param value: The initial value of the instance. Default to 0.
        :type value: int or :class:`Index`

        Represent a mutable integer that is very usefull when used as index in encode/decode methods since it will be automatically updated and so keeps track of the current position in the data array.
        this class mimic the `int` builtin class for addition and indexing.
        '''
        if isinstance(value, Index):
            self._value = value._value
        else:
            self._value = value
    def __index__(self):
        return self._value
    def __add__(self, other):
        return Index(self._value + other)
    def __radd__(self, other):
        return Index(self._value + other)
    def advance(self, quantity):
        '''
        :param quantity: The ammount to which the instance value has to be incremented.
        :type quantity: int

        Increment the instance value by the given quantity.
        '''
        self._value += quantity

def read_short(data, idx):
    res =  int.from_bytes(data[idx: idx + 2], byteorder='big')
    idx.advance(2)
    return res
def read_int(data, idx):
    res =  int.from_bytes(data[idx: idx + 4], byteorder='big')
    idx.advance(4)
    return res
def write_short(num, data):
    data.extend(num.to_bytes(2, byteorder='big'))
def write_int(num, data):
    data.extend(num.to_bytes(4, byteorder='big'))
def read_name(data, idx):
    size = data[idx]
    if size == 0:
        name = ''
        idx.advance(1)
    elif (size & 0xC0) != 0:
        #name is compressed
        tmp_idx = Index()
        tmp_idx = Index(read_short([size & 0x3F, data[idx + 1]], tmp_idx))
        name = read_name(data, tmp_idx)
        idx.advance(2)
    else:
        #name is not compressed
        idx.advance(1)
        name = data[idx:idx + size].decode('UTF-8') + '.'
        idx.advance(size)
        n = read_name(data, idx)
        name += n
    return name
def write_name(name, data, name_compression_dictionary):
    tokens = list(map(lambda t: bytes([len(t)]) + t ,[t.encode('UTF-8') for t in name.split('.') if len(t) != 0]))
    for token in [(tokens[i], b''.join(tokens[i:])) for i in range(len(tokens))]:
        if name_compression_dictionary != None and token[1] in name_compression_dictionary:
            offset = name_compression_dictionary[token[1]]
            offset |= 0xC000
            write_short(offset, data)
            return
        else:
            if name_compression_dictionary != None:
                name_compression_dictionary[token[1]] = len(data)
            data.extend(token[0])
    data.append(0)