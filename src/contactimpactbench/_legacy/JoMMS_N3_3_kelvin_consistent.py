"""N3.3 Kelvin-viscoelastic grip-slip prototype with energy-consistent return.
The viscous velocity is the recoverable (elastic) contact-rate z = s - gamma,
not the full slip rate s. Force = -k xi - c z; xi_new = Q xi_old + h z.
Gamma is the irreversible slip rate opposed to total frictional force.
The projected total force and drilling traction obey the coupled ellipsoid.
This is a reduced phenomenological model, not shell-level validation.
"""
from dataclasses import dataclass
from math import sqrt, sin, cos, pi
import numpy as np
from scipy.optimize import brentq

m=0.62; R=0.12; I=2*m*R*R/3; mstar=m*I/(I+m*R*R)
mu=.55; P0=55.16e3; c_hc=3000.; C_T=pi*(1+1.5**2)/(1.5**2-1.); K_mat=8000.; EPS=1e-3

def kn(p): return 2*pi*R*p
def kt(p): return C_T*(p*R/2)+K_mat
def chi(delta): return (2/3)*sqrt(max(0.,2*R*delta))

@dataclass
class Result:
    w30:float; vx:float; vy:float; vz:float; w3:float; tc:float; dE:float
    max_gain:float; positive_sum:float; max_phi:float; slip_steps:int; grip_steps:int
    reversal_count:int; peakN:float; peakFt:float; peakM:float; residual_max:float
    rows:list

