import numpy as np
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'


    #--------------------------------------------------------------------------------------
    #      CONSTANTS AND INITIAL CONDITIONS

    #The distance between the dome and the landing
    h=20

    #The radius of the dome
    R=21
    #The acceleration due to gravity at an altitude
    g=(6.67408*10**(-11)*5.972*10**24)/6373421**2



    m = eval(input("What is the bodies mass in lbs? " ))
    m=m* .453592
    #print("The mass in kg is ", m)

    height= eval(input("What is the distance between the ground and the center of mass of the body in feet? "))
    height = height * .3048
    #print("the height in meters is ", height)


    #The holonomic constraint
    rho=height+R
    #print("rho=",rho)

    '''

    moment = int(input("What is the moment of inertia "))

    '''
    '''
    Iner = (2 * m * height**2)/5
    print("The moment of inertia is that of a sphere which equals ", Iner)
    '''
    Iner=0
    k = 1.2*1.3*1.7/2
    #print("the coefficient of friction is ", k)



    v_domei=eval(input("What is the initial velocity of the object in meters per second? "))



    #------------------------------------------------------------------------------------------

    #The angle which the body leaves contact with the dome
    phi_init=np.arccos(2/(3+Iner/(m*rho**2))+v_domei**2*(1+Iner/(m*rho**2))/(g*rho*(3+Iner/(m*rho**2))))
    phi_init_deg=phi_init*180/np.pi
    print(bcolors.OKBLUE+"The body leaves contact with the dome at",phi_init_deg,"degrees as measured from zenith"+bcolors.ENDC)

    vertdist=h+rho*np.cos(phi_init)

    #The total speed of the object at phi_init
    v_airi=np.sqrt((-2*g*rho**2*np.cos(phi_init)/(rho+Iner/(m*rho)))+((2*g*rho**2)/(rho+Iner/(m*rho)))+v_domei**2)
    #print("v_airi=",v_airi)

    v_verti=-v_airi*np.sin(phi_init)
    #print("v_verti=",v_verti)

    v_hori=v_airi*np.cos(phi_init)
    #print("v_hori=",v_hori)

    #-----------------------------------------------
    #Constants of Integration
    C_yairdrag=-np.sqrt(m*g/k)*np.arctanh(np.sqrt(k/(m*g))*v_verti)
    #print("C_yairdrag=",C_yairdrag)

    C_dy=(m/k)*np.log(np.cosh(np.sqrt(k/(m*g))*C_yairdrag))
    #print("C_dy=",C_dy)

    t_critdrag=(1/g)*((np.sqrt(m*g/k))*np.arccosh(np.e**((k/m)*(vertdist+C_dy)))-C_yairdrag)

    print(bcolors.OKBLUE+"By the time the body is at the level of the catwalk it has fallen for", t_critdrag,"seconds" + bcolors.ENDC)

    x_traveled=m/k*np.log(1+k*v_hori*t_critdrag/m)
    print(bcolors.OKBLUE+"it has traveled",x_traveled,"meters horizontally"+bcolors.ENDC)

    '''
    cprint("it has traveled", 'magenta', end=' ')
    cprint(x_traveled, 'red', end=' ')
    cprint("meters horizontally", 'magenta')
    '''

    answer=x_traveled+rho*np.sin(phi_init)-R
    print(bcolors.HEADER+"The total distance traveled horizontally from the beginning of the catwalk is:", answer,"meters"+bcolors.ENDC)


if __name__ == "__main__":
    app.run(debug=True)