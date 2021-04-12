from MDAnalysis import Universe
from MDAnalysis.core.groups import AtomGroup
import MDAnalysis.lib.distances as mdadist

# BOOLEAN CHECKERS
def dist_bool_output(dist, dist1, dist2=0, mode='lim'):
    """
    This function takes an input distance and the upper and lower limits or the central value and the tolerance and outputs
    if it satisfies or not the given criteria.

    modes:
        lim -> limit mode, it requires a max and a min value
        tol -> tolerance mode, it requires a central value and a min and max value
    """

    if mode == 'lim':
        if dist1 >= dist2:
            d_max, d_min = dist1, dist2
        elif dist2 > dist1:
            d_max, d_min = dist2, dist1

    elif mode == 'tol':
        d_max = dist1 + dist2
        d_min = dist1 - dist2

    return (dist <= d_max and dist > d_min)

def angle_bool_output(ang, ang1, ang2, mode='tol'):
    """
    DESCRIPTION:
        This function takes an input angle and the upper and lower limits or the central value and the tolerance and outputs
        if it satisfies or not the given criteria.
        All the input values are transformed into the (0, 360) degrees format.
        The input values have to be in degrees, not in radians. They can be transformed using the np.rad2dreg() method, for example.

    OPTIONS:
        - modes:
            - lim -> limit mode, it requires a max and a min value
            - tol -> tolerance mode, it requires a central value and a min and max value
    """

    ang, ang1, ang2 = list(map(lambda ang: ((ang + 360) % 360), [ang, ang1, ang2]))

    if mode == 'lim':
        if ang1 >= ang2:
            a_max, a_min = ang1, ang2
        elif ang2 > ang1:
            a_max, a_min = ang2, ang1

    elif mode == 'tol':
        a_max = ang1 + ang2
        a_min = ang1 - ang2

    return (ang <= a_max and ang > a_min)



# DISTANCE, ANGLE AND DIHEDRAL ANGLES MEASURERS
def dist_measure(sel1, sel2):
    """
    DESCRIPTION:
        This function outputs the minimum measured distance between the two input selections or coordinates or their combination.
    """
    from numpy import min as npmin
    from numpy import array

    if isinstance(sel1, AtomGroup):
        sel1 = sel1.positions

    if isinstance(sel2, AtomGroup):
        sel2 = sel2.positions

    return npmin(mdadist.distance_array(array(sel1), array(sel2), backend='OpenMP'))

def dihe_measure(sel1, sel2, sel3, sel4, units='degree', domain=360):
    """
    DESCRIPTION:
        This functions measures the dihedral angle between 4 specified atoms and returns the dihedral value between 0 and 360 degrees.
        The input selections have to be single atoms.

    OPTIONS:
        - units: option for selecting the output units of the dihedral
            - degree
            - rad

        - domain: option for specifying the domain of the output measures
            - 180, pi: option for -180,180 domain
            - 360, 2pi: option for 0,360 domain. Default option
    """
    from ..exceptions import NotSingleAtomSelectionError

    for sel in (sel1, sel2, sel3, sel4):
        if len(sel) != 1:
            raise NotSingleAtomSelectionError

    units = units.lower()
    domain = str(domain).lower()

    if units not in ('deg', 'degree', 'degrees', 'rad', 'radian', 'radians'):
        units = 'degree'

    if domain not in (180, 360, '180', '360', 'pi', '2pi'):
        domain = '360'


    if units in ('rad', 'radian', 'radians'):
        if domain in (180, '180', 'pi'):
            dihedral = float(mdadist.calc_dihedrals(sel1.positions, sel2.positions, sel3.positions, sel4.positions, backend='OpenMP'))
        elif domain in (360, '360', '2pi'):
            from math import pi
            dihedral = (float(mdadist.calc_dihedrals(sel1.positions, sel2.positions, sel3.positions, sel4.positions, backend='OpenMP')) + pi) % pi

    elif units in ('deg', 'degree', 'degrees'):
        from numpy import rad2deg

        if domain in (180, '180', 'pi'):
            dihedral = float(rad2deg(mdadist.calc_dihedrals(sel1.positions, sel2.positions, sel3.positions, sel4.positions, backend='OpenMP')))
        elif domain in (360, '360', '2pi'):
            from math import pi
            dihedral = (float(rad2deg(mdadist.calc_dihedrals(sel1.positions, sel2.positions, sel3.positions, sel4.positions, backend='OpenMP'))) + 360) % 360

    return dihedral

