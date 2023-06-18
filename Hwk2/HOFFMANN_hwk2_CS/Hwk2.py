#!/usr/bin/env python
# coding: utf-8

# # Ex 1

# We observe that the sh-th Fibonacci number after pk_1 is equal to F_(sk+1)\*pk_1 + F_sk\*pk_2 where F_i is the i-th Fibonacci number. To find F_(sk+1) and F_(sk), we can use the matrix form of Fibonacci numbers and do a modular sk-exponentiation on this matrix.

# In[238]:


def KeyAgreement(pk, sk):
    pk_1 = pk[0]
    pk_2 = pk[1]
    p = pk[2]
    
    # matrix form
    M = matrix([[1,1],[1,0]])
    M_sk = power_mod(M,sk,p)
    
    # M_sk corresponds to [[F_(sk+1),F_sk],[F_sk,F_(sk-1)]] mod p
    # We extract F_(sk+1) and F_(sk) to compute  F_(sk+1)*pk_1 + F_sk*pk_2
    tmp1 = mod(M_sk[0][0]*pk_1,p)
    tmp2 = mod(M_sk[0][1]*pk_2,p)
    
    return mod(tmp1+tmp2,p)


# In[241]:


Q1_pkb = [68910103607139074619233638735136130348650279779551, 437976633712782333028420861813109612570972216180558, 440024756946224539785983905910262813912044132851283]
Q1_sk = 2194811192704907032837393


# In[243]:


KeyAgreement(Q1_pkb, Q1_sk)


# # Ex 2

# In[244]:


def decryptSlovak(ct,k):
    n_cols = len(k)
    n_rows = len(ct)//n_cols
    pt = [' ' for i in range(len(ct))]
    
    for j in range(n_cols):
        for i in range(n_rows):
            pt[i*n_cols + k.index(j+1)] = ct[j*n_rows + i]
    return ''.join(pt)


# In[245]:


def remove_pad(pt,pad):
    
    pt_pad_free = ''
    idx=len(pt)-1
    while (idx>=0 and pt[idx]==pad):
        idx-=1
        
    for str_idx in range(idx+1):
        pt_pad_free += pt[str_idx]
    
    return pt_pad_free


# In[249]:


import base64

def decrypt_transposition(kI, kII, ct):
    
    col_lenI = len(ct)//len(kI)
    col_lenII = len(ct)//len(kII)
    
    for N in range(lcm(len(kI),len(kII))):

        ### process to get ct_1
        rot_kII = kII[-mod(N,len(kII)):] + kII[:-mod(N,len(kII))]
        
        ct1 = decryptSlovak(ct,rot_kII)
                
        ### process to get pt_64
        rot_kI = kI[-mod(N,len(kI)):] + kI[:-mod(N,len(kI))]
        
        pt64 = remove_pad(decryptSlovak(ct1,rot_kI),' ')
        
        ### decode pt64
        try: 
            # decode pt64 encoded in base64
            pt_ascii = base64.b64decode(pt64)
            # decode pt_ascii encoded in ascii
            pt = pt_ascii.decode('ascii')
            print (pt)
        except:
            print('-')


# In[250]:


Q2_I=[2, 11, 9, 13, 4, 14, 8, 3, 7, 10, 5, 1, 12, 6]
Q2_II=[6, 7, 3, 1, 2, 4, 5]
Q2_ct="cVGaE2vUgG ld9mnlb13hVBv3IH5y2Je3sbBZbgQh GZGniG9b uchcg Iy2cRkmG IVlalc9GIBwjQ E0mTNZm9 wYzh GGIGmGS1bhuI5bl3cWvplz ulbBZ2Bd "


# In[251]:


decrypt_transposition(Q2_I, Q2_II, Q2_ct)


# # Ex 3

# ## Part a

# In[252]:


def decryptSlovak_2(ct,k):
    n_cols = len(k)
    n_rows = len(ct)//n_cols
    pt = [' ' for i in range(len(ct))]
    
    for j in range(n_cols):
        line = []
        for i in range(n_rows):
            pt[i*n_cols + j] = ct[k.index(j)*n_rows + i]
    return ''.join(pt)


# In[253]:


