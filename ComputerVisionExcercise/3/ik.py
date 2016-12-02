from pyfbsdk import *
import math


def skew_sym(v):
    '''
    Returns skew-symetric matrix for vector v
    '''
    m = FBMatrix([
    0, -v[2], v[1], 0,
    v[2], 0, -v[0], 0,
    -v[1], v[0], 0, 0,
    0, 0, 0, 1
    ])
    # IMPORTANT!: In MoBu, matrices are row-major, need to transpose it
    m.Transpose()
    return m


def align_matrix(a,b):
    '''
    Returns matrix that rotates vector a onto vector b
    '''
    # Turn them into unit vectors
    a.Normalize()
    b.Normalize()
    
    v = a.CrossProduct(b)
    s = v.Length() # Sin of angle
    c = a.DotProduct(b) # Cos of angle
    
    # Load identity
    I = FBMatrix()
 
    # a is prallel to b ( return identity)
    if v.Length() == 0:
        return I

    skew_M = skew_sym(v)
    
    R = I +  skew_M + (skew_M*skew_M)*((1-c)/(s*s))
    R[15] = 1 # Can' use 3x3 here
    return R


def getDist(p1, p2):
    '''
    Returns the distance between two points
    '''
    distance = (p2[0]-p1[0])*(p2[0]-p1[0]) \
             + (p2[1]-p1[1])*(p2[1]-p1[1]) \
             + (p2[2]-p1[2])*(p2[2]-p1[2])
    return math.sqrt(distance)


def ccd(goal,chain_base):
    # initialize the variables that are used in the ccd()
    t, pm, pn = FBVector3d(), FBVector3d(), FBVector3d()
    iteration, thresh = 0, 0.01
    
    
    # get the target point and store it in 't'
    goal.GetVector( t, FBModelTransformationType.kModelTranslation)

    # finde the lastNode -> chain_bace.Chidren[0].Chileren[0] ...
    # and find how many bones are there in total
    lastNode = chain_base.Children[0]
    numOfBones = 1
    while len(lastNode.Children) == 1:
        lastNode = lastNode.Children[0]
        numOfBones += 1
          
    # If the distance > thresh or iteration < numOfBones * 10 -> countinue
    while getDist(pn, t) > thresh and iteration < 10*numOfBones:
        # refresh the screen a the bigining
        FBSystem().Scene.Evaluate()

        # get the latest position of the lastNode and store it to 'pn'
        lastNode.GetVector(pn, FBModelTransformationType.kModelTranslation)
        
        # if current point does not have a parent, set lastNode as chain_base
        if chain_base.Parent == None:  
            chain_base = lastNode

        # get the parent of the chain_base
        # chain_base.Parent is the rotation center
        chain_base = chain_base.Parent
        chain_base.GetVector(pm,FBModelTransformationType.kModelTranslation)
     
        # get vector1, vector2, and align_matrix as is told in slides
        vector1 = pn - pm
        vector2 = t  - pm
        R = align_matrix(vector1,vector2)

        # This is copied from the sides, marker is the rotation center        
        marker = chain_base 
        cur_Ori = FBMatrix() 
        marker.GetMatrix(cur_Ori,FBModelTransformationType.kModelRotation,False) 

        # This is copied from the sides donig the rotation
        final_Ori = R * cur_Ori 
        ori_vec = FBVector3d() 
        FBMatrixToRotation(ori_vec,final_Ori) 
        marker.Rotation = ori_vec

        iteration+=1
        
''' The rest part are using for testing '''
'''
goal = FBFindModelByLabelName('Goal')
chain_base = FBFindModelByLabelName('Node')       
ccd(goal,chain_base)
'''