from yade import pack
import gts, os.path, locale
from yade import qt
import csv
import numpy as np

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')   #gts is locale-dependend.  If, for example, german locale is used, gts.read()-function does not import floats normally

surf=gts.read(open('../mesh/2DBrain_spine.gts'))

Rin = 0.03
Rout = 0.1
rp = 0.0014000


idTissue=O.materials.append(FrictMat(young=500.0, poisson=.35, density=1000.0, frictionAngle=.6,label="tissue"))
idSkull=O.materials.append(FrictMat(young=10000000.0, poisson=.35, density=2000.0, frictionAngle=.6,label="skull"))

wallMaterial=O.materials.append(FrictMat(young=10000000.0, poisson=.35, density=1000.0, frictionAngle=.6,label="walls"))
print "idTissue = ", idTissue
print "wallMaterial = ", wallMaterial

minX = -0.10668581441037103
maxX =  0.10668581441037103
minY = -0.23733754727640186 
maxY =  0.10670230537773978
minZ =  0.0
maxZ =  0.011892672035984387
mn,mx=Vector3(minX,minY,minZ),Vector3(maxX,maxY,maxZ) # corners of the initial packing
walls=aabbWalls([mn,mx],thickness=0, material="walls")
wallIds=O.bodies.append(walls)

pred=pack.inGtsSurface(surf)
spheres=pack.regularHexa(pred, radius=rp, gap=0.0, color=(1,0,0), material=idTissue)
O.bodies.append(spheres)
print "red mass = ", O.bodies[-1].state.mass
for b in O.bodies:
    if isinstance(b.shape,Sphere):
        if b.state.pos[1] < -0.097:
            print "position y = ", b.state.pos


print "radius hex = ", rp
radius = np.arange(Rin+rp, Rout-rp, 2.0*rp)
rSAS = 0.1 + 2.0 * rp 
print "rSAS = ", rSAS
rSkull = rSAS + 2.0*rp
print "rSkull = ", rSkull 
alphaSAS = 4.0*np.arcsin(rp/(2*rSAS)) 
alphaSkull = 4.0*np.arcsin(rp/(2*rSkull))
toll = 0.0
ntheta = 250
theta = np.linspace(0, 2.0*np.pi, ntheta, endpoint=False)
dt = theta[1] - theta[0] 

tlimit = []
xlimit = []
ylimit = []
dx = []
dy = []
rb = []
for r in [rSAS, rSkull]:
    a = r*np.sin((theta[1] - theta[0])/2.0)
    b = r - r*np.cos((theta[1] - theta[0])/2.0)
    rb += [np.sqrt(a*a + b*b) - 2e-5]

for z in [1, 3, 5, 7]:
    for t in theta:
        if (t < 3.0/2.0 *np.pi - 3*dt or t > 3.0/2.0 *np.pi + 3*dt):
            s = utils.sphere(center=[rSAS*np.cos(t), rSAS*np.sin(t), rb[0]*z], radius=rb[0], color=(0,1,0), material=idSkull)
            O.bodies.append(s)
            # print "green mass", O.bodies[-1].state.mass
            s = utils.sphere(center=[(rSAS+rb[0]+rb[1])*np.cos(t), (rSAS+rb[0]+rb[1])*np.sin(t), rb[1]*z], radius=rb[1], color=(0,1,1), material=idSkull)
            O.bodies.append(s)
            # print "light blue mass", O.bodies[-1].state.mass
        if (t >= 3.0/2.0 * np.pi - 5*dt and t <= 3.0/2.0 * np.pi - 3*dt) or (t >= 3.0/2.0 * np.pi + 3*dt and t <= 3.0/2.0 * np.pi + 5*dt):
            tlimit += [t]
            for i in range(1,50):
                s = utils.sphere(center=[(rSAS+rb[0]+rb[1])*np.cos(t), (rSAS+rb[0]+rb[1])*np.sin(t)-2*i*rb[1], rb[1]*z], radius=rb[1], color=(0,0,1), material=idSkull)
                O.bodies.append(s)
            # print "blue mass", O.bodies[-1].state.mass
            
            xlimit += [(rSAS+rb[0]+rb[1])*np.cos(t)]
            ylimit += [(rSAS+rb[0]+rb[1])*np.sin(t)-2*i*rb[1]]


print "rb = ", rb             
print xlimit
print ylimit
dx = xlimit[3] - xlimit[0]
Nbase = 9
rbase = dx/(Nbase*2-2)

print rbase
for i in range(2):
    for z in [1, 3, 5, 7]:
        s = utils.sphere(center=[xlimit[0] + i*2*rbase, ylimit[i]-rb[1]-rbase, rbase*z], radius=rbase, color=(1,0,1), material=idSkull)
        O.bodies.append(s)
        # s = utils.sphere(center=[xlimit[0] + i*2*rbase, ylimit[i]-rb[1]-3*rbase, rbase*z], radius=rbase, material=idTissue)
        # O.bodies.append(s)
for i in range(2):
    for z in [1, 3, 5, 7]:
        s = utils.sphere(center=[xlimit[6] + i*2*rbase, ylimit[6+i]-rb[1]-rbase, rbase*z], radius=rbase, color=(1,0,1), material=idSkull)
        O.bodies.append(s)
        # s = utils.sphere(center=[xlimit[6] + i*2*rbase, ylimit[6+i]-rb[1]-3*rbase, rbase*z], radius=rbase, material=idTissue)
        # O.bodies.append(s)
for i in range(2,7):
    for z in [1, 3, 5, 7]:
        s = utils.sphere(center=[xlimit[0] + i*2*rbase, ylimit[1]-rb[1]-rbase, rbase*z], radius=rbase, color=(1,0,1), material=idSkull)
        O.bodies.append(s)

for i in range(1,6):
    for z in [1, 3, 5, 7]:
        s = utils.sphere(center=[xlimit[1] + i*2*rbase, ylimit[1]-rb[1]+rbase, rbase*z], radius=rbase, color=(1,0,1), material=idSkull)
        O.bodies.append(s)
print "purple mass", O.bodies[-1].state.mass

# quit()
qt.View()

print "rbase = ", rbase
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
VTKRecorder(fileName='./VTK/',recorders=['all'],iterPeriod=1)
]

#setContactFriction(radians(finalFricDegree))

#B. Activate flow engine and set boundary conditions in order to get permeability
# flow.dead=0
print "defining flow parameters"
flow.debug=True
O.dt=0.1e-6
flow.dead=1
flow.defTolerance=0.3
flow.meshUpdateInterval=200
flow.useSolver=3
flow.permeabilityFactor=1
flow.viscosity=10

flow.bndCondIsPressure=[1,1,1,1,1,1]
flow.bndCondValue=[0,0,0,0,0,0]

O.run(1, True)
flow.saveVtk("./VTK")

#Make 4 layers
# look a cohesive material yade.wrapper.JCFpmMat