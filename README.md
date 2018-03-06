# manhattan
[![Licence](https://img.shields.io/badge/License-LGPL%20v2.1-blue.svg?style=flat)](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)


### Test L1-norm Periodograms for Astronomy

If a signal is sparse in the Fourier domain - for example, it is the sum of a small number of coherent sinusoids - you shouldn't be using the Fourier transform or Lomb-Scargle periodogram to analyse it! 

Following the theory of compressed sensing (https://arxiv.org/abs/math/0503066), the L1 metric (sum of absolute values) turns out to be far better than the L2 metric (Euclidean distance) for inferring a sparse signal given noisy data. L1 is sometimes called the 'taxicab' or 'Manhattan' metric because in the discrete case, you can only move on a grid of streets rather than taking a diagonal.

This repo is a thin wrapper for the SPGL1 library (https://github.com/drrelyea/SPGL1_python_port) aimed at implementing a compressive sensing periodogram for astronomy. To the best of my knowledge no such code is available open-source. We closely follow Chen & Donoho, "Application of Basis Pursuit in Spectrum Estimation" (http://ieeexplore.ieee.org/document/681827/), who considered a sum of sine, cosine and Dirac terms to fit astronomical radial velocity planet signals in collaboration with Scargle; we add some polynomial terms to help take care of long term trends, with the goal of also including cotrending basis vectors to make this more applicable to Kepler/K2 data.

