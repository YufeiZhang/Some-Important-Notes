from pyfbsdk import *
import sys

#sys.path.pop(0)
'''
sys.path.insert(0,"C:\Users\yufei2\Downloads")

if "ik" in sys.modules:
    del sys.modules["ik"]
'''

#import ik

def create_chain(nodes,bone_len):
    '''
    Creates a chain of nodes
    '''
    
    parent = None
    for i in xrange(0,nodes):
        child = FBModelSkeleton('Node')
        
        # Add a node to the chain
        if parent is not None:
            parent.Children.append(child)
            child.Translation = FBVector3d(0,bone_len,0)
            
        parent = child
        # Make sure every node is visible
        parent.Show = True
    

def create_goal(init_pos):
    '''
    Creates goal for our IK
    '''
    g = FBModelMarker('Goal')
    g.Translation = init_pos
    g.Show=True  
    
## Uncomment following block to test your script
n_nodes=5 # Always at least 2
bone_len=50
create_chain(n_nodes,bone_len)
initial_pos = FBVector3d(60,100,80)
create_goal(initial_pos)

#goal = FBFindModelByLabelName('Goal')
#chain_base = FBFindModelByLabelName('Node')
#ik.ccd(goal,chain_base)
