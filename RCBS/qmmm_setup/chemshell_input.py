#import sys
#sys.path.append("..") # Adds higher directory to python modules path.

from RCBS.exceptions import NotExistingMetalError

import yaml


""" TO-DO
    - [ ] Wrap all functions that create parts of the input into a Class

"""

basis_dict = {
    '6-31g' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ti'],
    '6-31G' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ti'],
    'cc-pvdz' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'ga', 'ge', 'as', 'se', 'br', 'kr'],
    'stuttgart_rsc' : ['k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'cs', 'ba', 'ce', 'pr', 'nd', 'pm', 'sm', 'eu', 'gd', 'tb', 'dy', 'ho', 'er', 'tm', 'yb', 'hf', 'ta', 'w', 're', 'os', 'ir', 'pt', 'au', 'hg', 'ti', 'ac', 'th', 'pa', 'u', 'np', 'pu', 'am', 'cm', 'bk', 'cf', 'es', 'fm', 'md', 'no', 'lr', 'db'],
    'lanl2dz' : ['h', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ba', 'la', 'hf', 'ta', 'w', 're', 'os', 'ir', 'pt', 'au', 'ti', 'u', 'np', 'pu'],
    'sto-3g' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'ti'],
    '6-31++g**' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar'],
    '6-31++G(d,p)' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar'],
    '6-31g*' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ti'],
    '6-31G(d)' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ti'],
    'ahlrichs_vdz' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'ti'],
    'sbkjc_vdz' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ba', 'la', 'ce', 'hf', 'ta', 'w', 're', 'os', 'ir', 'pt', 'au', 'hg', 'ti', 'pb', 'bi', 'po', 'at', 'rn'],
    'sadlej' : ['h', 'li', 'be', 'c', 'n', 'o', 'f', 'na', 'mg', 'si', 'p', 's', 'cl', 'k', 'ca', 'br', 'rb', 'sr', 'i'],
    'dzp' : ['h', 'li', 'b', 'c', 'n', 'o', 'f', 'ne', 'al', 'si', 'p', 's', 'cl'],
    '3-21g' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ti'],
    '3-21G' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ti'],
    'stuttgart_rlc' : ['li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ba', 'hg', 'pb', 'bi', 'po', 'at', 'rn', 'ac', 'th', 'pa', 'u', 'np', 'pu', 'am', 'cm', 'bk', 'cf', 'es', 'fm', 'md', 'no', 'lr'],
    'ahlrichs_vtz' : ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'ti']
}

basis_atoms = ['ac', 'ag', 'al', 'am', 'ar', 'as', 'at', 'au', 'b', 'ba', 'be', 'bi', 'bk', 'br', 'c', 'ca', 'cd', 'ce', 'cf', 'cl', 'cm', 'co', 'cr', 'cs', 'cu', 'db', 'dy', 'er', 'es', 'eu', 'f', 'fe', 'fm', 'ga', 'gd', 'ge', 'h', 'he', 'hf', 'hg', 'ho', 'i', 'in', 'ir', 'k', 'kr', 'la', 'li', 'lr', 'md', 'mg', 'mn', 'mo', 'n', 'na', 'nb', 'nd', 'ne', 'ni', 'no', 'np', 'o', 'os', 'p', 'pa', 'pb', 'pd', 'pm', 'po', 'pr', 'pt', 'pu', 'rb', 're', 'rh', 'rn', 'ru', 's', 'sb', 'sc', 'se', 'si', 'sm', 'sn', 'sr', 'ta', 'tb', 'tc', 'te', 'th', 'ti', 'tm', 'u', 'v', 'w', 'xe', 'y', 'yb', 'zn', 'zr']

hamiltonian = {
    'turbomole' : ['hf', 'mp2', 'cc2', 'lda', 'blyp', 'bp86', 'pbe', 'tpss', 'b3lyp', 'b3lyp_G', 'bhlyp', 'pbe0', 'tpssh'],
    'gaussian' : ['hf', 'blyp', 'bp86', 'b3lyp', 'b3p86', 'b3pw91', 'bpw91', 's-vwn', 'lda', 'casscf'],
}

