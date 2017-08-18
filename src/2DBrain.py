from yade import pack
import gts, os.path, locale
from yade import qt
import csv
import numpy as np

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')   #gts is locale-dependend.  If, for example, german locale is used, gts.read()-function does not import floats normally


surf=gts.read(open('../mesh/2DBrain.gts'))

#change material to a more appropriate
idTissue=O.materials.append(FrictMat(young=500.0, poisson=.35, density=1000.0, frictionAngle=.6,label="concrete"))
pred=pack.inGtsSurface(surf)
aabb=pred.aabb()

Rin = 0.03
Rout = 0.1
rp = 0.0014
#spheres=pack.randomDensePack(pred,spheresInCell=2000,radius=3.5e-3,returnSpherePack=False)
#spheres=pack.randomDensePack(pred, spheresInCell=2000, radius=.0035, color=(0,0,1))
#spheres=pack.randomDensePack(pred, spheresInCell=000, radius=3.0e-3, color=(0,1,0))
#O.bodies.append(spheres)
O.bodies.append(pack.regularHexa(pred, radius=rp, gap=0.0, material=idTissue, color=(0,1,0)))
#O.bodies.append(pack.randomDensePack(pred, radius=radius, gap=0.0, material=idTissue, color=(0,1,0)))



O.engines=[
    ForceResetter(),
    InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Facet_Aabb()],label='collider'),
    InteractionLoop(
        [Ig2_Sphere_Sphere_ScGeom(),Ig2_Facet_Sphere_ScGeom()],
        [Ip2_FrictMat_FrictMat_FrictPhys()],
        [Law2_ScGeom_FrictPhys_CundallStrack()],
    ),
    NewtonIntegrator(damping=0.1,gravity=[0,0,0]),
    # FlowEngine(label="flow"),#introduced as a dead engine for the moment, see 2nd section

]

radius = np.arange(Rin+rp, Rout-rp, 2.0*rp)
rSAS = 0.1 + 3.0/2.0 * rp
rSkull = rSAS + 2.0*rp
alphaSAS = 4.0*np.arcsin(rp/(2*rSAS)) 
alphaSkull = 4.0*np.arcsin(rp/(2*rSkull))
for z in [0.0022861904265976327, 0.004572380853195265]:
    for r in [rSAS, rSkull]:
        alpha = 4.0*np.arcsin(rp/(2*r))
        for j in range(3, int(np.floor((2*np.pi)/alpha))-3):
            s = utils.sphere(center=[r*np.sin(j*alpha), -r*np.cos(j*alpha), z], radius=rp, color=(0,1,1))
            O.bodies.append(s)

    for i in range(50):
        s = utils.sphere(center=[rSkull*np.sin(3*alphaSkull), -rSkull*np.cos(3*alphaSkull)- (2.0*rp*i), z], radius=rp, color=(0,1,1))
        O.bodies.append(s)
        index = int(np.floor((2*np.pi)/alpha))-3
        s = utils.sphere(center=[rSkull*np.sin(index*alphaSkull), -rSkull*np.cos(index*alphaSkull)- (2.0*rp*i), z], radius=rp, color=(0,1,1))
        O.bodies.append(s)

 
#O.bodies.append(pack.gtsSurface2Facets(surf,wire=True))

with open("state_shape.csv", "w") as f:
    wrt = csv.writer(f)
    for b in O.bodies:
        if isinstance(b.shape,Sphere):
            print "id = ", b.id     
            print "position = ", b.state.pos
            print "radius = ", b.shape.radius
            print "mass = ", b.state.mass

            wrt.writerow(("id", b.id))
            position = str(b.state.pos[0]) + " ; " + str(b.state.pos[1]) + " ; " + str(b.state.pos[2])
            wrt.writerow(("position ", position))
            wrt.writerow(("radius " , b.shape.radius))
            wrt.writerow(("mass ", b.state.mass))
        # if isinstance(b.shape,Facet):
        #     print "facet"
        #     print b.id
        #     print b.state.mass

# with open("Material.csv", "w") as f:
#     wrt = csv.writer(f)
#     d = O.bodies[0].material.dict() 
#     for k, v in d.items():
#         wrt.writerow((k, v))


# with open("Force_Resetter.csv", "w") as f:
#     wrt = csv.writer(f)

#     d = O.engines[0].dict() 
#     for k, v in d.items():
#         wrt.writerow((k, v))

# with open("InsertionSortCollider.csv", "w") as f:
#     wrt = csv.writer(f)
#     d = O.engines[1].dict() 
#     for k, v in d.items():
#         wrt.writerow((k, v))
           
# with open("InteractionLoop.csv", "w") as f:
#     wrt = csv.writer(f)
#     d = O.engines[2].dict() 
#     for k, v in d.items():
#         wrt.writerow((k, v))

# with open("GeometryDispatcher.csv", "w") as f:
#     wrt = csv.writer(f)
#     d = O.engines[2].dict()["geomDispatcher"].dict() 
#     for k, v in d.items():
#         wrt.writerow((k, v))

# with open("GeometryFunctors.csv", "w") as f:
#     wrt = csv.writer(f)
#     d = O.engines[2].dict()["geomDispatcher"].dict()["functors"][0].dict()
#     for k, v in d.items():
#         wrt.writerow((k, v))
#     d = O.engines[2].dict()["geomDispatcher"].dict()["functors"][1].dict()
#     for k, v in d.items():
#         wrt.writerow((k, v))

# with open("LawDispatcher.csv", "w") as f:
#     wrt = csv.writer(f)
#     d = O.engines[2].dict()["lawDispatcher"].dict() 
#     for k, v in d.items():
#         wrt.writerow((k, v))

# with open("LawDispatcherFunctors.csv", "w") as f:
#     wrt = csv.writer(f)
#     d = O.engines[2].dict()["lawDispatcher"].dict()["functors"][0].dict()
#     for k, v in d.items():
#         wrt.writerow((k, v))
 
# with open("PhysicsDispatcher.csv", "w") as f:
#     wrt = csv.writer(f)
#     d = O.engines[2].dict()["physDispatcher"].dict() 
#     for k, v in d.items():
#         wrt.writerow((k, v))

# with open("PhysicsDispatcherFunctors.csv", "w") as f:
#     wrt = csv.writer(f)
#     d = O.engines[2].dict()["physDispatcher"].dict()["functors"][0].dict()
#     for k, v in d.items():
#         wrt.writerow((k, v))


# with open("NewtonIntegrator.csv", "w") as f:
#     wrt = csv.writer(f)
#     d = O.engines[3].dict() 
#     for k, v in d.items():
#         wrt.writerow((k, v))

#This is the critical timestep, determined by spheres size 
O.dt=0.1*PWaveTimeStep()
O.saveTmp()
O.timingEnabled=True
O.trackEnergy=True

qt.View()
#O.run()
#yade.qt._GLViewer.GLViewer.saveSnapshot(qt.View(), "sphere.png")