def simulate(w30, *, v0=(4.,0.,-4.), p=P0, dt=2e-6,tmax=.04,record=False,normal='A', zeta_t=0.25):
    vx,vy,vz=map(float,v0); w1=w2=0.; w3=float(w30)
    xi=np.zeros(2); delta=0.; t=0.; knv=kn(p); ktv=kt(p)
    if zeta_t < 0: raise ValueError("zeta_t must be nonnegative")
    ct=2*zeta_t*sqrt(ktv*mstar)
    def E():
        U = .5*knv*delta*delta if normal=='A' else pi*p*(R*delta*delta-delta**3/3)
        return .5*m*(vx*vx+vy*vy+vz*vz)+.5*I*(w1*w1+w2*w2+w3*w3)+.5*ktv*np.dot(xi,xi)+U
    E0=E(); prevE=E0; gain=0.; possum=0.; maxphi=0.; slip_steps=0; grip_steps=0
    maxres=0.; rows=[]; last_F=None; reversals=0; peakN=peakFt=peakM=0.
    nmax=int(tmax/dt)+2
    for _ in range(nmax):
        # Monotone implicit normal solve: positive N= max(0, k(delta1)* + c delta1 delta_dot)
        old_delta=delta; old_vz=vz
        def normal_force(d):
            kforce=knv*d if normal=='A' else pi*p*(2*R*d-d*d)
            vdelta=(d-old_delta)/dt
            return max(0.,kforce+c_hc*d*vdelta)
        def normal_res(d): return d-old_delta+dt*old_vz+(dt*dt/m)*normal_force(d)
        free_delta=old_delta-dt*old_vz
        if free_delta<=0:
            dnew=0.; N=0.; vznew=old_vz
        else:
            dnew=brentq(normal_res,0.,free_delta,xtol=1e-15)
            N=normal_force(dnew)
            vznew=old_vz+dt*N/m
        ch=chi(dnew); s0=np.array([vx-R*w2,vy+R*w1]); wold=w3
        theta=dt*wold
        Q=np.array([[cos(theta),-sin(theta)],[sin(theta),cos(theta)]])
        xrot=Q@xi
        # Implicit Kelvin law, analytical radial return for *total* traction.
        # z = s - gamma, xi_new = xrot + h*z, F = -k*xi_new - c*z.
        # s_new = s0 + h*F/m*. Hence, for unconstrained grip
        # Ftrial = -(k*xrot + (k*h+c)*s0)/(1+h*(k*h+c)/m*).
        Acoef=dt*ktv+ct
        Dcoef=1+dt*Acoef/mstar
        Ftrial=-(ktv*xrot+Acoef*s0)/Dcoef
        def tangential(cap):
            fn=np.linalg.norm(Ftrial)
            F=Ftrial if fn <= cap or fn==0 else Ftrial*(cap/fn)
            sn=s0+dt*F/mstar
            gamma=Dcoef*(F-Ftrial)/Acoef if Acoef>0 else np.zeros(2)
            z=sn-gamma
            xn=xrot+dt*z
            return sn,xn,F,gamma,z
        if N<=0 or ch<=0:
            p3=0.; sn=np.array(s0); xn=np.zeros(2); Ft=np.zeros(2); gamma=np.zeros(2); z=np.zeros(2); wnew=wold
        else:
            radius=mu*N
            def evaluate(q):
                cap=sqrt(max(0.,radius*radius-q*q))
                sn,xn,Ft,gamma,z=tangential(cap)
                wnew=wold-dt*ch*np.sign(wold)*q/I
                us=ch*abs(wnew)
                D=sqrt(np.dot(sn,sn)+us*us+EPS*EPS)
                return q-radius*us/D,sn,xn,Ft,gamma,z,wnew
            if abs(wold)<1e-14:
                p3=0.
            else:
                qmax=min(radius,I*abs(wold)/(dt*ch))
                p3=brentq(lambda q:evaluate(q)[0],0.,qmax,xtol=1e-12)
            _,sn,xn,Ft,gamma,z,wnew=evaluate(p3)
        M=-ch*np.sign(wold)*p3
        vx+=dt*Ft[0]/m; vy+=dt*Ft[1]/m
        w1+=dt*R*Ft[1]/I; w2-=dt*R*Ft[0]/I
        vz=vznew; w3=wnew; delta=dnew; xi=xn; t+=dt
        enew=E(); inc=enew-prevE; gain=max(gain,inc); possum+=max(0.,inc)
        # Analytical dissipation and backward Euler inertial + potential defects.
        # Scalar energy residual should be small up to the corotation convention.
        slope=(knv*dnew if normal=='A' else pi*p*(2*R*dnew-dnew*dnew))
        ddelta=(dnew-old_delta)/dt
        normal_D=dt*(N-slope)*ddelta
        plastic_D=dt*np.dot(-Ft,gamma)
        viscous_D=dt*ct*np.dot(z,z)
        spin_D=dt*ch*p3*abs(wnew)
        mech_num=.5*m*(vznew-old_vz)**2+.5*mstar*np.dot(sn-s0,sn-s0)+.5*I*(wnew-wold)**2
        spring_num=.5*ktv*np.dot(xn-xrot,xn-xrot)
        norm_num=.5*knv*(dnew-old_delta)**2 if normal=='A' else 0.
        # account for C2 potential Taylor discrepancy for model B
        if normal=='B':
            Uold=pi*p*(R*old_delta**2-old_delta**3/3)
            Unew=pi*p*(R*dnew**2-dnew**3/3)
            norm_num=slope*(dnew-old_delta)-(Unew-Uold)
        predicted=-(normal_D+plastic_D+viscous_D+spin_D+mech_num+spring_num+norm_num)
        residual=inc-predicted; maxres=max(maxres,abs(residual))
        phi=(np.dot(Ft,Ft)+p3*p3)/(mu*N)**2 if N>0 else 0.
        maxphi=max(maxphi,phi)
        if N>0:
            if np.linalg.norm(gamma)>1e-9: slip_steps+=1
            else: grip_steps+=1
            if last_F is not None and np.linalg.norm(Ft)>1e-8 and np.linalg.norm(last_F)>1e-8 and np.dot(Ft,last_F)<0: reversals+=1
            if np.linalg.norm(Ft)>1e-8:last_F=Ft.copy()
        peakN=max(peakN,N);peakFt=max(peakFt,np.linalg.norm(Ft));peakM=max(peakM,abs(M))
        if record: rows.append((t,delta,N,float(np.linalg.norm(Ft)),M,vx,vy,vz,w3,enew,inc,phi,float(np.linalg.norm(gamma)),residual,viscous_D,plastic_D))
        prevE=enew
        if dnew<=0 and vz>0: break
    return Result(w30,vx,vy,vz,w3,t,prevE-E0,gain,possum,maxphi,slip_steps,grip_steps,reversals,peakN,peakFt,peakM,maxres,rows)

if __name__=='__main__':
    for w in [0,20,100,300]:
        r=simulate(w,dt=2e-6)
        print(w,r)
