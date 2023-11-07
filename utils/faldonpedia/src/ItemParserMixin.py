import struct
import string
from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column
class ItemParserMixin():
    __abstract__ = True

    def read_data(self, bin_data:bytes, offset:str, read_length:str, format_str:str="@H"):
        init_offset = int(offset, 16)
        int_length = int(read_length, 16)
        # Format string needs to ingest all bytes
        # Check to make sure no bytes remain
        read_size = struct.calcsize(format_str)
        if int_length % read_size != 0:
            print("Format str for struct size is incompatible with read length.")
            exit(1)

        read_values = bytearray()
        read_times = int_length // read_size
        current_offset = init_offset
        for i in range(read_times):
            read_end = init_offset+((i+1)*read_size) #End of range that will be read

            value = struct.unpack(format_str, bin_data[current_offset:read_end])[0]
            #print(f"Reading from {hex(current_offset)} to {hex(read_end)}")
            current_offset += read_size

            if type(value) == int:
                read_values += value.to_bytes(read_size, 'big')
            else:
                read_values += value

        if format_str == "@c": # Strip spaces if we're decoding a string
            return read_values.rstrip()

        return read_values

    def parse_per_schema(self, item_data, schema, schema_part):

        for field in schema[schema_part]:
            if "address" not in schema[schema_part][field]:
                item_data[field] = {}
                self.parse_per_schema(item_data[field], schema[schema_part], field )
            else:
                address = schema[schema_part][field]['address']
                length = schema[schema_part][field]['length']
                field_type = schema[schema_part][field]['format']
                
                match field_type:
                    case "utf-8":
                        item_data[field] = string.capwords(self.read_data(self.bin_data, address, length, "@c").decode()).replace("'", "")
                    case "uint8":
                        item_data[field] = self.bin_data[int(address, 16)]
                    case "int8":
                        unsigned = self.bin_data[int(address, 16)]
                        item_data[field] = unsigned-127
                    case "sint8":
                        unsigned = self.bin_data[int(address, 16)]
                        if unsigned > 127:
                            unsigned -= 256
                        item_data[field] = unsigned
                    case "uint16":
                        read_data = self.read_data(self.bin_data, address, length, "@H")
                        item_data[field] = int.from_bytes(read_data, byteorder='big', signed=True)
                    case _:
                        print(f"field format of {field_type} not defined...")
