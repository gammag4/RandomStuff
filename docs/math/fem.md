
### B-Splines

B-Spline:

$$
\begin{align*}
B_{i, n}(x) &= \frac{x - k_{i}}{k_{i + n} - k_{i}} B_{i, n - 1}(x) + \frac{k_{i + n + 1} - x}{k_{i + n + 1} - k_{i + 1}} B_{i + 1, n - 1}(x) \\
B_{i, 0}(x) &= 1 \text{ if } k_{i} \leq x < k_{i + 1}, 0 \text{ otherwise} \\
B_{(i, j, k), n}(x, y, z) &= B_{i, n}(x) B_{j, n}(y) B_{k, n}(z) \\
\end{align*}
$$

When it is equally distributed into intervals of size $l$ starting at 0:

$$
\begin{align*}
B_{i, n}(x) &= \frac{x - i l}{n l}B_{i, n - 1}(x) + \frac{(i + n + 1) l - x}{n l}B_{i + 1, n - 1}(x) \\
\frac{dB_{i, n}}{dx}(x) &= \frac{B_{i, n - 1}(x) - B_{i + 1, n - 1}(x)}{l} \\
\int B_{i, n}(x) \, dx &= C + \frac{(n + 1) l}{n + 1} \sum_{j=i}^{\infty} B_{i, n + 1}(x)
\end{align*}
$$

B-Splines satisfy partition of unity property: $\sum_{ijk} \phi_{ijk}(\mathbf{x}) = 1$
Proof is trivial from definition above

## Heat Diffusuion Model

### PDE

$$
\rho c_{p} \frac{ \partial u }{ \partial t } - \nabla \cdot (\kappa \nabla u) - Q = 0
$$

- $u(\mathbf{r}, t)$ is temp at position $\mathbf{r}$ time $t$
- $\alpha = \frac{\kappa}{\rho c_{p}}$ is thermal difusivity
- $\rho, c_{p}$ are scalars
- $\kappa$ is a tensor if anisotropic or scalar if isotropic
- $Q$ represents internal sources or sinks
- $u_{ext}$ is constant, the temp at external environment
- $h$ is heat transfer coefficient (it depends of conditions of external environment which change overtime, for air approximate it to 5-10 W/m^2K)

### Weak form

$$
\begin{align*}
\int_{\Omega} \rho c_{p} \frac{ \partial u }{ \partial t } \phi \, d\Omega - \int_{\Omega} \nabla \cdot (\kappa \nabla u) \phi \, d\Omega - \int_{\Omega} Q \phi \, d\Omega &= 0 \\
\int_{\Omega} \rho c_{p} \frac{ \partial u }{ \partial t } \phi\, d\Omega - \int_{\partial\Omega} \phi (\kappa \nabla u) \cdot \, d\mathbf{\Sigma} + \int_{\Omega} (\kappa \nabla u) \cdot \nabla \phi \, d\Omega - \int_{\Omega} Q \phi \, d\Omega &= 0 \text{ (applying div variation of integration by parts in second term)} \\
\int_{\Omega} \rho c_{p} \frac{ \partial u }{ \partial t } \phi\, d\Omega + \int_{\partial\Omega} \phi h (u - u_{ext}) \, d\Sigma + \int_{\Omega} (\kappa \nabla u) \cdot \nabla \phi \, d\Omega - \int_{\Omega} Q \phi \, d\Omega &= 0 \text{ (Robin boundary condition in second term)} \\
\sum_{ijk} \left(\rho c_{p} \frac{dc_{ijk}}{dt} \int_{\Omega} \phi_{ijk} \phi_{abc} \, d\Omega + \kappa c_{ijk} \int_{\Omega} \nabla \phi_{ijk} \cdot \nabla \phi_{abc} \, d\Omega + h c_{ijk} \int_{\partial\Omega} \phi_{ijk} \phi_{abc} \, d\Sigma \right) - h u_{ext} \int_{\partial\Omega} \phi_{abc} \, d\Sigma - \int_{\Omega} Q \phi_{abc} \, d\Omega &= 0 \text{ (Eq abc Assuming isotropic constant material)} \\
\end{align*}
$$

### Temperature

Here we are approximating temp $u$ with b-splines:

$$
\begin{align*}
u(\mathbf{r}, t) &= \sum_{ijk} c_{ijk}(t) \phi_{ijk}(\mathbf{r}) \\
\frac{ \partial u }{ \partial t }(\mathbf{r}, t) &= \sum_{ijk} \frac{dc_{ijk}}{dt}(t) \phi_{ijk}(\mathbf{r}) \\
\nabla u(\mathbf{r}, t) &= \sum_{ijk} c_{ijk}(t) \nabla \phi_{ijk}(\mathbf{r}) \\
\end{align*}
$$