def inv_phi(U,V,S):
    C = ['A','D','F','G','V','X']
    i = C.index(U)
    j = C.index(V)
    n_cols = 6
    return S[i*n_cols+j]


# In[259]:


def decrypt3a(y,S,c,s,n):
    y_1 = decryptSlovak_2(y,list(s))

    # inverse substitution (unpadded length is 2*n)
    p = ''
    for i in range(0,2*n,2):
        U = y_1[i]
        V = y_1[i+1]
        p += inv_phi(U,V,S)
    
    return p


# In[260]:


Q3a_y="DXDGVDFAVDDVAFDVVDVFFDFDDAFDDVGXFAX"
Q3a_S='IFWNV15SETL7J8ZQUY4XDMPG2KA0HR9C36BO'
Q3a_c="D"
Q3a_s=(2, 4, 6, 3, 5, 0, 1)
Q3a_n=16


# In[261]:


decrypt3a(Q3a_y,Q3a_S,Q3a_c,Q3a_s,Q3a_n)


# ## Part b

# In[262]:


def encryptSlovak(pt,k,c):
    n_cols = len(k)
    n_rows = ceil(len(pt)/n_cols)
    ct = ['' for i in range(n_cols*n_rows)]
    
    for j in range(n_cols):
        line = []
        for i in range(n_rows):
            pt_idx = i*n_cols + k[j]
            if (pt_idx>=len(pt)):
                ct[j*n_rows + i] = c
            else:
                ct[j*n_rows + i] = pt[pt_idx]

    return ''.join(ct)


# In[263]:


def phi(x,S):
    C = ['A','D','F','G','V','X']
    n_cols = 6
    idx = S.index(x)
    j = idx%n_cols
    i = (idx - j) / n_cols
    return (C[i],C[j])


# In[264]:


import string

P = string.punctuation + string.whitespace

def encrypt3b(x,S,c,s):

    # substitution
    y_sub = ''
    for i in range(len(x)):
        if (P.find(x[i]) != -1):
            y_sub += x[i]+x[i]
        else:
            (U,V) = phi(x[i],S)
            y_sub += U+V
    
    # permutation
    y_perm = encryptSlovak(y_sub,list(s),c)
    
    return y_perm


# In[265]:


Q3b_x="WELCOME TO THE BONFIRE, UNKINDLED ONE. I AM A FIRE KEEPER. I TEND TO THE FLAME, AND TEND TO THEE. THE LORDS HAVE LEFT THEIR THRONES, AND MUST BE DELIVER'D TO THEM. TO THIS END, I AM AT THY SIDE."
Q3b_S='NWZQJ1MIH3R2S5GL86EUCYFTP9A4DO7BXVK0'
Q3b_c="V"
Q3b_s=(0, 1, 4, 3, 12, 10, 8, 5, 11, 9, 2, 7, 6)


# In[266]:


encrypt3b(Q3b_x,Q3b_S,Q3b_c,Q3b_s)


# ## Part c

# In[284]:


P = string.punctuation + string.whitespace

def inv_phi_extend(U,V,S):
    if (P.find(U)!=-1 or P.find(V)!=-1):
        return U
    else:
        C = ['A','D','F','G','V','X']
        i = C.index(U)
        j = C.index(V)
        n_cols = 6
        return S[i*n_cols+j]


# In[285]:


def decrypt3c(y,S,c,s,n):
    y_1 = decryptSlovak_2(y,list(s))

    # inverse substitution (unpadded length is 2*n)
    p = ''
    for i in range(0,2*n,2):
        U = y_1[i]
        V = y_1[i+1]
        p += inv_phi_extend(U,V,S)
    
    return p


# In[292]:


import itertools
from difflib import SequenceMatcher

def find_permutation(pt,ct,incomplete_S,c):
    n = len(pt)
    for l in range(2,7):
        for s in itertools.permutations([i for i in range(l)]):
            res = decrypt3c(ct,incomplete_S.replace('\x00','*'),c,s,n)
            if (SequenceMatcher(None, res, pt).ratio()>0.3):
                print (res)
                print (s)
                print ('----------')


# In[293]:


