from yade import pack
import gts, os.path, locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')   #gts is locale-dependend.  If, for example, german locale is used, gts.read()-function does not import floats normally


surf=gts.read(open('sphere.gts'))

if surf.is_closed():
	pred=pack.inGtsSurface(surf)
	aabb=pred.aabb()
	dim0=aabb[1][0]-aabb[0][0]; radius=dim0/40. # get some characteristic dimension, use it for radius
	O.bodies.append(pack.regularHexa(pred,radius=radius,gap=radius/4.))
	#surf.translate(0,0,-(aabb[1][2]-aabb[0][2])) # move surface down so that facets are underneath the falling spheres
O.bodies.append(pack.gtsSurface2Facets(surf,wire=True))

for b in O.bodies:
	if b.shape.name!=Sphere: continue
	if b.state.pos[2]<.5: 
		b.dynamic=False
		print b.state.pos
    
O.engines=[
	#ForceResetter(),
	InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Facet_Aabb()],label='collider'),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(),Ig2_Facet_Sphere_ScGeom()],
		[Ip2_FrictMat_FrictMat_FrictPhys()],
		[Law2_ScGeom_FrictPhys_CundallStrack()],
	),
	NewtonIntegrator(damping=.1,gravity=[0,0,0]),
	PyRunner(iterPeriod=1000,command='timing.stats(); O.pause();'),
	PyRunner(iterPeriod=10,command='addPlotData()')
]
O.dt=.7*PWaveTimeStep()
O.saveTmp()
O.timingEnabled=True
O.trackEnergy=True
from yade import plot
plot.plots={'i':('total',O.energy.keys,)}
def addPlotData(): plot.addData(i=O.iter,total=O.energy.total(),**O.energy)
plot.plot(subPlots=False)

from yade import timing
from yade import qt
qt.View()
