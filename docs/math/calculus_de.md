# calc/de

[Engineering Math: Vector Calculus and Partial Differential Equations](https://www.youtube.com/playlist?list=PLMrJAkhIeNNQromC4WswpU1krLOq5Ro6S)

fundamental theorem of calculus: generalized stokes theorem
gives rise to FTC in 1d, green/stokes theorem (2d/3d), gauss divergence theorem, and so on

## Generalizations of integration by parts

Divergent (original generalization):
$$\int_V f (\nabla \cdot \mathbf{A}) \, d\tau = \oint_S f \mathbf{A} \cdot d\mathbf{a} - \int_V \mathbf{A} \cdot (\nabla f) \, d\tau$$

Gradient:
$$\int_V u (\nabla v) \, d\tau = \oint_S uv \, d\mathbf{a} - \int_V v (\nabla u) \, d\tau$$

Curl:
$$\int_V \mathbf{A} \cdot (\nabla \times \mathbf{B}) \, d\tau = \int_V \mathbf{B} \cdot (\nabla \times \mathbf{A}) \, d\tau - \oint_S (\mathbf{A} \times \mathbf{B}) \cdot d\mathbf{a}$$

### Green's identities

Green’s First Identity:

$$\iiint_V (\phi \nabla^2 \psi + \nabla \phi \cdot \nabla \psi) \, dV = \oint_S (\phi \nabla \psi \cdot \mathbf{n}) \, dS$$

Derived directly by applying the Divergence Theorem to the vector field $\mathbf{F} = \phi \nabla \psi$.

Green’s Second Identity:

$$\iiint_V (\phi \nabla^2 \psi - \psi \nabla^2 \phi) \, dV = \oint_S (\phi \nabla \psi - \psi \nabla \phi) \cdot \mathbf{n} \, dS$$

This is Green's Theorem in 3D, is obtained by writing the first identity twice (swapping $\phi$ and $\psi$) and subtracting the two.
This is used to prove the uniqueness of solutions to Laplace’s and Poisson's equations.

Green’s Third Identity:

$$\phi(\mathbf{x}) = \iiint_V G \nabla^2 \phi \, dV + \oint_S (\phi \nabla G - G \nabla \phi) \cdot \mathbf{n} \, dS$$

This represents a function at a specific point $\mathbf{x}$ inside the volume based on its values and derivatives on the boundary. It uses a Green's Function ($G$).
This is the mathematical foundation for solving boundary value problems using the Boundary Element Method.

## Summary

- considering only enoughly continuous funcs/fields here
- grad: gradient of a potential function $f : \mathbb{R}^{n} \to \mathbb{R}$ which is $\nabla f : \mathbb{R}^{n} \to \mathbb{R}^{n}$
  - conservative
  - irrotational ($\nabla \times \mathbf{r} = 0$, where $\mathbf{r} = \nabla f$)
    - if $\mathbf{r} = \nabla f$ for some $f$ then $\nabla \times \mathbf{r} = 0$
    - if $\mathbf{r}$ is simply connected and $\nabla \times \mathbf{r} = 0$ then $\mathbf{r} = \nabla f$ for some $f$
  - integrating over time, it tells how much the material will move
  - grad multiplied by normalized vector gives directional derivative
- div: divergence of a vec field $\mathbf{v} : \mathbb{R}^{n} \to \mathbb{R}^{n}$ which is $\nabla \cdot \mathbf{v} : \mathbb{R}^{n} \to \mathbb{R}$
  - tells where the field has stuff going out or going in (material being expelled out/sunked in) and how much
  - integrating over time, it tells how much the material will expand/shrink
  - from divergence theorem, $\nabla \cdot \boldsymbol{\phi} = \lim_{A \to 0} \frac{1}{A} \oint_S \boldsymbol{\phi} \cdot \mathbf{n} \; dS$, where $A$ is the n-d surface enclosed by $S$
    - integrating over the normals going out of the surface
    - this gives more intuition on the result
- curl: curl of a vec field $\mathbf{v} : \mathbb{R}^{n} \to \mathbb{R}^{n}$ which is $\nabla \times \mathbf{v} : \mathbb{R}^{n} \to \mathbb{R}^{n}$
  - tells where the field rotates and how much
  - incompressible ($\nabla \cdot \mathbf{r} = 0$ where $\mathbf{r} = \nabla \times \mathbf{u}$)
    - ...
  - integrating over time, it tells how much the material will rotate
  - from stokes theorem, $\nabla \times \boldsymbol{\phi} = \lim_{A \to 0} \frac{1}{A} \oint_C \boldsymbol{\phi} \cdot d \mathbf{l}$, where $A$ is the area enclosed by $l$
    - integrating over the tangent vectors circulating around that vector at the point
    - this gives more intuition on the result
- div grad curl are all linear operators
- curl of grad = 0
- div of curl = 0

- almost all of physics boils down to some conservation law where you use gauss div/stokes theorem to derive pdes
- e.g. mass conservation:
  - total mass: $M = \iiint_{V} \rho \; dV$
  - $\frac{d}{dt} \iiint_{V} \rho \; dV = - \iint_{S} \rho \mathbf{F} \cdot d \mathbf{S} + \iiint_{V} Q \; dV$ where $S = \partial V$
    - Q is for when matter is created/destroyed inside the volume (e.g. turned into energy etc)
  - from gauss we get:
    - $\frac{ \partial \rho }{ \partial t } + \nabla \cdot \rho \mathbf{F} = Q$ (or $= 0$ if no matter is created/destroyed)
      - bc the volume integral is zero for all volumes, the integrand must be zero
      - this is the mass continuity equation
    - mass continuity eq for incompressible flows:
      - $\nabla \cdot \mathbf{F} = 0$ (bc $\nabla \rho = \frac{ \partial \rho }{ \partial t } = 0$)
  - gauss can only be applied if we have smooth $F$ (no shock waves  etc)
- e.g. to prove Kutta-Joukowski Theorem one uses stokes theorem
- e.g. track area of land with stokes theorem

- flows: all fields
- grad flows: irrotational fields ($\mathbf{F} = \nabla f$)
- potential flows: steady, irrotational and incompressible fields (or irrotational grad flows) ($\frac{ \partial \mathbf{F} }{ \partial t } = 0, \nabla \cdot \mathbf{F} = \nabla \times \mathbf{F} = 0, \mathbf{F} = \nabla f$ where $\frac{ \partial f }{ \partial t } = 0$ and $\nabla^{2} f = 0$ (this satisfies steadiness and incompressibility parts))
  - in such flows, we have both:
    - from divergence theorem, $\int_A \nabla \cdot \boldsymbol{\phi} = \oint_S \boldsymbol{\phi} \cdot \mathbf{n} \; dS = 0$, where $S = \partial A$
      - zero flux through the contour/boundary
    - from stokes theorem, $\int_A \nabla \times \boldsymbol{\phi} = \oint_C \boldsymbol{\phi} \cdot d \mathbf{l} = 0$, where $l = \partial A$
      - zero circulation through the contour
  - $\nabla^{2} f = 0$ is the laplace eq
    - solutions to laplace eq
    - e.g. complex potential $\Phi : \mathbb{C} \to \mathbb{C}$ where $\Phi (z) = \phi (x, y) + i \psi (x, y)$
      - iff $\Phi(z)$ is analytic (or holomorphic) (satisfies cauchy-riemann conditions) then:
        - both $\phi$ and $\psi$ satisfy laplaces equation
        - anti-holomorphic derivative is zero
        - holomorphic derivative becomes the real derivative
      - $\phi(x, y)$ is potential function
        - gradient: $\nabla \phi = \left( \frac{\partial \phi}{\partial x}, \frac{\partial \phi}{\partial y} \right)$
        - its gradient gives velocity field (considering $\phi$ the velocity potential in fluid dynamics then $\nabla \phi = (u, v)$)
        - this one has same structure as lagrangian
      - $\psi(x, y)$ is stream function
        - gradient: $\nabla \phi = (u, v) = \left( \frac{\partial \psi}{\partial y}, -\frac{\partial \psi}{\partial x} \right)$
        - this one has same structure as hamiltonian
          - streamlines are given by level sets of $\psi$ (where $\psi(x, y) = C$)
      - #TODO check for C^n -> C^n and for R^n, also check what is the meaning of laplacian and vector laplacian of potentials or fields
      - so these complex functions are useful for finding solutions to laplace's equations
- helmholtz/hodge decomposition: any field sufficiently smooth that decays to zero at infinity can be decomposed into a conservative irrotational gradient and a rotation only incompressible part
  - $\mathbf{F} = - \nabla \boldsymbol{\Phi} + \nabla \times \mathbf{A}$
  - irrotational fields only stretches/shrinks material
  - incompressible fields only rotate
- process for modeling dynamical system:
  - find which properties of the system are conserved
  - from that create conservation laws (probably in integral form)
  - then use gauss/stokes/other theorem to get PDEs
  - then find solution to PDEs which will be a vector field
    - the actual functions that solve the equations will be defined by boundary conditions
  - then take that vector field and imagine elements/particles (you visualize things as elements e.g. heat/electricity/mass element) in that vector field
    - you can analyze how the field will affect these elements over time
    - which will give an ode in time
  - then the vector field defines odes for elements in that field
  - which can also be integrated to get how the element moves in the field
  - or can be used for simulations cfd element methods etc
  - e.g. fluid flow
    - conservation law:
    - pde (navier stokes equation): $\frac{ \partial \mathbf{u} }{ \partial t } = f(\mathbf{u}, t)$
    - solution: vector field $\mathbf{u}(\mathbf{r}(t), t)$
      - this gives fluid velocity $\mathbf{u}(\mathbf{r}(t), t) = \dot{\mathbf{r}}(t)$
    - solution can be integrated from starting op
  - e.g. heat flow
    - conservation law:
    - pde (heat equation): $\frac{ \partial T }{ \partial t }(\mathbf{r}(t), t) = \alpha^{2} \nabla^{2} T(\mathbf{r}(t), t)$
      - $T(\mathbf{r}(t), t)$: temp distribution
      - $\alpha$: constant
    - solution:

- PDEs: usually described as function of some state $\mathbf{u}(\mathbf{r}, t)$
- canonical PDEs:
	- linear (allows superposition of solutions where you create a basis of solutions for the function space)
	- 2nd order
	- homogeneous: a function of only the dependent variable (no independent variables)
	- examples:
		- wave eq: $\frac{ \partial^{2} \mathbf{u} }{ \partial t^{2} }(\mathbf{r}, t) = c^{2} \nabla^{2} \mathbf{u}(\mathbf{r}, t)$
		- heat eq: $\frac{ \partial \mathbf{u} }{ \partial t }(\mathbf{r}, t) = \alpha^{2} \nabla^{2} \mathbf{u}(\mathbf{r}, t)$
		- laplace eq: $\nabla^{2} \mathbf{u}(\mathbf{r}, t) = 0$
- eqs that satisfy laplace eq
	- gravitation $\mathbf{F} = - \nabla \mathbf{V}, \mathbf{V} = -\frac{mMG}{r}, \nabla^{2}\mathbf{F} = 0$
	- electrostatic potential (same thing)
	- steady-state heat conduction $\frac{ \partial \mathbf{T} }{ \partial t } = \alpha^{2} \nabla^{2}T = 0$
	- incompressible irrotational flow
- poisson eq: $\nabla^{2} \phi = f$ where $f$ is a forcing function

- greens function $G$: impulse response to an inhomogeneous linear differential operator $L$
  - $LG = \delta$
  - the sol to equation $Ly = f$ is $y = (G * f)$
  - this green function is also what you use to define dirac delta function generalized to n-dim

laplacian
vector laplacian

material derivative: total acceleration $\frac{d \mathbf{u}}{dt} = \frac{D\mathbf{u}}{Dt} = \frac{ \partial \mathbf{u} }{ \partial t } + \mathbf{u} \cdot \nabla \mathbf{u}$, where $\mathbf{u}(\mathbf{r}, t)$ is velocity
Defined for any tensor field $y(\mathbf{r}, t)$: $\frac{Dy}{dt} = \frac{ \partial y }{ \partial t } + \mathbf{u} \cdot \nabla y$ where $\mathbf{u}(\mathbf{r}, t)$ is flow velocity


Heat:
$$
\rho c_{p} \frac{ \partial u }{ \partial t } - \nabla \cdot (\kappa \nabla u) - Q = 0
$$

Cauchy equilibrium:

$$
\begin{align*}
\rho \frac{D\mathbf{u}}{Dt} - \nabla \cdot \sigma + \rho \mathbf{b} &= 0
\end{align*}
$$

Navier-Stokes:

$$
\begin{align*}
\frac{ \partial \rho }{ \partial t } + \nabla \cdot (\rho \mathbf{u}) &= 0 \\
\rho \frac{D\mathbf{u}}{Dt} + \nabla p - \nabla \cdot \tau - \rho \mathbf{g} &= 0 \\
\tau &= \mu (\nabla \mathbf{u} + (\nabla \mathbf{u})^{T}) + \lambda (\nabla \cdot \mathbf{u}) I
\end{align*}
$$


TODO incompleto

https://www.youtube.com/watch?v=pvrIagjEk4c&list=PLMrJAkhIeNNQromC4WswpU1krLOq5Ro6S&index=12

https://www.youtube.com/playlist?list=PLMrJAkhIeNNR6DzT17-MM1GHLkuYVjhyt
https://www.youtube.com/playlist?list=PLMrJAkhIeNNQWO3ESiccZmPssvUDFHL4M

check SDEs
