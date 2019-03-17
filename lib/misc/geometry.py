#!/usr/bin/python


from math import pi, cos, sin, sqrt, acos
from sys import exit

def tensprod(T1, T2):
    
    # M3 = tensprod(M1, M2)
    #
    #Tensor product
    #M1, M2 = [[x_ss.. ],[ y_ps..],[z_ts..]]
    #
    #Othe seccond input can have multiple columns??
    #
    c = len( T1)
    v = len( T1[0])
    Tx = []
    Ty = []
    Tz = []
    #print '-'*35
    #for i in range( len( T2)):
    #    print T2[i]
    #for i in range( c):
    #    print T1[i]
    #print T1[0][0]*T2[0][0] + T1[0][2]*T2[2][0]
    if len( T2) <> v:
        print('Tensors length')
        pT = [ [], [], []]
    else:
        for j in range( len( T2[0])):
            sx = 0
            sy = 0
            sz = 0
            for i in [0,1,2]:
                #print T1[0][i],'*', T2[0][j], '+',
                sx += T1[0][i] * T2[i][j]
                sy += T1[1][i] * T2[i][j]
                sz += T1[2][i] * T2[i][j]
            #print ' .'
            Tx.append( sx)
            Ty.append( sy)
            Tz.append( sz)
        pT = [ Tx, Ty, Tz]
        
    return pT

def raiz( value):
    return sqrt( value)

def arcos( value):
    return acos( value)

def rotate( t2r, angle, axis = 'x'):
    
    R =     [[ 1         ,  0         , 0         ],
             [ 0         ,  1         , 0         ],
             [ 0         ,  0         , 1         ]]
    if axis == 'x':
        R = [[ 1         ,  0         , 0         ],
             [ 0         ,  cos(angle),-sin(angle)],
             [ 0         ,  sin(angle), cos(angle)]]
    elif axis == 'y':
        R = [[ cos(angle),  0         , sin(angle)],
             [ 0         ,  1         , 0         ],
             [-sin(angle),  0         , cos(angle)]]
    elif axis == 'z':
        R = [[ cos(angle), -sin(angle), 0         ],
             [ sin(angle),  cos(angle), 0         ],
             [ 0         ,  0         , 1         ]]
    else:
        print 'Error! invalid axis : {}'.format( axis)
    
    return tensprod( R, t2r)
    

if __name__ == '__main__':
    
    tensorvec = [ 4.04659, 2.63083, 68.36656, 0.00000,   0.00000,  -0.73454,   0.00000,  -1.45599, -0.54283]
    
    tensorvec = [ x_y_z*10 for x_y_z in tensorvec ]
    Ar = [[0,0,0],[0,0,0],[0,0,0]]
    k = 0
    index = range(3)
    for i in range(3):
        Ar[i][i] = tensorvec[i]
        print Ar
        for j in range(3):#.remove(i):
            if i <> j:
                #
                Ar[i][j] = tensorvec[k+3]
                k += 1
    print Ar
    #Ar = [ [4.0465, 0, 0],[-0.73454, 2.63083, 0], [-1.45599, -0.54283, 68.36656 ]]
    #A = [ 4.0465, -0.73454, -1.45599, 0, 2.63083, -0.54283, 0, 0, 68.36656 ]
    
    a_tor_y = -acos( (Ar[0][0])/(sqrt(Ar[0][0]*Ar[0][0]+Ar[2][0]*Ar[2][0])) )
    #Ry = [cos(a_tor_y) 0 sin(a_tor_y); 0 1 0 ; -sin(a_tor_y) 0 cos(a_tor_y)]
    #Ry = [[cos(a_tor_y), 0, sin(a_tor_y)],[0, 1, 0], [-sin(a_tor_y), 0, cos(a_tor_y)]]
    #Ar = tensprod( Ry, Ar)
    
    Ar = rotate( Ar, a_tor_y, 'y')
    
    
    a_tor_z = acos( (Ar[0][0])/(sqrt(Ar[0][0]*Ar[0][0]+Ar[1][0]*Ar[1][0])) )
    #Rz = [cos(a_tor_z) -sin(a_tor_z) 0; sin(a_tor_z) cos(a_tor_z) 0; 0 0 1];
    #Rz = [[ cos(a_tor_z), -sin(a_tor_z), 0], [sin(a_tor_z), cos(a_tor_z), 0], [0, 0, 1]]
    #Ar = tensprod( Rz, Ar)
    Ar = rotate( Ar, a_tor_z, 'z')
    
    a_tor_x = acos( Ar[1][1]/( sqrt( Ar[1][1]*Ar[1][1] + Ar[2][1]*Ar[2][1])) )
    #Rx = [[1, 0, 0], [0, cos(a_tor_x), -sin(a_tor_x)], [0, sin(a_tor_x), cos(a_tor_x)]]
    #Rx = [1 0 0; 0 cos(a_tor_x) -sin(a_tor_x); 0 sin(a_tor_x) cos(a_tor_x)];
    Ar = rotate( Ar, a_tor_x)
    
    for i in range( len( Ar)):
        print Ar[i]
    
    
# vim:tw=80