Remember that $\mathbf{c}$ is not the temperatures because the b-spline does not pass through the points, so for initial $\mathbf{c}$ you have to compute it with an algebraic method from starting temps.

### Laser beam

The laser is modeled using the Volumetric Beer-Lambert model:

$$
Q(\mathbf{r}, t) = \frac{2AP}{\pi r_{l}^{2}}\exp\left( -2 \frac{(x - r_{x}(t))^{2} + (z - r_{z}(t))^{2}}{r_{l}^{2}} \right) \cdot \alpha \exp(-\alpha y)
$$

Where $\mathbf{r}(t) = (r_{x}(t), r_{y}(t))$ is the velocity it travels and $y$ must start at the surface of the material and get more positive as you get deeper into the material.

Also, considering that the region where the laser beam acts is very small, if numerical integration methods are used, one should integrate over a really small region around the sensor.

Visualizing the model as a normal distribution with $\sigma = r_{l}$, we can get 99.9937% of the distribution by integration in the range $\pm 4\sigma$ in both x and z and  the range $\left[ 0, \frac{10}{\alpha} \right]$ in y for 99.9954% which would give both 99.9891%, or we could use $\pm 3\sigma$ for x and z and $\left[ 0, \frac{5}{\alpha} \right]$ for 99.05%.

### Matrix form

Now we turn the integrands into matrices/vectors:

$$
\begin{align*}
M_{abc, ijk} &= \int_{\Omega} \phi_{ijk} \phi_{abc} \, d\Omega \text{ (constant over time, just computed once, except if the boundary changes over time)} \\
K_{abc, ijk} &= \int_{\Omega} \nabla \phi_{ijk} \cdot \nabla \phi_{abc} \, d\Omega \text{ (constant over time, just computed once, except if the boundary changes over time)} \\
B_{abc, ijk} &= \int_{\partial\Omega} \phi_{ijk} \phi_{abc} \, d\Sigma \text{ (constant over time, just computed once, except if the boundary changes over time)} \\
\mathbf{b} &= \left\lbrace \int_{\partial\Omega} \phi_{abc} \, d\Sigma \right\rbrace_{abc} \text{ (constant over time, just computed once, except if the boundary changes over time)} \\
\mathbf{f} &= \left\lbrace \int_{\Omega} Q \phi_{abc} \, d\Omega \right\rbrace_{abc} \text{ (changes over time, but for some cases (e.g. laser) can be precomputed as switching states kernel (e.g. turning on/off))} \\
\mathbf{c} &= \{ c_{ijk} \}_{ijk} \text{ (changes over time)} \\
\end{align*}
$$

From this, we get:

$$
\begin{align*}
\rho c_{p} M \frac{d\mathbf{c}}{dt} + (\kappa K + h B) \mathbf{c} - h u_{ext} \mathbf{b} - \mathbf{f} &= \mathbf{0} \\
\left( \rho c_{p} M + \Delta t (\kappa K + h B) \right) \mathbf{c} - \rho c_{p} M \mathbf{c}_{last} - \Delta t h u_{ext} \mathbf{b} - \Delta t \mathbf{f} &= \mathbf{0} \text{ (using } \frac{d\mathbf{c}}{dt} \approx \frac{\mathbf{c} - \mathbf{c}_{last}}{\Delta t} \text{)} \\
( M_{2} + \Delta t B_{2} ) \mathbf{c} - M_{2} \mathbf{c}_{last} - \Delta t (\mathbf{b}_{2} + \mathbf{f}) &= \mathbf{0} \\
M_{2} &= \rho c_{p} M \\
B_{2} &= \kappa K + h B \\
\mathbf{b}_{2} &= h u_{ext} \mathbf{b} \\
\end{align*}
$$

Values chosen for variables:

These values were chosen to approximate an lpbf scenario with a laser beam that melts stainless steel metal powder, in SI units.

$$
\begin{align*}
\rho &= 0.5 \cdot 8000 \text{ (0.4-0.6 $\cdot \rho_{solid}$ which is 8000)} \\
c_{p} &= 500 \text{ (450-500 room temp, 700-800 melting point)} \\
\kappa &= 0.5 \text{ (0.4-0.55)} \\
h &= 15 \text{ (10-25)} \\
u_{ext} &= 300 \text{ (room temp)} \\
A &= 0.35 \text{ (0.3-0.4)} \\
P &= 200 \text{ (150-300)} \\
r_{l} &= 0.00004 \text{ (35-50 um)} \\
v &= 0.8 \text{ (600-1200mm/s)} \\
\alpha &= 4 \cdot 10^{4} \text{ (3.3-5 $\cdot 10^{4}$)} \\
\end{align*}
$$

## Optimization

