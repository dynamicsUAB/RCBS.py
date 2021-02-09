import yaml

""" TO-DO
    - [ ] Wrap all functions that create parts of the input into a Class

"""

basis_dict = {
    '6-31g' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ti'],
    'cc-pvdz' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'ga', 'ge', 'as', 'se', 'br', 'kr'],
    'stuttgart_rsc' : ['k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'cs', 'ba', 'ce', 'pr', 'nd', 'pm', 'sm', 'eu', 'gd', 'tb', 'dy', 'ho', 'er', 'tm', 'yb', 'hf', 'ta', 'w', 're', 'os', 'ir', 'pt', 'au', 'hg', 'ti', 'ac', 'th', 'pa', 'u', 'np', 'pu', 'am', 'cm', 'bk', 'cf', 'es', 'fm', 'md', 'no', 'lr', 'db'],
    'lanl2dz' : ['h', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ba', 'la', 'hf', 'ta', 'w', 're', 'os', 'ir', 'pt', 'au', 'ti', 'u', 'np', 'pu'],
    'sto-3g' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'ti'],
    '6-31++g**' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar'],
    '6-31g*' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ti'],
    'ahlrichs_vdz' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'ti'],
    'sbkjc_vdz' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ba', 'la', 'ce', 'hf', 'ta', 'w', 're', 'os', 'ir', 'pt', 'au', 'hg', 'ti', 'pb', 'bi', 'po', 'at', 'rn'],
    'sadlej' : ['h', 'li', 'be', 'c', 'n', 'o', 'f', 'na', 'mg', 'si', 'p', 's', 'cl', 'k', 'ca', 'br', 'rb', 'sr', 'i'],
    'dzp' : ['h', 'li', 'b', 'c', 'n', 'o', 'f', 'ne', 'al', 'si', 'p', 's', 'cl'],
    '3-21g' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ti'],
    'stuttgart_rlc' : ['li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ba', 'hg', 'pb', 'bi', 'po', 'at', 'rn', 'ac', 'th', 'pa', 'u', 'np', 'pu', 'am', 'cm', 'bk', 'cf', 'es', 'fm', 'md', 'no', 'lr'],
    'ahlrichs_vtz' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'ti']
}

def yaml2dict(default_file, user_file):
    """
    Function which creates a dictionary from the user-input YAML completing the not defined keyword with the default configuration from the default YAML.
    """

    qmmm_dict = yaml.safe_load(open(default_file))
    user_dict = yaml.safe_load(open(user_file))

    keys = list(user_dict.keys())

    for i in range(len(keys)):
        if keys[i] in ('name', 'type', 'input_files'):
            qmmm_dict[keys[i]] = user_dict[keys[i]]

        else :
            if keys[i] in ('calculations_features', 'theory'):
                keys_ = list(user_dict[keys[i]].keys())

                for j in range(len(keys_)):
                    qmmm_dict[keys[i]][keys_[j]] = user_dict[keys[i]][keys_[j]]


    for i in range(len(keys)):
        if keys[i] in ('calculations_features', 'theory'):
            keys_ = list(user_dict[keys[i]].keys())

            for key in range(len(keys_)):
                if keys_ == 'optimiser' and qmmm_dict[keys[i]][keys_[j]] not in ('lbfgs', 'prfo', 'dimer'):
                    print('The selected optimiser is not implemented. L-BFGS has been selected instead')
                    qmmm_dict[keys[i]][keys_[j]] = 'lbgfs'

                elif keys_ == 'coordinates' and qmmm_dict[keys[i]][keys_[j]] not in ('hdlc', 'cartesian', 'dlc'):
                    print('The selected coordinates system is not implemented. HDLC has been selected instead')
                    qmmm_dict[keys[i]][keys_[j]] = 'hdlc'

                elif keys_ == 'tolerance' and (not isinstance(qmmm_dict[keys[i]][keys_[j]], float)):
                    print('The default value of 0.001 has been used as tolerance.')
                    qmmm_dict[keys[i]][keys_[j]] = 0.001

                #elif keys_ == 'microiterative' and str(qmmm_dict[keys[i]][keys_[j]]).lower() not in ('yes', 'no'):#, 'y', 'n', 'true', 'false'):
                #    if str(qmmm_dict[keys[i]][keys_[j]]).lower() in ('y', 'true'):
                #        qmmm_dict[keys[i]][keys_[j]] = 'yes'
                #    elif str(qmmm_dict[keys[i]][keys_[j]]).lower() in ('n', 'false'):
                #        qmmm_dict[keys[i]][keys_[j]] = 'no'
                #    else :
                #        print('Microiterative has been deactivated.')
                #        qmmm_dict[keys[i]][keys_[j]] = 'no'

    return qmmm_dict, user_dict



