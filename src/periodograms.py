import numpy as np
from sklearn.linear_model import OrthogonalMatchingPursuit
from scipy.ndimage.filters import gaussian_filter1d
from spgl1 import spg_bp, spg_lasso

'''-------------------------------------------------------
Code to use compressed sensing to generate better, faster
periodograms. The L1-norm allows you to sparsely recover
individual frequencies even when they are irregularly 
sampled and corrupted by noise - within reason.
-------------------------------------------------------'''

def basis_pursuit(t,y,fmin=None,fmax=None,nfreqs=5000,polyorder=2,
	method="basis",tau=0.1):
    ndata = np.size(y)

    trange = np.nanmax(t)-np.nanmin(t)
    dt = np.abs(np.nanmedian(t-np.roll(t,-1)))
    nt = np.size(t)

    if fmin is None:
        fmin = 1./trange
    if fmax is None:
        fmax = 2./dt

    freqs = np.linspace(fmin,fmax,nfreqs)
    df = np.abs(np.nanmedian(freqs-np.roll(freqs,-1)))

    X = np.zeros((nt,nfreqs*2+polyorder+1+ndata))

    # set up matrix of sines and cosines
    for j in range(nfreqs):
        X[:,j] = np.sin(t*freqs[j])
        X[:,nfreqs+j] = np.cos(t*freqs[j])

    # now do polynomial bits
    for j in range(polyorder+1):
    	pp = t**(polyorder-j)
        X[:,nfreqs*2 +j] = pp/np.abs(pp.max())

    # now do the dirac delta functions

    for j in range(ndata):
        X[j,-ndata+j] = 1.

    if method == "basis":
    	x,resid,grad,info = spg_bp(X, y)

    elif method == "lasso":
    	tau = 0.1
    	x, resid, grad, info = spg_lasso(X, y, tau)

    else:
    	print "Did not select a method"
    	return 0 
    power = (sines**2 + cosines**2)

    output = {'freqs':freqs,
              'sines': x[:nfreqs],
              'cosines': x[nfreqs:2*nfreqs],
              'power':power,
              'polys':x[2*nfreqs:2*nfreqs+polyorder+1],
              'diracs':x[-ndata:],
              'resid':resid,
              'grad':grad,
              'info':info,
              'coeffs':x,
              'matrix':X,
              'model':np.dot(X,x)
             }
    
    return output 


def csper(t,y,fmin=None,fmax=None,nfreqs=5000,nsines=4,polyorder=2,sig=5):
	trange = np.nanmax(t)-np.nanmin(t)
	dt = np.abs(np.nanmedian(t-np.roll(t,-1)))
	nt = np.size(t)

	# make defaults

	if fmin is None:
		fmin = 1./trange
	if fmax is None:
		fmax = 2./dt

	freqs = np.linspace(fmin,fmax,nfreqs)
	df = np.abs(np.nanmedian(freqs-np.roll(freqs,-1)))

	X = np.zeros((nt,nfreqs*2+polyorder))

	# set up matrix of sines and cosines
	for j in range(nfreqs):
		X[:,j] = np.sin(t*freqs[j])
		X[:,nfreqs+j] = np.cos(t*freqs[j])

	# now do polynomial bits
	for j in range(polyorder):
		X[:,-j] = t**(polyorder-j)

	n_components, n_features = nfreqs, nt
	n_nonzero_coefs = nsines+polyorder

	omp = OrthogonalMatchingPursuit(n_nonzero_coefs=n_nonzero_coefs)
	omp.fit(X, y-np.nanmedian(y))

	coef = omp.coef_
	idx_r, = coef[:-polyorder].nonzero()
	sines = freqs[idx_r[idx_r<nfreqs]]
	cosines = freqs[idx_r[idx_r>nfreqs]-nfreqs]
	print 'Sine components:', sines
	print 'Cosine components:',cosines

	amp_raw = np.sqrt(coef[:nfreqs]**2. + coef[nfreqs:-polyorder]**2)
	amp = gaussian_filter1d(amp_raw,sig)

	recon = np.dot(X,coef)

	output = {'Frequencies':freqs,
			  'Raw_Amplitudes':coef[:-polyorder],
			  'Polynomial':coef[-polyorder:],
			  'Reconstruction':recon,
			  'Amplitude':amp}

	return output