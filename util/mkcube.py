#!/usr/bin/env python

# imports
import optparse

VERSION = '0.1.0'

LONGHELP = """
mkcube.py -- description here

SYSNOPSIS

mkcube.py [options] ?? ?? ??

Options: mkcube.py --help

DESCRIPTION

PROCEDURE

EXAMPLES

ENVIRONMENT

PREREQUISITE

SEE ALSO
"""

def parse_args():
    
    #mkcube 'nsnr=50:2500:50' 'snrate=0.0005:0.1:0.0005' 'nambient=0.5,1,2,3,4,5,10'
    #    1e5 pathtogalaxyinputs --split=5,20,1 --cubes=1:30
    # Parse command line arguments
    usage = "%prog [options] 'name1=grid1' 'name2=grid2' 'name3=grid3' lifetime galaxydir"
    p = optparse.OptionParser(usage=usage, version='v'+VERSION)
    
    p.add_option('--lifetime', action='store', type='float', help='required argument. Emitting lifetime.')
    p.add_option('--galaxydir', action='store',type='string', help='required argument. Path to the input files.')
    
    p.add_option('--cubes', action='store', type='string', default=None, help='Range of cubes to set up. id1:idN')
    p.add_option('--split', action='store', type='string', default='1,1,1', help='Number of sections into which the axes are to be split.')
    
    p.add_option('--debug', action='store_true', help='toggle debug messages')
    p.add_option('--verbose', '-v', action='store_true', help='toggle on verbose mode')
    p.add_option('--longhelp', action='store_true', help='print online manual')
    
    (options, args) = p.parse_args()
    
    if options.longhelp:
        print LONGHELP
        raise SystemExit
    
    if options.debug:
        options.verbose = True
        print 'options: ', options
        print 'args: ', args

    if len(args) != 5:
       errmsg = '\nUSAGE ERROR: Expecting ...'
       p.print_help()
       raise SystemExit, errmsg
    
    # Parsing the required arguments
    axes_names = []
    axes_grid_strings = []
    for arg in args[0:3]:
        (name,grid_string) = arg.split('=')
        axes_names.append(name)
        axes_grid_strings.append(grid_string)
    
    options.lifetime = float(args[3])
    options.galaxydir = args[4]
    
    if options.debug:
        print axes_names
        print axes_grid_strings
        
    return (options, axes_names, axes_grid_strings)


def mkcube(options, axes_names, axes_grid_strings):
    import re
    # required inputs:
    #    - name of three axes
    #    - grid for each axes
    #    - how to split the parameter space
    #    - lifetime
    #    - path to galaxy inputs
    #    - which cubes to set up in this location.
    
    # Define the parameter space to explore
    # Axis 1 : Number of SNR to model.  50 to 2500 in steps of 50.
    # Axis 2 : Supernova rate (SN/yr?) to model for. 0.0005 to 0.1 in steps of 0.0005.
    # Axis 3 : Ambient density in (??). 0.5, 1, 2, 3, 4, 5, 10
    psaxes = []
    for i in range(len(axes_names)):
        grid = Grid(axes_grid_strings[i])
        if grid.range:
            psaxes.append(PSAxis(axes_names[i]))
            psaxes[i].set_values_from_range(grid.start,grid.end+grid.step,grid.step)
        else:
            psaxes.append(PSAxis(axes_names[i],grid.list))
    fullps = Param_Space(psaxes[0],psaxes[1],psaxes[2])
    
    # Split the cube as required by the user (eg. split the param space into n cubes)
    # This involves keeping track of the param space for each cube.
    nsections = [int(x) for x in options.split.split(',')]
    sections = fullps.split_param_space(axes_names,nsections)
    
    # Create cubes from those sections of the parameter space.
    cubes = []
    id = 1
    for section in sections:
        cube = Cube(section, id, lifetime=options.lifetime)
        cubes.append(cube)
        id += 1
    
    if options.cubes == None:
        firstcube = cubes[0].id
        lastcube = cubes[-1].id
    elif re.match('\d+:\d+', options.cubes):
        firstcube, lastcube = [int(x) for x in options.cubes.split(':')]
    else:
        firstcube = int(options.cubes)
        lastcube = firstcube
        
    # create README_cube
    create_readme(cubes[firstcube-1:lastcube])
    
    # create cube directories
    create_cubedir(cubes[firstcube-1:lastcube])
    
    # populate cube directories
    # This involves 
    #    - copy inputs for specified galaxy
    #    - modifying some .param files with the param space for that cube
    #    - use mk*queue.sh to generate the queues.
    populate_cubes(cubes[firstcube-1:lastcube],options.galaxydir)
    
    # generate the queues
    generate_queues(firstcube,lastcube)
    
    return