Q3c_x0="OBI-WAN: IT'S OVER, ANAKIN! I HAVE THE HIGH GROUND! ANAKIN SKYWALKER: YOU UNDERESTIMATE MY POWER! OBI-WAN: DON'T TRY IT."
Q3c_y0="FDGD: X' FAF DAAG!D AX GA DX XAAX!ADGD DDFGAF:DF AXGADDFXGXVFFAF FD-AD VG' GD X.AX-FG:DGX XG, GDDD DVDA VGVDV FFGV DAAG GVAXAF VX GVFGXDAG F VGG! FDGD: ADX FVDGFD-AD D'DAXF,ADGD!  DXGXD DVDVFXD! GDDDXAGDGG: AAXDAFXGXDA D AFF!AX-FG:XF'GXF D."
Q3c_y1=" XGXXDA VFDDA AXVVVD, AFAFD.. X X  VFDX V DXG AF FFG DAGXDFD DFDDD FAFA DVADFDA,VDA ADXDDFVDXGXDXFD VDGD GA XD XGDXD GFDA.XADD GA AGGG FFG DDG FGDAVXFXGAXXGFG VAD G GA XVFGX GGXDA ADAD GA ADV XD, G FFFG DAG DAGADGDV GFVDFFAFXFXGXFD G GGFGFXGG. XFXG X GA XVFGX DDXGF VGXD VDDAD XDDFDADVFA FFFVVG DAFVD, XDAVADAFXD DAXG GDX VD GG AX DF AFGGAD FXGFGVFAVX A VGVDAA....A AD GXGAX D DVDAA FF,VD DAV..DGDDA AFAVAFFDDXGD. AXG FDADDV, XFGDV FF DVDXG XXG DXGGF GAD FFD XFGFVAXDDX VGAXG AXFGF XVFG VFDV VGFDXX, AXG FDX ADVG G DAD DFFX GDX A VGAFDF'DXXDFXGGGFF, VGXGXDXGF,ADAFAFX FDA XDDF FXDADXX VGG G VXGAVADADDF VADX.FAXAX D VGAFDF'DXDDDAFAXGG, FDFGX AD FFG DXGAXAF DF XDXDF,FAXFDD F GA XFADFXGDXDX ADXDA AFFGFX DX ADAF FAGAFXFXD XGDD...DGFV DF DA G  XGDD AF FF GD.. D D DFGDF F GXD FF.FGAXXVFGVDX,XGDAGXVFX  DXVG AD, AX FG VGF DFX DGAF DADXGXD GDXVDAGDGAFDF. XFGXXD XXGA,FGAXXVADXDAXX A XGG AGAGFXGDXFXD GFDA' AXDAG FAVG,XD VAG DAF D DXFAVXVFGXGXDG DG GAAV AFF A ADFF D GXDA GDAG VFDAVFVXD GFDA' DGDXG DADX,FFGGXDGGA AGX AF DADX AFXGFDDV GXGXDG V VGXGGG VAD GAGFD DXGVG VAVA GVFGXFA FGXF G GA AXVV..."
Q3c_S='9AOEZ38\x002Q\x0071J\x00\x00\x00\x00\x00N\x0040L\x00\x00\x0065\x00\x00\x00M\x00\x00\x00'
Q3c_c="V"
Q3c_H="9c95c7e362b26c49cf5a45909e4c7b57"


# In[294]:


find_permutation(Q3c_x0,Q3c_y0,Q3c_S,Q3c_c)


# In[295]:


