from yade import pack
import gts, os.path, locale
from yade import qt

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')   #gts is locale-dependend.  If, for example, german locale is used, gts.read()-function does not import floats normally


surf=gts.read(open('../mesh/sphere.gts'))

idTissue=O.materials.append(FrictMat(young=500.0,poisson=.35,frictionAngle=.6,label="concrete"))
pred=pack.inGtsSurface(surf)
aabb=pred.aabb()

dim0=aabb[1][0]-aabb[0][0];
# brain radius
dim0 = dim0/2.0
# small
radius=dim0/20. # get some characteristic dimension, use it for radius
O.bodies.append(pack.regularHexa(pred, radius=radius, gap=0.0, material=idTissue))

O.bodies.append(pack.gtsSurface2Facets(surf,wire=True))

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

for b in O.bodies:
	if isinstance(b.shape,Sphere):
		print b.state.pos
		print b.shape.radius

O.dt=0.1*PWaveTimeStep()
O.saveTmp()
O.timingEnabled=True
O.trackEnergy=True

#a = qt.View()
#yade.qt._GLViewer.GLViewer.saveSnapshot(qt.View(), "sphere.png")