def ang_measure(sel1, sel2, sel3, units='deg', domain='180'):
    """
    DESCRIPTION:
        This functions measures the angle between 3 specified atoms and returns the value between 0 and 360 degrees.
        The input selections have to be single atoms.

    OPTIONS:
        - units: option for selecting the output units of the dihedral
            - degree
            - rad

        - domain: option for specifying the domain of the output measures
            - 180, pi: option for -180,180 domain
            - 360, 2pi: option for 0,360 domain. Default option
    """
    from ..exceptions import NotSingleAtomSelectionError

    for sel in (sel1, sel2, sel3):
        if len(sel) != 1:
            raise NotSingleAtomSelectionError


    units = units.lower()
    domain = str(domain).lower()

    if units not in ('deg', 'degree', 'degrees', 'rad', 'radian', 'radians'):
        units = 'degree'

    if domain not in (180, '180', 360, '360', 'pi', '2pi'):
        domain = '360'


    if units in ('rad', 'radian', 'radians'):
        if domain in (180, '180', 'pi'):
            angle = float(mdadist.calc_angles(sel1.positions, sel2.positions, sel3.positions, backend='OpenMP'))
        elif domain in (360, '360', '2pi'):
            from math import pi
            angle = (float(mdadist.calc_angles(sel1.positions, sel2.positions, sel3.positions, backend='OpenMP')) + pi) % pi

    elif units in ('deg', 'degree', 'degrees'):
        from numpy import rad2deg

        if domain in (180, '180', 'pi'):
            angle = float(rad2deg(mdadist.calc_angles(sel1.positions, sel2.positions, sel3.positions, backend='OpenMP')))
        elif domain in (360, '360', '2pi'):
            from math import pi
            angle = (float(rad2deg(mdadist.calc_angles(sel1.positions, sel2.positions, sel3.positions, backend='OpenMP'))) + 360) % 360

    return angle


######################

def dist_WATbridge(u, sel1, sel2, sel1_env=3, sel2_env=3):
    """
        This function takes two selection and looks for the nearest bridgin water between them.

        It requires the universe (it needs to select the environment of each selection), the two selections,
        the radius around each selection to look for waters (or the selections of the environment, which requires
        the updating=True argument).
        If no water has been found it will output 'None, None, None'.
    """
    from numpy import min as npmin

    if isinstance(sel1_env, (int, float)):
        res_list = list(sel1.residues)
        for i in range(len(res_list)):
            res_list[i] = str(res_list[i])[(str(res_list[i]).find(', ') + 2):(str(res_list[i]).find('>'))]

        sel1_env = list(u.select_atoms('around ' + str(sel1_env) +
                                            ' resid ' + " or resid ".join(res_list)).residues)

    elif isinstance(sel1_env, Universe):
        pass

    if isinstance(sel2_env, (int, float)):
        res_list = list(sel2.residues)
        for i in range(len(res_list)):
            res_list[i] = str(res_list[i])[(str(res_list[i]).find(', ') + 2):(str(res_list[i]).find('>'))]

        sel2_env = list(u.select_atoms('around ' + str(sel2_env) +
                                            ' resid ' + " or resid ".join(res_list)).residues)

    elif isinstance(sel2_env, Universe):
        pass

    WAT_list = []

    WAT_list = list(filter(lambda r: 'WAT' in str(r), list(set(sel1_env) & set(sel2_env))))
    WAT_list = str(WAT_list)[1:-1].replace('<Residue WAT, ', '')
    WAT_list = str(WAT_list).replace('>', '')
    WAT_list = WAT_list.replace(', ', ' ').split()

    if WAT_list != []:
        for WAT in WAT_list:
            dist1  = npmin(mdadist.distance_array(
                                (u.select_atoms('resid ' + WAT).positions),
                                sel1.positions,
                                backend='OpenMP'))
            dist2 = npmin(mdadist.distance_array(
                                u.select_atoms('resid ' + WAT).positions,
                                sel2.positions,
                                backend='OpenMP'))

            try :
                if dist1 < dist1_min and dist2 < dist2_min:
                    dist1_min  = dist1
                    dist2_min  = dist2
                    bridge_WAT = WAT

            except NameError:
                dist1_min  = dist1
                dist2_min  = dist2
                bridge_WAT = WAT

        return dist1_min, dist2_min, bridge_WAT

    else :
        return None, None, None

def dist_plane(sel, plane1, plane2=None, plane3=None):
    """
        This functions takes one input atom and 3 other input atoms that constitute a plane
        and outputs the distance value and sign.
        #    There are two sets of inputs: the sel, which is the atom that will be measured and which can be input as
        #    a single atom selection, as a selection of multiple atoms or as a list of multiple selections; and the
        #    plane1 (plane2, plane3), which are the three atoms that constitute the plane
        Input selection has to be a selection of the atoms to be measured, while plane atoms can be either a
        selection of 3 atoms or 3 selection of 1 atom.
        The output is a float value or a list of float values depending on the length of the input selection

    TODO:
        - [ ] Convert to input dist_atom_plane and change the input of atoms for building the plane to the plane equation
        - [ ] Plane can be created with the create_plane function

    OBSERVATIONS:
        Results given by this function are not consistent with results shown by Chimera.
    """

    def plane_eq(plane1, plane2, plane3):
        from numpy import cross, dot

        v1 = plane2.position - plane1.position
        v2 = plane3.position - plane1.position

        a, b, c = cross(v1, v2)
        d = dot([a, b, c], plane3.position)

        return [a, b, c, d]

    def distance(point, eq):
        from math import sqrt

        return ((eq[0]*point[0] + eq[1]*point[1] + eq[2]*point[2] - eq[3])/(sqrt((eq[0] ** 2) + (eq[1] ** 2) + (eq[2] ** 2))))

    if len(sel) == 1:
        sel = sel.atoms[0]

    else :
        raise NotSingleAtomSelectionError


    if len(plane1) == 1 and len(plane2) == 1 and len(plane3) == 1:
        plane3 = plane3.atoms[0]
        plane2 = plane2.atoms[0]
        plane1 = plane1.atoms[0]

    elif len(plane1) == 2 and len(plane2) == 1 and plane3 == None:
        plane3 = plane2.atoms[0]
        plane2 = plane1.atoms[1]
        plane1 = plane1.atoms[0]

    elif len(plane1) == 1 and len(plane2) == 2 and plane3 == None:
        plane3 = plane2.atoms[1]
        plane2 = plane2.atoms[0]
        plane1 = plane1.atoms[0]

    elif len(plane1) == 3 and plane2 == None and plane3 == None:
        plane3 = plane1.atoms[2]
        plane2 = plane1.atoms[1]
        plane1 = plane1.atoms[0]

    else :
        raise NotSingleAtomSelectionError


    return distance(sel.position, plane_eq(plane1, plane2, plane3))