def find_S(pt,ct,incomplete_S,s,c):
    C = ['A','D','F','G','V','X']
    n = len(pt)
    initial_S = incomplete_S.replace('\x00','*')
    S = [initial_S[i] for i in range(len(incomplete_S))]
    ct_1 = decryptSlovak_2(ct,list(s))

    for i in range(0,2*n,2):
        U = ct_1[i]
        V = ct_1[i+1]
        if (P.find(U)!=-1 or P.find(V)!=-1):
            if (V!=U):
                return -1
        elif S[C.index(U)*6+C.index(V)] == '*':
            S[C.index(U)*6+C.index(V)] = pt[i//2]
    
    return ''.join(S)


# In[296]:


find_S(Q3c_x0,Q3c_y0,Q3c_S,(2, 0, 1),Q3c_c)


# In[297]:


decrypt3c(Q3c_y1,'9AOEZ38I2QY71JR*PBKNW40L*H*65GUSMTDV',Q3c_c,(2, 0, 1),len(Q3c_y1)//2)


# In[303]:


# guess missing chars in plaintext and verify with given hash
string = "A LONG TIME AGO IN A GALAXY FAR, FAR AWAY... IT IS A PERIOD OF CIVIL WAR. REBEL SPACESHIPS, STRIKING FROM A HIDDEN BASE, HAVE WON THEIR FIRST VICTORY AGAINST THE EVIL GALACTIC EMPIRE. DURING THE BATTLE, REBEL SPIES MANAGED TO STEAL SECRET PLANS TO THE EMPIRE'S ULTIMATE WEAPON, THE DEATH STAR, AN ARMORED SPACE STATION WITH ENOUGH POWER TO DESTROY AN ENTIRE PLANET. PURSUED BY THE EMPIRE'S SINISTER AGENTS, PRINCESS LEIA RACES HOME ABOARD HER STARSHIP, CUSTODIAN OF THE STOLEN PLANS THAT CAN SAVE HER PEOPLE AND RESTORE FREEDOM TO THE GALAXY....."
import hashlib
import base64
s = string.encode()                 
r = base64.b64encode(s)
string_hash = hashlib.md5(r).hexdigest()
print (Q3c_H==string_hash)


# ## Part d

# In[304]:


Q3d_x0="OBI-WAN: IT'S OVER, ANAKIN! I HAVE THE HIGH GROUND! ANAKIN SKYWALKER: YOU UNDERESTIMATE MY POWER! OBI-WAN: DON'T TRY IT."
Q3d_y0="A AX!V G!AX:XDFAAG' A DX!X V!AV:DDGDDF' VDGXA ADX AFFAXGA  DG:  FXG FXFV GDF XFF-AVG FVD GX GF XX:FAX:  GXF VDFD FFD XGF-AXF GGV FX FD VG:DAAGD,AVVVGXDFXDX !XADX'DD FGXGDDAFAFD-VF.DFD,AGGGFXXGDVX !VDVX'VX DVDFDXDGXFV-FD.XFFXA AAX DFVAAFA  F"
Q3d_y1="V GVVAVAXAVD AV D AXFXX FGGFFADAFA DF D AGDXVX DXGDFGVVX FFDGGVDDFDVAD GGXDFX .XGV G  GDFF.AXD G GFFAG GFX D DADAD FFGAVX .FFD V  VAGD.DXF F FGGAV XDV V VGAD V F FDVDVFFXDFGDGXGDADFFA A 'DDAAXGFXXG.VDX F D FAXDGGVDAXFDVGFVAAGXD D 'DVADDFGXDF.DX XVFFVVGDX GFAFVXAAV"
Q3d_S='\x00\x005J02\x00\x00\x0081\x00\x00\x00\x00\x00\x004Q6\x009\x00\x003\x00\x00\x007\x00M\x00\x00\x00\x00\x00'
Q3d_c="X"
Q3d_s=(5, 4, 8, 2, 7, 3, 6, 1, 11, 0, 10, 9)
Q3d_H="97d50c18a9cedf33fd91a6efacbec7db"


# In[305]:


find_S(Q3d_x0,Q3d_y0,Q3d_S,Q3d_s,Q3d_c)


# In[307]:


decrypt3c(Q3d_y1,'IL5J02OST81U*PYND4Q6E9HB3R*G7WMK**VA',Q3d_c,Q3d_s,len(Q3d_y1)//2)


# In[311]:


string2 = "GOVERNOR TARKIN. I SHOULD HAVE EXPECTED TO FIND YOU HOLDING VADER'S LEASH. I RECOGNIZED YOUR FOUL STENCH WHEN I WAS BROUGHT ONBOARD."
import hashlib
import base64
s = string2.encode()                 
r = base64.b64encode(s)
string_hash = hashlib.md5(r).hexdigest()
print (Q3d_H==string_hash)


# In[ ]:




