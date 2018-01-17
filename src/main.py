import sys
import src.decoder.FrameDecoder as FrameDecoder
import src.decoder.BlockDecoder as BlockDecoder


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("""
Usage:
python lz4d.py [input_file_path] [output_file_path]
""")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        with open(input_file, "rb") as f:
            file_content = f.read()

        frame_info = FrameDecoder.decode(file_content)
        block_info = BlockDecoder.decode(file_content, frame_info['block_start'], frame_info['has_block_checksum'], frame_info['has_content_checksum'])