def yaml2dict2(default_file, user_file):
    """
    DEXCRIPTION:
        Function which creates a dictionary from the user-input YAML completing the not defined keyword with the default configuration from the default YAML.
    TO-DO
        - [ ] Create checker for inputs
    """

    qmmm_dict = yaml.safe_load(open(default_file))
    user_dict = yaml.safe_load(open(user_file))



    for key in list(qmmm_dict.keys()):
        if key not in ('calculation_features', 'theory'):
            try :
                qmmm_dict[key] = user_dict[key]
            except KeyError:
                pass

        else :
            for key_ in list(qmmm_dict[key].keys()):
                try :
                    qmmm_dict[key][key_] = user_dict[key][key_]
                except KeyError:
                    pass



    return qmmm_dict

def theory(dict_):
    """
    Function for creating the theory section of the ChemShell input file.
    """

    def coupling(dict_=dict_):
        # QM-MM coupling specification
        if dict_['theory']['qmmm_embedding'] == 'electrostatic':
            coupling = 'shift'
        elif dict_['theory']['qmmm_embedding'] == 'mechanical':
            coupling = 'mechanical'

        return coupling

    def basis_spec(dict_=dict_):
        # basisspec specification
        if dict_['theory']['metal'] == None:
            if dict_['theory']['basis'].lower() == '6-31g(d)':
                basis_spec = '{ { 6-31g* * } }'
            elif dict_['theory']['basis'].lower() == '6-31++g(d,p)':
                basis_spec = '{ { 6-31++g** * } }'
            else :
                if dict_['theory']['basis'].lower() in basis_dict.keys():
                    basis_spec = '{ { %s * } }' % dict_['theory']['basis'].lower()
                else :
                    print('The specified basis set does not exist. 6-31G(d) will be used instead')
                    basis_spec = '{ { 6-31g* * } }'

        elif dict_['theory']['metal'] != None:
            if dict_['theory']['metal_basis'].lower() in basis_dict.keys():
                if dict_['theory']['metal'].lower() in basis_dict[dict_['theory']['metal_basis'].lower()]:
                    basis_spec = '{ { %s %s } ' % (dict_['theory']['metal_basis'].lower(), dict_['theory']['metal'].lower())
                else :
                    print('This basis cannot be used with this metal')
            else :
                print('The specified basis set cannot be used. ')

            if dict_['theory']['basis'].lower() == '6-31g(d)':
                basis_spec = basis_spec + '{ 6-31g* * } }'
            elif dict_['theory']['basis'].lower() == '6-31++g(d,p)':
                basis_spec = basis_spec + '{ 6-31++g** * } }'
            else :
                if dict_['theory']['basis'].lower() in basis_dict.keys():
                    basis_spec = basis_spec +  '{ %s * } }' % dict_['theory']['basis'].lower()
                else :
                    print('The specified basis set does not exist. 6-31G(d) will be used instead')
                    basis_spec = basis_spec + '{ 6-31g* * } }'


        return basis_spec

    def scftype(dict_=dict_):
        if dict_['theory']['electronic_configuration'] == 'closed':
            scftype = 'rhf'
        elif dict_['theory']['electronic_configuration'] == 'open':
            scftype = 'uhf'

        return scftype

    def qm_region(dict_=dict_):
        if isinstance(dict_['theory']['qm_region'], str):
            qm_region = dict_['theory']['qm_region']
        elif isinstance(dict_['theory']['qm_region'], list):
            qm_region = 'set qm_region { '
            for i in range(len(dict_['theory']['qm_region'])):
                qm_region = qm_region + dict_['theory']['qm_region'][i] + ' '

            qm_region = qm_region + '}'

        return qm_region





    theory_string = '''        theory= hybrid : [ list \\
                            coupling=  %s \\
                            debug= no \\
                            qm_region=  %s \\
                            qm_theory=  %s : [ list  \\
                                                    hamiltonian=  %s \\
                                                    scftype=  %s \\
                                                    basisspec=  %s \\
                                                    maxcyc= 10000 \\
                                                    charge= %s mult= %s] \\
                            mm_theory=dl_poly : [ list \\
                                                    conn= %s \\
                                                    list_option=none \\
                                                    debug=no \\
                                                    scale14 = [ list [ expr 1 / 1.2 ] 0.5  ] \\
                                                    amber_prmtop_file=  %s ]]''' % (

    coupling(),
    qm_region(),
    dict_['theory']['software'],
    dict_['theory']['hamiltonian'],
    scftype(),
    basis_spec(),
    dict_['theory']['charge'],
    dict_['theory']['multiplicity'],
    dict_['input_files']['coords_chemsh'],
    dict_['input_files']['topology'])




    return theory_string