class Cube:
    def __init__(self, parameter_space, id=1, lifetime=0):
        self.set_parameter_space(parameter_space)
        self.set_id(id)
        self.set_name()
        self.set_lifetime(lifetime)
    
    def set_id(self,id):
        self.id = id
        return
    
    def set_lifetime(self, lifetime):
        self.lifetime = lifetime
        return
    
    def set_name(self):
        root = 'cube'
        self.name=(root+str(self.id))
        return
    
    def set_parameter_space(self,parameter_space):
        self.parameter_space = parameter_space
        return
    
    def axis_names(self):
        names = self.parameter_space.axes.keys()
        return names
    
    
class Param_Space:
    def __init__(self, axis1, axis2, axis3):
        # axisN are PSAxis objects
        #
        # {'nsnr': [50,100,...,2500],
        #  'snrate': [0.0005, 0.0010, 0.1],
        #  'nambient': [0.5,1,2,3,5,10]}
        #
        # Attributes:
        #    axes:    dictionary
        #    size:    dictionary
        self.set_axes(axis1, axis2, axis3)
        self.size = self.get_size()
    
    def set_axes(self, axis1, axis2, axis3):
        # axisN are PSAxis objects.
        self.axes = {axis1.name : axis1.values,
                     axis2.name : axis2.values,
                     axis3.name : axis3.values
                     }
        return
    
    def get_size(self):
        size = {}
        for name in self.axes.keys():
            size[name] = len(self.axes[name])
        return size
    
    def split_param_space(self, axis_names, nsections):
        import operator
        debug=False
        
        # Split the axes into nsections
        axis_sections = {}
        for i in range(len(axis_names)):
            nelement_per_section = len(self.axes[axis_names[i]])/nsections[i]
            
            axis_sections[axis_names[i]] = []
            for section in range(nsections[i]):
                index1 = section*nelement_per_section
                index2 = (section+1)*nelement_per_section
                values = self.axes[axis_names[i]][index1:index2]
                axis = PSAxis(axis_names[i],values)
                axis_sections[axis_names[i]].append(axis)
        
        # Reassemble the axes into new Param_Spaces
        if debug:
            n_param_spaces = reduce(operator.mul, nsections)
            print n_param_spaces
        
        new_param_spaces = []
        for s0 in axis_sections[axis_names[0]]:
            for s1 in axis_sections[axis_names[1]]:
                for s2 in axis_sections[axis_names[2]]:
                    ps = Param_Space(s0,s1,s2)
                    new_param_spaces.append(ps)                
        
        return new_param_spaces
  
class PSAxis:
    def __init__(self, name=None, values=None):
        # Attributes:
        #    name:    string
        #    values:  list
        self.set_name(name)
        self.set_values(values)
    
    def set_name(self, name):
        self.name=name
        return
    
    def set_values(self, values):
        self.values=values
        return
    
    def set_values_from_range(self,start,end,increment):
        values = [x for x in _drange(start, end, increment)]
        self.values=values
        return

class Grid:
    def __init__(self, grid_string):
        # figure out if range or list
        # set type (range or list)
        # store values
        import re
        
        # Range or list?
        # start:end:step  or  n1,n2,n3,...,nN
        if re.match('[\d\.]+:[\d\.]+:[\d\.]+', grid_string):
            self.range = True
            (self.start,self.end,self.step) = [float(x) for x in grid_string.split(':')]
        elif re.match('[\d\.]+|,?', grid_string):
            self.range = False
            self.list=[float(x) for x in grid_string.split(',')]


def create_readme(cubes):
    filename = 'README_cube'
    line1fmt = '%s: 0 completed (computer) ; status(queue_name) 0 @ computer\n'
    lineNfmt = '   - %s=%s\n'
    lineblankfmt = '\n'
    
    f = open(filename,'w')
    
    for cube in cubes:
        axis_names = cube.axis_names()
        axis_names.sort()
        ps = cube.parameter_space
        L = []
        L.append(line1fmt % (cube.name))
        
        for i in range(len(axis_names)):
            values_str = ''
            first = True
            for x in ps.axes[axis_names[i]]:
                if first:
                    values_str += '%g' % (x)
                    first = False
                else:
                    values_str += ',%g' % (x)      
            L.append(lineNfmt % (axis_names[i],values_str))
            
        L.append(lineblankfmt)
        f.writelines(L)
    
    f.close()
    
    return

def create_cubedir(cubes):
    import os
    import os.path
    
    for cube in cubes:
        dirs_to_create = [cube.name,
                          os.path.join(cube.name, 'day'),
                          os.path.join(cube.name, 'night'),
                          os.path.join(cube.name, 'wkend')
                          ]
        for dir in dirs_to_create:
            if not os.path.exists(dir):
                os.makedirs(dir)
    return

