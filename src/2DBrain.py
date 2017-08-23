from yade import pack
import gts, os.path, locale
from yade import qt
import csv
import numpy as np

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')   #gts is locale-dependend.  If, for example, german locale is used, gts.read()-function does not import floats normally


# surf=gts.read(open('../mesh/2DBrain_withSkull.gts'))
surf=gts.read(open('../mesh/2DBrain.gts'))
O.materials.append(FrictMat(young=10000,poisson=0.35,frictionAngle=0,density=0,label='walls'))


# mn,mx=Vector3(-0.3,-0.3,0.0),Vector3(0.2,0.2,0.006) # corners of the initial packing

Rin = 0.03
Rout = 0.1
rp = 0.0014000

#change material to a more appropriate

pred=pack.inGtsSurface(surf)

idTissue=O.materials.append(FrictMat(young=500.0, poisson=.35, density=1000.0, frictionAngle=.6,label="concrete"))

spheres=pack.regularHexa(pred, radius=rp, gap=1.0e-6, color=(1,0,0), material=idTissue)
O.bodies.append(spheres)

mn,mx=Vector3(-0.10675,-0.3,-0.1),Vector3(0.10675,0.10675,0.006) # corners of the initial packing
walls=aabbWalls([mn,mx],thickness=0, material="walls")
wallIds=O.bodies.append(walls)
print wallIds

# # spherePack = pack.regularHexa(pred, radius=rp, gap=0.0, color=(0,1,0))
# # filteredPack = yade.pack.filterSpherePack(pred, spherePack)

# # O.bodies.append(pack.gtsSurface2Facets(surf,wire=True))
# # O.bodies.append(spheres)
# # O.bodies.append(pack.regularHexa(pack.inAlignedBox(mn,mx),radius=.1,gap=0,color=(0,0,1)))

radius = np.arange(Rin+rp, Rout-rp, 2.0*rp)
rSAS = 0.1 + 2.0 * rp 
rSkull = rSAS + 2.0*rp 
alphaSAS = 4.0*np.arcsin(rp/(2*rSAS)) 
alphaSkull = 4.0*np.arcsin(rp/(2*rSkull))
toll = 0.0
ntheta = 250
theta = np.linspace(0, 2.0*np.pi, ntheta, endpoint=False)
dt = theta[1] - theta[0]
# for z in [0.0014, 0.0042]:
    # for r in [rSAS, rSkull]:
    #     alpha = 4.0*np.arcsin(rp/(2*r))
    #     for j in range(0, int(np.floor((2*np.pi)/alpha))):
    #         s = utils.sphere(center=[r*np.sin(j*alpha), -r*np.cos(j*alpha), z], radius=rp-toll,material=idTissue)
    #         O.bodies.append(s)
tlimit = []
rb = []
for r in [rSAS, rSkull]:
    a = r*np.sin((theta[1] - theta[0])/2.0)
    b = r - r*np.cos((theta[1] - theta[0])/2.0)
    rb += [np.sqrt(a*a + b*b)]

print rb
for z in [1, 3]:
    for t in theta:
        if (t < 3.0/2.0 *np.pi - 3*dt or t > 3.0/2.0 *np.pi + 3*dt):
            s = utils.sphere(center=[rSAS*np.cos(t), rSAS*np.sin(t), rb[0]*z], radius=rb[0], material=idTissue)
            O.bodies.append(s)
            s = utils.sphere(center=[(rSAS+rb[0]+rb[1])*np.cos(t), (rSAS+rb[0]+rb[1])*np.sin(t), rb[0]*z], radius=rb[0], material=idTissue)
            O.bodies.append(s)
        if (t >= 3.0/2.0 * np.pi - 5*dt and t <= 3.0/2.0 * np.pi - 3*dt) or (t >= 3.0/2.0 * np.pi + 3*dt and t <= 3.0/2.0 * np.pi + 5*dt):
            tlimit += [t]
            for i in range(1,50):
                s = utils.sphere(center=[(rSAS+rb[0]+rb[1])*np.cos(t), (rSAS+rb[0]+rb[1])*np.sin(t)-2*i*rb[1], rb[0]*z], radius=rb[0], material=idTissue)
                O.bodies.append(s)
                