def yaml2dict(default_yaml, user_yaml):
    """
    DESCRIPTION:
        Function which creates a dictionary from the user-input YAML completing the not defined keyword with the default configuration from the default YAML.
    TO-DO
        - [ ] Create checker for inputs
    """

    default_dict = yaml.safe_load(open(default_yaml))
    user_dict = yaml.safe_load(open(user_yaml))


    for key in list(default_dict.keys()):
        if key not in ('calculation_features', 'theory'):
            try :
                default_dict[key] = user_dict[key]
            except KeyError:
                pass

        else :
            for key_ in list(default_dict[key].keys()):
                try :
                    default_dict[key][key_] = user_dict[key][key_]
                except KeyError:
                    pass

    return default_dict, yaml.safe_load(open(default_yaml))


def dict_checker(input_dict, default_dict):
    """
    DESCRIPTION:
        Function for checking the values introduced in the input yaml. All non recognised values will be substituted by the values from the default configuration.

    TO-DO:
        - [ ] Add other QM packages than turbomole and gaussian
    """

    """
    if default_dict = None:
        default_dict = {
            'name': None, 
            'type': 'opt', 
            'input_files': {
                'coordinates': None, 
                'topology': None, 
                'pdb': None, 
                'coords_chemsh': None, 
                'active_atoms': None
                }, 
            'calculation_features': {
                'optimiser': 'lbgs', 
                'coordinates': 'hdlc', 
                'tolerance': 0.001, 
                'microiterative': None
                }, 
            'theory': {
                'software': 'turbomole', 
                'qmmm_embedding': 'electrostatic', 
                'qm_region': 'qm_list', 
                'hamiltonian': 'b3lyp', 
                'electronic_configuration': 'closed', 
                'basis': '6-31G(d)', 
                'metal': 'fe', 
                'metal_basis': 'lanl2dz', 
                'charge': 0, 
                'multiplicity': 1, 
                'extra': None
                }
            }
    """

    # Values checker
    ## calculation_features
    ### optimiser
    if input_dict['calculation_features']['optimiser'].lower() not in ('lbfgs', 'prfo', 'dimer'):
        print('The selected optimiser is not implemented. %s has been selected instead' % default_dict['calculation_features']['optimiser'])
        input_dict['calculation_features']['optimiser'] = default_dict['calculation_features']['optimiser']

    ### coordinates
    if input_dict['calculation_features']['coordinates'].lower() not in ('hdlc', 'cartesian', 'dlc'):
        print('The selected coordinates system is not implemented. %s has been selected instead' % default_dict['calculation_features']['coordinates'])
        input_dict['calculation_features']['coordinates'] = default_dict['calculation_features']['coordinates']

    ### tolerance
    try :
        float(input_dict['calculation_features']['tolerance'])
    except ValueError:
        print('The specified tolerance is not correct. %s will be used instead.' % default_dict['calculation_features']['tolerance'])
        input_dict['calculation_features']['tolerance'] = default_dict['calculation_features']['tolerance']

    ### microiterative
    if input_dict['calculation_features']['microiterative'] != None:
        if isinstance(input_dict['calculation_features']['microiterative'], str):
            if input_dict['calculation_features']['microiterative'].find(',') != -1: # splitting with , in case of it is a comma-separated list
                input_dict['calculation_features']['microiterative'] = input_dict['calculation_features']['microiterative'].split(',')
            else :
                input_dict['calculation_features']['microiterative'] = input_dict['calculation_features']['microiterative'].split(' ')


        if isinstance(input_dict['calculation_features']['microiterative'], list):
            for i in range(len(input_dict['calculation_features']['microiterative'])):
                try :
                    input_dict['calculation_features']['microiterative'][i] = str(int(input_dict['calculation_features']['microiterative'][i]))
                except ValueError:
                    print('Residue %s of the microiterative scheme is not a residue. It will be removed.')
                    input_dict['calculation_features']['microiterative'][i] = ' '
            
            if input_dict['calculation_features']['microiterative'].count(' ') == len(input_dict['calculation_features']['microiterative']):
                print('No residue is valid for microiterative scheme, so it will be deactivated.')
                input_dict['calculation_features']['microiterative'] = None
            else :
                input_dict['calculation_features']['microiterative'] = ' '.join(input_dict['calculation_features']['microiterative'])


    ## theory
    ### software
    if input_dict['theory']['software'] not in ('gaussian', 'turbomole'):
        print('The chosen software is not available. %s will be used instead.' % default_dict['theory']['software'])
        input_dict['theory']['software'] = default_dict['theory']['software']

    ### coupling
    if input_dict['theory']['qmmm_embedding'].lower() not in ('electrostatic', 'mechanical'):
        print('The selected coupling does not exist or is not usable in ChemShell. %s embedding will be used instead.' % default_dict['theory']['qmmm_embedding'])
        input_dict['theory']['qmmm_embedding'] = default_dict['theory']['qmmm_embedding']

    ### hamiltonian
    if input_dict['theory']['hamiltonian'].lower() not in hamiltonian[input_dict['theory']['software']]:
        print('The selected hamiltonian does not exist or it is not usable in the selected QM package. %s hamiltonian will be used instead.' % default_dict['theory']['qmmm_embedding'])
        input_dict['theory']['hamiltonian'] = default_dict['theory']['hamiltonian']

    ### electronic_configuration
    if input_dict['theory']['electronic_configuration'] not in ('closed', 'open'):
        print('The selected electronic configuration does not exist. %s will be used instead.' % default_dict['theory']['electronic_configuration'])
        input_dict['theory']['electronic_configuration'] = default_dict['theory']['electronic_configuration']

    ### basis
    if input_dict['theory']['basis'] not in basis_dict.keys():
        print('The selected basis set for all atoms is not available. The default one will be used instead.')
        input_dict['theory']['basis'] = default_dict['theory']['basis']

    #### metal
    if input_dict['theory']['metal'] != None:
        if input_dict['theory']['metal'] in basis_atoms:
            if input_dict['theory']['metal'] not in basis_dict[input_dict['theory']['metal_basis']]:
                print('The basis set is not available for the selected metal. %s will be used instead.' % default_dict['theory']['metal_basis'])
                input_dict['theory']['metal_basis'] = default_dict['theory']['metal_basis']

        else :
            #print('There is no basis set available for the selected metal. Check the input file.')
            raise NotExistingMetalError
    

    ### charge
    try :
        int(input_dict['theory']['charge'])
    except ValueError:
        print('Charge for QM region is not valid.')

    ### multiplicity
    try :
        int(input_dict['theory']['multiplicity'])
    except ValueError:
        print('Multiplicity for QM region is not valid.')


    return input_dict