Considering a set of b-splines of degrees $n$ index $i$ and interval $l$, which would have $n + 2$ control points, the range where it is non-zero is $(i, (n + i + 1) l)$.
That means that considering two b-splines indices $i_{1}, i_{2}, i_{1} < i_{2}$ and degrees $n_{1}, n_{2}$ their product is only nonzero in the window given by $(i_{1}, (n_{1} + i_{1} + 1) l) \cup (i_{2}, (n_{2} + i_{2} + 1) l) = (i_{2}, (n_{1} + i_{1} + 1)l)$ and it is zero everywhere for $i_{2} > (n_{1} + i_{1} + 1)l$.

Also considering that we are only integrating over cubic volumes or surfaces, we can visualize such integrals as sums of integrals over intervals of size $l$.
With that, we could build matrices that represent the combinations of integrations in such windows for specific positions in volume:

Integrating $\phi_{000}$ over side s of boundary given by $(i_{3}, j_{3}, k_{3}) - (i_{3} + l, j_{3} + l, k_{3} + l)$:

$$
\begin{align*}
I_{v}(s, i_{3}j_{3}k_{3}) &= \int_{\partial_{s} \Omega_{i_{3}j_{3}k_{3}}} \phi_{000} \, d\Sigma \\
& \Omega_{i_{3}j_{3}k_{3}} = [i_{3}, i_{3} + l] \times [j_{3}, j_{3} + l] \times [k_{3}, k_{3} + l] \\
& i_{3}, j_{3}, k_{3} \in [0, n] \\
\end{align*}
$$

Integrating $\phi_{ijk}\phi_{nnn}$ over side s of boundary given by $(i_{3}, j_{3}, k_{3}) - (i_{3} + l, j_{3} + l, k_{3} + l)$:

$$
\begin{align*}
I_{b}(s, ijk, i_{3}j_{3}k_{3}) &= \int_{\partial_{s} \Omega_{i_{3}j_{3}k_{3}}} \phi_{ijk} \phi_{nnn} \, d\Sigma \\
& \Omega_{i_{3}j_{3}k_{3}} = [i_{3}, i_{3} + l] \times [j_{3}, j_{3} + l] \times [k_{3}, k_{3} + l] \\
& i, j, k \in [0, 2n] \\
& i_{3}, j_{3}, k_{3} \in [0, 3n] \\
\end{align*}
$$

Integrating $\phi_{ijk}\phi_{i_{2}j_{2}k_{2}}$ over volume given by $(i_{3}, j_{3}, k_{3}) - (i_{3} + l, j_{3} + l, k_{3} + l)$:

$$
\begin{align*}
I_{p}(ijk, i_{2}j_{2}k_{2}, i_{3}j_{3}k_{3}) &= \int_{\Omega_{i_{3}j_{3}k_{3}}} \phi_{ijk} \phi_{i_{2}j_{2}k_{2}} \, d\Omega \\
& \Omega_{i_{3}j_{3}k_{3}} = [i_{3}, i_{3} + l] \times [j_{3}, j_{3} + l] \times [k_{3}, k_{3} + l] \\
& i, j, k \in [0, 2n] \\
& i_{3}, j_{3}, k_{3} \in [0, 3n] \\
\end{align*}
$$

Integrating $\nabla \phi_{ijk} \cdot \nabla \phi_{i_{2}j_{2}k_{2}}$ over volume given by $(i_{3}, j_{3}, k_{3}) - (i_{3} + l, j_{3} + l, k_{3} + l)$:

$$
\begin{align*}
I_{g}(ijk, i_{2}j_{2}k_{2}, i_{3}j_{3}k_{3}) &= \int_{\Omega_{i_{3}j_{3}k_{3}}} \nabla \phi_{ijk} \cdot \nabla \phi_{i_{2}j_{2}k_{2}} \, d\Omega \\
& \Omega_{i_{3}j_{3}k_{3}} = [i_{3}, i_{3} + l] \times [j_{3}, j_{3} + l] \times [k_{3}, k_{3} + l] \\
& i, j, k \in [0, 2n] \\
& i_{3}, j_{3}, k_{3} \in [0, 3n] \\
\end{align*}
$$

Here, $s \in [0, 5]$ (side -x +x -y +y -z +z).
Also the boundaries for $\phi_{000}$ and $\phi_{nnn}$ were chosen in such a way where it only sweeps nonzero regions.

TODO fix the ranges for x y z are wrong they must be in the middle of the spline

## Vector formulation

We can visualze B-Splines as vectors in a polynomial vector space.
This allows us to visualize its products as bilinear maps on two vectors, which can be represented by tensors.
Integration and derivation also becomes a straightforward linear operation on these vectors.
This also allows us to generalize to any curve that can be represented (including the general function for external heat $Q(\mathbf{r}, t)$ ).

TODO