def populate_cubes(cubes,inputpath):
    import shutil
    import os.path
    import glob
        
    files = glob.glob(os.path.join(inputpath,'*.param'))
    files.extend(glob.glob(os.path.join(inputpath,'dofit*.sh')))
    files.extend(glob.glob(os.path.join(inputpath,'*.fits')))
    files.extend(glob.glob(os.path.join(inputpath,'*.coo')))
    files.extend(glob.glob(os.path.join(inputpath,'*.pop')))
    files.append(os.path.join(inputpath,'README'))
        
    for cube in cubes:
        # copy files
        for file in files:
            shutil.copy(file, os.path.join(cube.name, 'day'))
            shutil.copy(file, os.path.join(cube.name, 'night'))
            shutil.copy(file, os.path.join(cube.name, 'wkend'))
            
        # configure files
        # --
        # dofit.sh and dofit-wud.sh: 
        #    replace cube1.log with appropriate name for this cube
        _config_file(os.path.join(cube.name,'day'),'dofit.sh', '\w+\.log', cube.name+'.log')
        _config_file(os.path.join(cube.name,'day'),'dofit-wud.sh', '\w+\.log', cube.name+'.log')
        toCopy = ['dofit.sh','dofit-wud.sh']
        
        # snrpopfit.param
        nsnr = ','.join([str(x) for x in cube.parameter_space.axes['nsnr']])
        snrate = ','.join([str(x) for x in cube.parameter_space.axes['snrate']])
        nambient = ','.join([str(x) for x in cube.parameter_space.axes['nambient']])
        _config_file(os.path.join(cube.name,'day'),'snrpopfit.param',
                     'snrpopfit.nsnr=(\d|,|\.)+', 'snrpopfit.nsnr='+nsnr)
        _config_file(os.path.join(cube.name,'day'),'snrpopfit.param',
                     'snrpopfit.snrate=(\d|,|\.)+', 'snrpopfit.snrate='+snrate)
        _config_file(os.path.join(cube.name,'day'),'snrpopfit.param',
                     'snrpopfit.nambient=(\d|,|\.)+', 'snrpopfit.nambient='+nambient)
        toCopy.append('snrpopfit.param')
        
        # mksnrpop.param
        _config_file(os.path.join(cube.name,'day'),'mksnrpop.param',
                     'mksnrpop.life=(\d|e)+', 'mksnrpop.life=%g' % cube.lifetime)
        toCopy.append('mksnrpop.param')
        
        for file in toCopy:
            shutil.copy(os.path.join(cube.name,'day',file),
                        os.path.join(cube.name,'night',file))
            shutil.copy(os.path.join(cube.name,'day',file),
                        os.path.join(cube.name,'wkend',file))
        
    return


def generate_queues(idstart, idend):
    import subprocess
    
    day = open('dodayqueue.sh','w')
    night = open('donightqueue.sh', 'w')
    wkend = open('dowkendqueue.sh','w')
    retcode = subprocess.call(['mkdayqueue.sh',str(idstart),str(idend)],stdout=day)
    retcode = subprocess.call(['mknightqueue.sh',str(idstart),str(idend)],stdout=night)
    retcode = subprocess.call(['mkwkendqueue.sh',str(idstart),str(idend)],stdout=wkend)
    day.close()
    night.close()
    wkend.close()

    return


def _config_file(dir,file,pattern,replacement):
    import os.path
    import re
    
    f = open(os.path.join(dir,file),'r')
    L = f.readlines()
    f.close()
    f = open(os.path.join(dir,file),'w')
    new_L=[]
    for line in L:
        line = re.sub(pattern, replacement, line)
        new_L.append(line)
        #print line
    f.writelines(new_L)
    f.close()

    return

def _drange(start, end, increment):
    value = start
    while value < end:
        yield value
        value += increment
        

def test():
    a1=PSAxis('nsnr',None)
    a1.set_values_from_range(50,2501,50)
    a2=PSAxis('snrate')
    a2.set_values_from_range(0.0005,0.1001,0.0005)
    a3 = PSAxis('nambient',[0.5,1,2,3,4,5,10])
    ps = Param_Space(a1,a2,a3)
    sections = ps.split_param_space(['nsnr','snrate','nambient'],[5,1,1])
    cubes = []
    id = 1
    for section in sections:
        cube = Cube(section, id, lifetime=1e5)
        cubes.append(cube)
        id += 1
    
    return cubes

def test2():
    grid = Grid('50:2500:50')
    grid = Grid('0.0005:0.1:0.0005')
    grid = Grid('0.5,1,2,3,4,5,10')
    
    return

#---------------------------

if __name__ == '__main__':
    (options, axes_names, axes_grid_strings) = parse_args()
    
    mkcube(options, axes_names, axes_grid_strings)
