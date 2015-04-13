# Autogenerated with SMOP version 
# /usr/local/bin/smop solveFB.m

from __future__ import division
try:
    from runtime import *
except ImportError:
    from smop.runtime import *

def solveFB_(I=None,alpha=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 2-[I,alpha].count(None)+len(args)

    h,w,c=size_(I,nargout=3)
    mask=(alpha >= 0.02).dot((alpha <= 0.98))
    Gx,Gy,Gd1,Gd2=getGMatByMask_(w,h,mask,nargout=4)
    G=matlabarray([[Gx],[Gy],[Gd1],[Gd2]])
    Ga=G * alpha[:]
    wgf=abs_(Ga) ** 0.5 + 0.003 * repmat_((1 - alpha[:]),4,1)
    wgb=abs_(Ga) ** 0.5 + 0.003 * repmat_(alpha[:],4,1)
    wf=(alpha[:] > 0.98) * 100 + 0.03 * alpha[:].dot((alpha[:] > 0.7)) + 0.01 * (alpha[:] < 0.02)
    wb=(alpha[:] < 0.02) * 100 + 0.03 * (1 - alpha[:]).dot((alpha[:] < 0.3)) + 0.01 * (alpha[:] > 0.98)
    wgf=spdiags_(wgf[:],0,length_(wgf),length_(wgf))
    wgb=spdiags_(wgb[:],0,length_(wgb),length_(wgb))
    wf=spdiags_(wf[:],0,length_(wf),length_(wf))
    wb=spdiags_(wb[:],0,length_(wb),length_(wb))
    for t in arange_(1,c).reshape(-1):
        tI=I[:,:,t]
        Ag=matlabarray([[wgf * G,sparse_(size_(G,1),size_(G,2))],[sparse_(size_(G,1),size_(G,2)),wgb * G]])
        bg=zeros_(size_(Ag,1),1)
        Ai=matlabarray([[wf,sparse_(w * h,w * h)],[sparse_(w * h,w * h),wb]])
        bi=matlabarray([[wf * tI[:].dot((alpha[:] > 0.02))],[wb * tI[:].dot((alpha[:] < 0.98))]])
        As=matlabarray([spdiags_(alpha[:],0,w * h,w * h),spdiags_(1 - alpha[:],0,w * h,w * h)])
        bs=tI[:]
        A=matlabarray([[Ai],[As],[Ag]])
        b=matlabarray([[bi],[bs],[bg]])
        x=numpy.linalg.solve((A.T * A),(A.T * b))
        F[:,:,t]=reshape_(x[1:w * h],h,w)
        B[:,:,t]=reshape_(x[w * h + 1:end()],h,w)
    return F,B