def ang_planes(plane1, plane2, units='deg'):
    """
    DESCRIPTION:
        Function for measuring the angle between two given planes.

    OPTIONS:
        - units: deg or rad output

    INPUTS:
        - plane1, plane2: general equation of the input planes
    """

    from math import sqrt, acos
    from numpy import rad2deg

    ang = acos((abs(plane1[0]*plane2[0] + plane1[1]*plane2[1] + plane1[2]*plane2[2]))/((sqrt(plane1[0]**2 + plane1[1]**2 +  plane1[2]**2))*(sqrt(plane2[0]**2 + plane2[1]**2 +  plane2[2]**2))))

    if units.lower() in ('d', 'deg', 'degree', 'degrees'):
        return rad2deg(ang)

    if units.lower() in ('r', 'rad', 'radian', 'radians'):
        return ang


def create_plane(*sel, verbose=False, plot=False):
    """
    DESCRIPTION:
        Function for computing the best fitting plane of several atoms (3 or more) and the centroid and the weighted centroid (by mass).
        The output has three values:
            - The plane equation in the general form (ax + by + cz + d = 0)
            - The Center of Geometry (the centroid) (x, y, z)
            - The Center of Mass (the weighted centroid) (x, y, z)

    ARGUMENTS:
        - sel: MDAnalysis selection(s) of atoms. Multiple selections or selection of multiple atoms or their combination are allowed. At least 3 are required for creating the plane. If not given, an error will be raised
        - verbose: option for printing the fitting errors between atoms and the created plane
        - plot: option for drawing the points (atoms) and the fitted plot in a 3D vision using matplotlib

    SOURCE:
        The code of this function comes from https://math.stackexchange.com/questions/99299/best-fitting-plane-given-a-set-of-point
    """

    from ..exceptions import NotEnoughAtomsSetectedError
    from numpy import matrix
    from numpy.linalg import norm

    sel = sum(sel)

    if len(sel) < 3:
        raise NotEnoughAtomsSetectedError

    elif len(sel) >= 3:
        xs = sel.positions[:,0]
        ys = sel.positions[:,1]
        zs = sel.positions[:,2]

        # do fit
        A, b = [], []
        for i in range(len(xs)):
            A.append([xs[i], ys[i], 1])
            b.append(zs[i])
        b = matrix(b).T
        A = matrix(A)

        # Manual solution
        fit = (A.T * A).I * A.T * b
        errors = b - A * fit
        residual = norm(errors)

        fit = [float(fit[0]), float(fit[1]), 1, float(fit[2])]

        cog = list(sel.center_of_geometry())
        com = list(sel.center_of_mass())

    if verbose == True:
        print(f'The general form of the equation of the plane is: {round(fit[0], 3)}x + {round(fit[1], 3)}y + {round(fit[2], 3)}z + {round(fit[3], 3)} = 0')

        if len(errors) > 1:
           print('Fitting error is: ', errors)
        else :
            errors_str = ''
            for e in errors[:-1]:
                errors_str = errors_str + str(e) + ', '

            errors_str = errors_str + str(e)

            print('Fitting errors for each atom (in order) are: ', errors_str)

    elif verbose == False:
        pass

    if plot == True:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        from numpy import meshgrid, arange, zeros

        plt.figure()
        ax = plt.subplot(111, projection='3d')
        ax.scatter(xs, ys, zs, color='k')
        ax.scatter(cog[0], cog[1], cog[2], color='b')
        ax.scatter(com[0], com[1], com[2], color='r')

        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        X,Y = meshgrid(arange(xlim[0], xlim[1]),
                        arange(ylim[0], ylim[1]))
        Z = zeros(X.shape)
        for r in range(X.shape[0]):
            for c in range(X.shape[1]):
                Z[r,c] = fit[0] * X[r,c] + fit[1] * Y[r,c] + fit[3]
        ax.plot_wireframe(X,Y,Z, color='k')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        plt.show()

    if plot == False:
        pass

    return fit, cog, com


