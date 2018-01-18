
def decode(file, block_info):
    result = bytearray()
    for info in block_info:
        result = __process_block(file, info["is_compressed"], info["block_start"], info["block_end"], result)
    return result.decode();
    # return result

def __process_block(file, is_compressed, block_start, block_end, previous_result):

    result = previous_result
    if not is_compressed:
        # TODO handle uncompressed block
        return result

    current_pos = block_start
    while current_pos < block_end:
        token_byte = file[current_pos]
        # print(hex(current_pos))

        literal_token = token_byte >> 4
        match_token = token_byte & 15
        current_pos += 1

        # Literal Copy

        if literal_token != 0:
            literal_length = literal_token
            if literal_token == 15:
                # Extend Literal Length
                while True:
                    v = file[current_pos]
                    literal_length += v
                    current_pos += 1
                    if v != 255:
                        break
            literal_start = current_pos
            if literal_start == 0x979:
                pass
            result += file[literal_start: literal_start + literal_length]
            current_pos += literal_length
            # print(literal_length + literal_start)
            # print("literalStart                             = " + str(hex(literal_start))[2:])
            # print("literalLength                            = " + str(hex(literal_length))[2:])
        else:
            pass
            # print("literalStart                             = " + str(hex(current_pos))[2:])
            # print("literalLength                            = 0")
        if current_pos < block_end:
            # Match Copy
            match_length = match_token + 4
            match_offset = file[current_pos] + (file[current_pos + 1] << 8)
            current_pos += 2
            # print("matchOffset                              = " + str(hex(match_offset))[2:])

            if match_token == 15:
                # Extend Match Length
                while True:
                    v = file[current_pos]
                    match_length += v
                    current_pos += 1
                    if v != 255:
                        break

            # Match Copy
            for i in range(match_length):
                # pass
                result.append(result[len(result) - match_offset])
                # result += [result[len(result) - match_offset]]
                # result += '\0'
    return result
