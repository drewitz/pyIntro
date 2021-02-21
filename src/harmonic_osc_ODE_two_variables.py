#!/usr/bin/env python3

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def model(a, t, D, m):
    """
    implementation of the differential equation
    a'(t) = model(a, t, ...)

    for this example (harmonic oscillator)
    :param a: [x, v] tuple of [amplitude, speed]
    :param t: time
    :param D: spring constant
    :param m: mass of the weight
    :return: [x', v']
    """
    xprime = a[1] # x' = v
    vprime = -D*a[0]/m # v' = -D*x/m
    return [xprime, vprime]

# initial condition
x0 = 10
v0 = 0

# time points
t0 = 0
tmax = 5
timesteps = 1000
# 'resolution' of time. the bigger, the more accurate but also slower the solution
t = np.linspace(t0, tmax, timesteps)

fig = plt.figure(figsize=(5,10))
fig.suptitle("Some Examples of the Harmonic Oscillator")

# first example
plt.subplot(311) # set subplot
D, m = (1, 1) # set parameters
plt.title(f"D = {D}, m = {m}") # set title
z1 = odeint(model, [x0, v0], t, args=(D, m)) # solve equation
plt.plot(t, z1[:,0], 'b') # plot solution

# second example
plt.subplot(312)
D, m = (1, 5) # heavier object
plt.title(f"D = {D}, m = {m} (heavy)")
z2 = odeint(model, [x0, v0], t, args=(D, m))
plt.plot(t, z2[:,0], 'r')

# third example
plt.subplot(313)
D, m = (5, 1) # strong spring
plt.title(f"D = {D} (strong), m = {m}")
z3 = odeint(model, [x0, v0], t, args=(D, m))
plt.plot(t, z3[:,0], 'g')

# show the plot
plt.show()
