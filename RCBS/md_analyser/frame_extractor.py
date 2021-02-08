from ..snippets.folders import check_folder

structure_saver = lambda sel, file_name, format: sel.write(file_name + format)


def trajectory_frame_extractor(u, frame, name='', folder='', format='.pdb'):
    """
    DESCRIPTION:
        Function for saving a frame from a trajectory loaded as a MDAnalysis Universe

    INPUTS:
        u       --> MDAnalysis Universe
                --> It has to be a trajectory.
        frame   --> it can be a single frame (input as number or string of number) or a list of frames.
        name    --> name for the output file. If more than one frame is input, outputs will be secuencially named
                --> by default, output will be saved as pdb. All formats accepted by the write module of MDAnalysis are accepted.
        folder  --> folder name where pdbs have to be saved.
                --> if the folder does not exist, it will be created.
                --> by default, no folder is used
        format  --> format for the output file
                --> by default, the format is pdb

    """

    if folder != '':
        check_folder(folder)

    sel = u.select_atoms('all')

    if isinstance(frame, list):
        f_ = 0
        for f in frame:
            f_ += 1
            u.trajectory[int(f)]
            sel = u.select_atoms('all')

            if name == '':
                file_name = folder + str(f)
            else :
                file_name = folder + name + '_' + str(f_)

            structure_saver(sel, file_name, format)

    if isinstance(frame, (str, int)):
        u.trajectory[int(frame)]

        if name == '':
            file_name = folder + str(frame)
        else :
            file_name = folder + name

        structure_saver(sel, file_name, format)




