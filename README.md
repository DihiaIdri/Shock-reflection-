# Planar Shock Wave Reflection
## Explanation
In this code I am simplifying the problem of the bow shock reflection ahead of the projectile by treating it as a planar shock wave. 
This code replicates the reflection of a planar shock wave between two surfaces that come closer to each other.
A few assumptions are made:
1. Planar shock wave
2. Steady state
3. Ideal gas
4. Constant specific heat for now, therefore the same cp/cv ratio is used (to be changed)
5. Adiabatic
6. Neglect body forces
7. Neglect P.e
8. Projectile does not decelerate (no rarefaction waves that weaken the )

### Shock reflection
Use planar shock wave equations and the piston effect. We start by estimating the Mach number 
1. of the planar shock wave (bow shock) ahead of the projectile:
   - Consider V2 (the speed of the gas behind the shock) to be equal to the speed of the projectile. 
   - The shock travels in air at standard state
   - Once the Mach number is obtained, we can get the thermodynamic properties behind the shock
2. Shock reflected from wall
   - The gas behind the shock V2 (after reflection) must be quiescent 

Repeat 1 and 2, as long as you want. 

### Piston effect 
The previous code can also be used to estimate the speed of the bow shock, treated as a planar shock wave,
in front of the shedding as it travels at supersonic speed in air at standard condition. 
- Requires the speed of the shedding. We can plot the speed, or mach number, of the planar shock wave as a function of the 
fragments, or piston, speed. 
- Do not consider shock wave reflection. 

# To-do 
1. As temperature increases, the specific heat of the gas changes and so does the ratio of cp/cv = gamma. Ideally, 
this value should be changed as we interpolate for the Mach number... but it makes everything slightly more complicated 
because it makes the temperature and mach number equations dependent. 
   - For now, since this is just a simulation that shows that temperature can increase significantly, it doesn't really matter. 
   Perhaps, the gamma can be changed between reflections alone. 

