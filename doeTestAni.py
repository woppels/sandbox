import time

from openmdao.main.api import Assembly, Component
from openmdao.lib.drivers.api import DOEdriver
from openmdao.lib.doegenerators.api import FullFactorial, Uniform
from openmdao.examples.simple.paraboloid import Paraboloid

from openmdao.lib.casehandlers.api import JSONCaseRecorder, BSONCaseRecorder


class Analysis(Assembly):

    def configure(self):

        self.add('paraboloid', Paraboloid())

        self.add('driver', DOEdriver())
        #There are a number of different kinds of DOE available in openmdao.lib.doegenerators
        #self.driver.DOEgenerator = FullFactorial(10) #Full Factorial DOE with 10 levels for each variable
        self.driver.DOEgenerator = Uniform(1000) 

        #DOEdriver will automatically record the values of any parameters for each case
        self.driver.add_parameter('paraboloid.x', low=-50, high=50)
        self.driver.add_parameter('paraboloid.y', low=-50, high=50)
        #tell the DOEdriver to also record any other variables you want to know for each case
        self.driver.add_response('paraboloid.f_xy')

        self.recorders = [JSONCaseRecorder('doe.json'), BSONCaseRecorder('doe.bson')]


if __name__ == "__main__":

	import time
	from mpl_toolkits.mplot3d import Axes3D
	from matplotlib import cm
	from matplotlib import pyplot as p
	from matplotlib import animation as animation
    
analysis = Analysis()
tt = time.time()
analysis.run()

x = analysis.driver.case_inputs.paraboloid.x
y = analysis.driver.case_inputs.paraboloid.y
f_xy = analysis.driver.case_outputs.paraboloid.f_xy
    
p.ion()
fig = p.figure()
ax = Axes3D(fig)
#ax = p.gca()
slices = range(3,len(x))[::10]
every_10 = range(3,len(x))[::10]
ims = []
for i in every_10:
	ax.clear()
	ax.set_xlim(-60,60)
	ax.set_ylim(-60,60)
	ax.set_zlim(-1000,6000)
	ax.grid(False)
	temp = ax.plot_trisurf(x[:i],y[:i],f_xy[:i], cmap=cm.jet, linewidth=0.2)
	ims.append([temp])
	p.draw()
	time.sleep(.005)
	#ani = animation.ArtistAnimation(fig, ims, interval=1, blit=True, repeat_delay=500)

ani = animation.ArtistAnimation(fig, ims, interval=1, blit=True, repeat_delay=500)
ani.save('test.mp4')

p.ioff()
print "Elapsed time: ", time.time()-tt, "seconds"
print analysis.driver.case_inputs.paraboloid.x[:5]


    