def header(dict_):
    """
    DESCRIPTION:
        Function for creating the header of the Chemshell input files.

    TO-DO:
        - [ ] When the config.yaml function is ready, read the ChemShell DIR and the software to adapt the tcl importing routes.
    """

    header_string = '''global sys_name_id
        source ./%s
        source ./%s
        source /QFsoft/applic/CHEMSHELL/3.7/intel2017-serial/src/interface_turbomole/turbomole.tcl
        source /QFsoft/applic/CHEMSHELL/3.7/intel2017-serial/src/interface_amber/parse_amber.tcl
        set dir .
        set sys_name_id %s
    ''' % {
        dict_['input_files']['active_atoms'],
        dict_['theory']['qm_region'],
        dict_['name']
    }
    ## by now it is made for working on Picard

    return header_string

def residues(dict_):

    """
    DESCRIPTION:
        Function for creating the piece of code that creates a list of residues and the contained atoms. It is needed only when using HDLC coordinates.
    """

    residues_string = """
        set pdbresidues [ pdb_to_res "%s" ]
        set fil [open "pdbresidues" {RDWR CREAT TRUNC}]
        puts $fil "set pdbresidues [ list $pdbresidues ]"
        close $fil
    """ % dict_['input_files']['pdb']

    return residues_string

def opt_min_calculation(dict_):
    """
    DESCRIPTION:
        Function for creating the job to carry out.
    """

    if dict_['input_files']['coords_chemsh'] == None:
        coord_string = f"load_amber_coords inpcrd={dict_['input_files']['coordinates']} prmtop={dict_['input_files']['topology']} coords=coord.c\n\n"
        coords = 'coord.c'
    else :
        coord_string = ''
        coords = dict_['input_files']['coords_chemsh']


    if dict_['calculation_features']['coordinates'].lower() == 'hdlc':
        residues_string = residues(dict_) + '\n\n'
        residues_option = 'residues= $pdbresidues \\\n'

    else :
        residues_string = ''
        residues_option = ''

    if microiterative != None:
        pass

    calculation_string = """"
        dl-find coords=%s \\
                result= ${sys_name_id}.c \\
                %s coordinates= %s \\
                optimizer= %s \\
                active_atoms= %s \\
                maxene= 100000 \\
                tolerance= %s \\
                maxstep= 0.1 \\
                lbfgs_mem= 1000 \\
                list_option= none \\
    """ % {
        coords,
        residues_option,
        dict_['calculation_features']['coordinates'].lower(),
        dict_['input_files']['']
    }

    """
                microiterative= yes \\
                inner_residues=  { 250 255 430 434 552 553 554 555 } \\
    """