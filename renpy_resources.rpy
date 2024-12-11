#stolen from katawa shoujo
init python:
    def yu_bg(shared_resources):
        for bgid in shared_resources['bg_list']:

            path = "images/cg/bg/"
            tag = "bg"
            
            base_image = path + bgid + ".png"
            
            if not renpy.loadable(base_image):
                base_image = "images/default.png"
            renpy.image((tag,bgid), base_image)

    def yu_ev(shared_resources):
        for evid in shared_resources['ev_list']:

            path = "images/cg/ev/"
            tag = "ev"
            
            base_image = path + evid + ".png"
            
            if not renpy.loadable(base_image):
                base_image = "images/default.png"
            renpy.image((tag,evid), base_image)

    def yu_st(shared_resources):
        for stid in shared_resources['st_list']:

            path = "images/cg/stand/"

            if("nem" in stid):
                path = "images/cg/stand/01_nem/"
            elif("kan" in stid):
                path = "images/cg/stand/02_kan/"
            elif("rin" in stid):
                path = "images/cg/stand/03_rin/"
            elif("rik" in stid):
                path = "images/cg/stand/04_rik/"
            elif("nat" in stid):
                path = "images/cg/stand/05_nat/"
            elif("miy" in stid):
                path = "images/cg/stand/11_miy/"
            elif("mb1" in stid):
                path = "images/cg/stand/12_mb1/"
            elif("mb2" in stid):
                path = "images/cg/stand/13_mb2/"
            elif("mg1" in stid):
                path = "images/cg/stand/14_mg1/"
            elif("mg2" in stid):
                path = "images/cg/stand/15_mg2/"

            base_image = path + stid + ".png"
            
            if not renpy.loadable(base_image):
                base_image = "images/default.png"
            renpy.image((stid), base_image)

    ex_m_tracks = []
    def ks_music(shared_resources):
        fullpath = "bgm/" + filename + ".ogg"
        setattr(store, "music_" + alias, fullpath)
        store.ex_m_tracks.append((filename.replace("_", " "), fullpath))

    for i in range(99):
        renpy.music.register_channel(f"yu_{i}")