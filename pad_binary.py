import os
from pathlib import Path
import argparse

def append_nops_to_executable(file_path, num_nops, output_file):
    nop = b'\x90'  # NOP opcode in x86 assembly
    try:
        with open(file_path, 'rb') as original_file:
            data = original_file.read()
            data += nop * num_nops  # Append the specified number of NOPs

        with open(output_file, 'wb') as modified_file:
            modified_file.write(data)

        print(f"Successfully appended {num_nops} NOPs to {file_path}. Output file: {output_file}")
    except IOError as e:
        print(f"Error: {e}")

def process_folder(target_folder, num_nops):
    target_folder = Path(target_folder)
    modded_folder = target_folder / "modded"

    if not modded_folder.exists():
        modded_folder.mkdir()

    for file in target_folder.iterdir():
        if file.is_file():
            output_file = modded_folder / f"{file.stem}_modded{file.suffix}"
            append_nops_to_executable(file, num_nops, output_file)

def process_single_file(file_path, num_nops):
    file = Path(file_path)
    output_file = file.parent / f"{file.stem}_modded{file.suffix}"
    append_nops_to_executable(file, num_nops, output_file)

def main():
    parser = argparse.ArgumentParser(
        description="Append NOPs to executables.",
        epilog="""
        Examples of usage:
        
        To process an entire folder:
          python pad_binary.py /path/to/target_folder --num_nops 15

        To process a single file:
          python pad_binary.py /path/to/target_file --num_nops 15 --single_file
        """
    )
    parser.add_argument("target_path", type=str, help="Path to the target folder or file.")
    parser.add_argument("--num_nops", type=int, default=10, help="Number of NOP bytes to append. Default is 10.")
    parser.add_argument("--single_file", action="store_true", help="Process a single file instead of a folder.")
    
    args = parser.parse_args()
    
    target_path = args.target_path
    num_nops = args.num_nops
    single_file = args.single_file

    if single_file:
        process_single_file(target_path, num_nops)
    else:
        process_folder(target_path, num_nops)

if __name__ == "__main__":
    main()
