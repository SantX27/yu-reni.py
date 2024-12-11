def topy(script, shared_resources):
    renpy_head = ""
    renpy_script = ""
    for num_instruction,instruction in enumerate(script):
        match instruction['type']:
            case "label":
                 #Ren'py doesn't like labels with numbers at the start.
                 renpy_script += f"label yu_{instruction['value']}:\n"
            case "instruction":
                match instruction['opcode']:
                    case "_":
                        #TODO fix and map variable text (0x56)
                        if not "UNMAPPED" in instruction['attributes'][0]['attrib_values'][0]:
                            renpy_script += f"{instruction['attributes'][0]['attrib_values'][0]}\n"

                    case "GO":
                        if "\"" in instruction['attributes'][0]['attrib_values'][0]:
                            renpy_script += f"jump yu_{instruction['attributes'][0]['attrib_values'][0].replace("\"", "")}\n"
                    
                    case "GOSUB":
                        match instruction['attributes'][0]['attrib_values'][0].replace("\"", ""):
                            case "ES.SEL.GO": # Choice select and jump
                                #We need to find the respective ES.SEL.SET, then process them together
                                for es_sel_set in script[num_instruction:]:
                                    try:
                                        if "ES.SEL.SET" in es_sel_set['attributes'][0]['attrib_values'][0]:
                                            renpy_script += f"menu:\n"
                                            for num_attrib, go_attrib in enumerate(instruction['attributes']):
                                                if "PSTR" in go_attrib['argument'] and "''" not in go_attrib["attrib_values"][0]:
                                                    sel_text = es_sel_set['attributes'][num_attrib]['attrib_values'][0]
                                                    sel_jump = go_attrib["attrib_values"][0].replace("\"", "")
                                                    renpy_script += "  " + sel_text + ":\n"
                                                    renpy_script += f"    jump yu_{sel_jump}\n"
                                                    #print(f"Jump: {go_attrib["attrib_values"][0]}, Text: {es_sel_set['attributes'][num_attrib]['attrib_values'][0]}")
                                            break
                                    except IndexError:
                                        pass
                            case "MAC.BG": # Set scene background
                                attrib_list = []
                                #Process all attributes
                                for attribute in instruction['attributes']:
                                    #Process changesign
                                    try:
                                        if "vm_changesign" in attribute['attrib_values'][1]:
                                            value = -int(attribute['attrib_values'][0])
                                    except (IndexError, TypeError):
                                        if type(attribute['attrib_values'][0]) == str:
                                            value = attribute['attrib_values'][0].replace("\"", "")
                                        else:
                                            value = attribute['attrib_values'][0]
                                    attrib_list.append(value)
                                if not "UNMAPPED" in attrib_list[1]:
                                    #renpy_head += f"yu_bg(\"{attrib_list[1]}\")\n"
                                    renpy_script += f"scene bg {attrib_list[1]}\n"
                                    shared_resources['bg_list'].append(attrib_list[1])
                                #renpy_script += f"$ dyn_bg_name = \"{attrib_list[1]}\"\n"
                            # case "es.SND": # Play sound
                            #     attrib_list = []
                            #     #Process all attributes
                            #     for attribute in instruction['attributes']:
                            #         #Process changesign
                            #         try:
                            #             if "vm_changesign" in attribute['attrib_values'][1]:
                            #                 value = -int(attribute['attrib_values'][0])
                            #         except (IndexError, TypeError):
                            #             if type(attribute['attrib_values'][0]) == str:
                            #                 value = attribute['attrib_values'][0].replace("\"", "")
                            #             else:
                            #                 value = attribute['attrib_values'][0]
                            #         attrib_list.append(value)
                            #     if not "UNMAPPED" in attrib_list[1]:
                            #         #renpy_head += f"yu_bg(\"{attrib_list[1]}\")\n"
                            #         renpy_script += f"play yu_{attrib_list[1]} \n"
                            #         shared_resources['ev_list'].append(attrib_list[1])
                            case "es.WA.SET": # Pause the script for a while
                                renpy_script += f"pause {instruction['attributes'][1]['attrib_values'][0]/1000}\n"
                            case "MAC.EV": # Set scene background
                                attrib_list = []
                                #Process all attributes
                                for attribute in instruction['attributes']:
                                    #Process changesign
                                    try:
                                        if "vm_changesign" in attribute['attrib_values'][1]:
                                            value = -int(attribute['attrib_values'][0])
                                    except (IndexError, TypeError):
                                        if type(attribute['attrib_values'][0]) == str:
                                            value = attribute['attrib_values'][0].replace("\"", "")
                                        else:
                                            value = attribute['attrib_values'][0]
                                    attrib_list.append(value)
                                if not "UNMAPPED" in attrib_list[1]:
                                    #renpy_head += f"yu_ev(\"{attrib_list[1]}\")\n"
                                    renpy_script += f"scene ev {attrib_list[1]}\n"
                                    shared_resources['ev_list'].append(attrib_list[1])
                            case "es.SP.ST.SET": # Set sprites
                                attrib_list = []
                                #Process all attributes
                                for attribute in instruction['attributes']:
                                    #Process changesign
                                    try:
                                        if "vm_changesign" in attribute['attrib_values'][1]:
                                            value = -int(attribute['attrib_values'][0])
                                    except (IndexError, TypeError):
                                        if type(attribute['attrib_values'][0]) == str:
                                            value = attribute['attrib_values'][0].replace("\"", "")
                                        else:
                                            value = attribute['attrib_values'][0]
                                    attrib_list.append(value)
                                if not "UNMAPPED" in attrib_list[2]:
                                    #renpy_head += f"yu_ev(\"{attrib_list[1]}\")\n"
                                    renpy_script += f"show {attrib_list[2].lower()}\n"
                                    shared_resources['st_list'].append(attrib_list[2])


    script_file = f"{renpy_head}\n{renpy_script}"

    return script_file, shared_resources