# xx = np.linspace((rSAS+rb[0]+rb[1])*np.cos(tlimit[0]), (rSAS+rb[0]+rb[1])*np.cos(tlimit[-1]), 10, endpoint=True)
# rx = (xx[1]-xx[0])/2.0
# for z in[1, 3]:
#     for x in xx:
#         s = utils.sphere(center=[x, (rSAS+rb[0]+rb[1])*np.sin(tlimit[0])-2*50*rb[0]-2*rx, rx*z], radius=rx, material=idTissue)
#         O.bodies.append(s)
#         s = utils.sphere(center=[x, (rSAS+rb[0]+rb[1])*np.sin(tlimit[0])-2*50*rb[0]-4*rx, rx*z], radius=rx, material=idTissue)
#         O.bodies.append(s)

    # for i in range(50):
    #     s = utils.sphere(center=[rSkull*np.sin(3*alphaSkull), -rSkull*np.cos(3*alphaSkull)- (2.0*rp*i), z], radius=rp-toll, material=idTissue)
    #     O.bodies.append(s)
    #     index = int(np.floor((2*np.pi)/alpha))-3
    #     s = utils.sphere(center=[rSkull*np.sin(index*alphaSkull), -rSkull*np.cos(index*alphaSkull)- (2.0*rp*i), z], radius=rp-toll, material=idTissue)
    #     O.bodies.append(s)

    # for i in range(1,50):
    #     s = utils.sphere(center=[rSkull*np.sin(3*alphaSkull) + 2.0*rp, -rSkull*np.cos(3*alphaSkull)- (2.0*rp*i), z], radius=rp-toll, material=idTissue)
    #     O.bodies.append(s)
    #     index = int(np.floor((2*np.pi)/alpha))-3
    #     s = utils.sphere(center=[rSkull*np.sin(index*alphaSkull)-2.0*rp, -rSkull*np.cos(index*alphaSkull)- (2.0*rp*i), z], radius=rp-toll, material=idTissue)
    #     O.bodies.append(s)
        # if i==49 or i==50:
        #     for j in [-3, -2, -1, 0, 1, 2, 3]:
        #         index = int(np.floor((2*np.pi)/alpha))-j
        #         s = utils.sphere(center=[rSkull*np.sin(index*alphaSkull)-2.0*rp,\
        #                                 -rSkull*np.cos(index*alphaSkull)- (2.0*rp*i), z], radius=rp, material=idTissue)
        #         O.bodies.append(s)

qt.View()

newton=NewtonIntegrator(damping=0.2)

O.engines=[
ForceResetter(),
InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Box_Aabb()]),
InteractionLoop(
    [Ig2_Sphere_Sphere_ScGeom(),Ig2_Box_Sphere_ScGeom()],
    [Ip2_FrictMat_FrictMat_FrictPhys()],
    [Law2_ScGeom_FrictPhys_CundallStrack()],label="iloop"
),
FlowEngine(label="flow"),#introduced as a dead engine for the moment, see 2nd section
GlobalStiffnessTimeStepper(active=1,timeStepUpdateInterval=100,timestepSafetyCoefficient=0.8),
# triax,
newton,
VTKRecorder(fileName='./VTK/3d-vtk-',recorders=['all'],iterPeriod=1)
]



#setContactFriction(radians(finalFricDegree))

#B. Activate flow engine and set boundary conditions in order to get permeability
# flow.dead=0
print "defining flow parameters"
# flow.defTolerance=0.0003
flow.debug=True
# flow.useSolver=3
flow.dead=True
flow.bndCondIsPressure=[1,1,1,1,1,1]
flow.bndCondValue=[0,0,0,0,0,0]
# flow.boundaryUseMaxMin=[0,0,0,0,0,0]
O.dt=0.01*PWaveTimeStep()
print "unbalanced Force =", utils.unbalancedForce()
# O.run(1, True)
# print "print cell 3", flow.getCellCenter(3)
# flow.saveVtk("./")

