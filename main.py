#!/bin/env python3
import os
# import shutil
import argparse
from ytp_parser import *
from expr_parser import *
import yu 
from func import *

if __name__ == "__main__":
    print("YTP_NEXT v4.2.0")
    print("---------------")
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', type=str, required=True, help='Folder that contains the yu-ris files')
    parser.add_argument('-o', '--output', dest='output', type=str, required=True, help='Folder where to drop the generated ren\'py files')
    parser.add_argument('-d', '--debug', action='store_true', help='Let the program yap about what it\'s doing behind the scenes')
    args = parser.parse_args()

    project_dir = os.path.dirname(os.path.realpath(__file__))

    # Sanity check since the user might be insane
    if not os.path.exists(args.input):
        print("The folder you specified DOESN'T EXIST? WHAT!")
        print(f"Tried to access: {args.input}")
        quit()

    YSCF = readExtractYSCF(args.input)
    YSTL = readExtractYSTL(args.input, YSCF['caption'])
    YSLB = readExtractYSLB(args.input)
    YSVR = readExtractYSVR(args.input)
    YSCM = readExtractYSCM(args.input)

    if args.debug:
        debug_path = os.path.join(project_dir, "debug", sanitizePath(YSCF['caption']))
        makeDirs(debug_path)


        with open(os.path.join(debug_path, "yst_list.ytp"), 'w') as f:
            f.write(prettyDict(YSTL))

        with open(os.path.join(debug_path,"ysl.ytp"), 'w') as f:
            f.write(prettyDict(YSLB))

        with open(os.path.join(debug_path, "ysv.ytp"), 'w') as f:
            f.write(prettyDict(YSVR))

        with open(os.path.join(debug_path, "yscfg.ytp"), 'w') as f:
            f.write(prettyDict(YSCF))

        with open(os.path.join(debug_path, "ysc.ytp"), 'w') as f:
            f.write(prettyDict(YSCM))

    # Read all yst00*.ybn files, excluding eris
    shared_resources = {
        'bg_list': [],
        'ev_list': [],
        'st_list': [],
        'sound_list': []
    }

    for script in YSTL['scripts']:
        if not "userscript" in script['path']:
            pass
        else:
            yst_index_name = "yst" + str(script['index']).zfill(5) + ".ybn"
            
            YSTB = readExtractYSTB(os.path.join(args.input, yst_index_name))
            
            if args.debug:
                debug_path_script = os.path.join(debug_path, *script['path'].split("\\")[2:-1])
                makeDirs(debug_path_script)

                debug_name_script = str(script['index']).zfill(5) + "_" + script['path'].split("\\")[-1]

                with open(os.path.join(debug_path_script, debug_name_script + ".ytp"), 'w') as f:
                    f.write(prettyDict(YSTB))
                yap(f"Wrote {os.path.join(debug_path_script, debug_name_script)}", True)

            # try:
            if YSTB is not False:
                parsed = instructionParser(script['index'], YSTB, YSCM, YSTL, YSVR, YSLB)
                
                if args.debug:
                    with open(os.path.join(debug_path_script, debug_name_script + ".yuris"), 'w') as f:
                        f.write(yurisPrint(parsed))
                    yap(f"Wrote {os.path.join(debug_path_script, debug_name_script + ".yuris")}", True)

                    with open(os.path.join(debug_path_script, debug_name_script + ".parsed"), 'w') as f:
                        f.write(prettyDict(parsed))
                    yap(f"Wrote {os.path.join(debug_path_script, debug_name_script + ".parsed")}", True)
                
                #real ytp
                renpy, shared_resources = yu.topy(parsed, shared_resources)
                with open(os.path.join(args.output, os.path.splitext(debug_name_script)[0] + ".rpy"), 'w') as f:
                    f.write(renpy)
                yap(f"Wrote {os.path.join(args.output, os.path.splitext(debug_name_script)[0] + ".rpy")}", True)

    #writing the shared resources (man those functions are trash)
    shared_resources['bg_list'] = list(dict.fromkeys(shared_resources['bg_list']))
    shared_resources['ev_list'] = list(dict.fromkeys(shared_resources['ev_list']))
    shared_resources['st_list'] = list(dict.fromkeys(shared_resources['st_list']))

    with open(os.path.join(project_dir, "renpy_resources.rpy"), 'r') as f:
        helper_file = f.read()
    with open(os.path.join(args.output, "renpy_resources.rpy"), 'w') as f:
        f.write(f"{helper_file}\n    shared_resources = {repr(shared_resources)}\n    yu_bg(shared_resources)\n    yu_ev(shared_resources)\n    yu_st(shared_resources)")