def header(dict_):
    """
    DESCRIPTION:
        Function for creating the header of the Chemshell input files.

    TO-DO:
        - [ ] When the config.yaml function is ready, read the ChemShell DIR and the software to adapt the tcl importing routes.
    """

    header_string = '''global sys_name_id
source ./{0}
source ./{1}
source /QFsoft/applic/CHEMSHELL/3.7/intel2017-serial/src/interface_turbomole/turbomole.tcl
source /QFsoft/applic/CHEMSHELL/3.7/intel2017-serial/src/interface_amber/parse_amber.tcl
set dir .
set sys_name_id {2}'''.format(
        dict_['input_files']['active_atoms'],
        dict_['theory']['qm_region'],
        dict_['name'])
    
    ## by now it is made for working on Picard

    return header_string


def residues(dict_):
    """
    DESCRIPTION:
        Function for creating the piece of code that creates a list of residues and the contained atoms. It is needed only when using HDLC coordinates.
    """

    if dict_['calculation_features']['coordinates'].lower() == 'hdlc':
        residues_string = """\n\nset pdbresidues [ pdb_to_res "%s" ]
set fil [open "pdbresidues" {RDWR CREAT TRUNC}]
puts $fil "set pdbresidues [ list $pdbresidues ]"
close $fil\n
    """ % dict_['input_files']['pdb']

    else :
        residues_string = ''

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
        residues_option = '\n            residues= $pdbresidues \\'
    else :
        residues_option = ''

    calculation_string = '''
dl-find coords= {0} \\
        result= ${{sys_name_id}}.c \\{1}
        coordinates= {2} \\
        optimizer= {3} \\
        active_atoms= {4} \\
        maxene= 100000 \\
        tolerance= {5} \\
        maxstep= 0.1 \\
        lbfgs_mem= 1000 \\
        list_option= none \\\n'''.format(
        coords, #coords
        residues_option, #residues
        dict_['calculation_features']['coordinates'].lower(), #coordinates
        dict_['calculation_features']['optimiser'].lower(), #optimser
        dict_['input_files']['active_atoms'], #act
        str(dict_['calculation_features']['tolerance'])) #tolerance
    

    
    if dict_['calculation_features']['microiterative'] != None:
        calculation_string = calculation_string + "            microiterative= yes \\\n            inner_residues=  { %s } \\\n" % dict_['calculation_features']['microiterative']

    return calculation_string


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

