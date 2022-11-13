# Final script to perform embedding on all images

import argparse
from pathlib import Path
from shutil import copy

from rsa_main import main as RSA_main
from pvd_main import main as PVD_main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--embed", "-e", action = "store_true", help = "Embedding all images from dataset")
    group.add_argument("--extract", "-d", action = "store_true", help = "Extracting secret message from all Embedded Images")

    args = parser.parse_args()
    if args.embed:
        # Encrypting all text files containing patient data using RSA
        src_dir = Path("./embedding")
        for fp in src_dir.iterdir():
            if fp.name.endswith(".txt") and not fp.name.startswith("encrypted"):
                out_fp = src_dir /f"encrypted_{fp.name}"
                rsa_args =argparse.Namespace(encrypt = True, input = fp, output = out_fp, decrypt = False)
                RSA_main(rsa_args)
        # Embedding encrypted text into images
        dest_dir = Path("./embedding/output")
        for fp in src_dir.iterdir():
            if fp.name.endswith(".png"):
                out_fp = dest_dir /f"embedded_{fp.name}"
                encryted_msg_fp = src_dir / f"encrypted_{fp.name.replace('.png', '.txt')}"
                pvd_args = argparse.Namespace(embed = True, ref = fp, outimage = out_fp, inmessage = encryted_msg_fp, extract = False)
                PVD_main(pvd_args)
                copy(out_fp, Path(f"./extraction/{out_fp.name}"))
    elif args.extract:
        # Extracting encrypted text into images
        src_dir = Path("./extraction")
        dest_dir = Path("./extraction/output")
        for fp in src_dir.iterdir():
            if fp.name.endswith(".png") and not fp.name.startswith("embedded"):
                embed_fp = src_dir /f"embedded_{fp.name}"
                embed_message_fp = dest_dir/ f"encrypted_{fp.name.replace('.png','.txt')}"
                pvd_args = argparse.Namespace(embed = False, ref = fp, inimage = embed_fp, outmessage = embed_message_fp, extract = True)
                PVD_main(pvd_args)
        # Decrypting all text files containing patient data using RSA
        for fp in dest_dir.iterdir():
            if fp.name.endswith(".txt") and fp.name.startswith("encrypted"):
                out_fp = dest_dir /f"decrypted_{fp.name.replace('encrypted_','')}"
                rsa_args =argparse.Namespace(encrypt = False, input = fp, output = out_fp, decrypt = True)
                RSA_main(rsa_args)
