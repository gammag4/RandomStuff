
equacao pra transformar $K[R t]v$ de coords do sensor pra range (0, 1)
w h sao width height em pixels
x y z e o vetor depois da transformacao (x, y, z) = K[R t]v
vendo a matriz K para cameras reais temos

((x - z x0) / w + z 0.5, (y - z y0) / h + z 0.5, z)

essa equacao da a matriz:

$$
M =
\begin{bmatrix}
  \frac{1}{w} & 0 & 0.5 - \frac{x_{0}}{w} \\
  0 & \frac{1}{h} & 0.5 - \frac{y_{0}}{h} \\
  0 & 0 & 1
\end{bmatrix}
$$

dai da pra reescrever o vetor transformado como:

(x', y', z') = MK[R t]v

onde MK e

$$
MK =
\begin{bmatrix}
  \frac{f_{x}}{w} & \frac{s}{w} & 0.5 \\
  0 & \frac{f_{y}}{h} & 0.5 \\
  0 & 0 & 1
\end{bmatrix}
$$

dai da pra usar isso pra calcular a transformacao inversa, onde voce consegue transformar qualquer pixel no range (0, 1) pra o respectivo raio no mundo

the question is, after subtracting (x0, y0), i should calibrate by dividing it by (w, h) or by (2 x0, 2 y0)? i assumed it should be divided by (w, h) bc it is in pixel coordinates, so it makes sense, but maybe it is in the range of (0, 2 x0)
if this is not true, search for "Convert an intrinsic matrix from pixel coordinates to normalized image coordinates (range)"
if nothing found tell in tcc and say you assumed that, maybe even test with both in the datasets

talvez nao precise fazer essa transformacao
porque o que ta invertido e o y (que faz sentido pq quando renderiza e de cima pra baixo) e o z (que tb faz sentido pq mao direita)
