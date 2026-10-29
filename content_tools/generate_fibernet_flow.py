"""Generate a seeded scalar spring-network illustration for the FiberNet hero.

A graph-Laplacian spring model with one scalar displacement per node: prescribed
left/right displacements, equilibrated internal nodes, independent bond occupancy.
This is an illustrative network, not a FiberNet FEM result or measured specimen.
Only normalized edge loads and a connectivity front are exported for decoration.
Requires NumPy and SciPy for regeneration; the website build remains offline and
uses the committed JSON. Source geometry and states share the same graph IDs.
"""
from pathlib import Path
import json
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
from scipy.sparse.linalg import spsolve

ROOT = Path(__file__).resolve().parents[1]

def generate():
    rng = np.random.default_rng(291026)
    grid = np.array([[x,y,z] for x in range(11) for y in range(6) for z in range(5)], dtype=float)
    coords = grid + rng.uniform(-.44,.44,grid.shape)
    coords = (coords / [10,5,4] - .5) * [2.8,1.6,1.12]
    pairs = set()
    for a, neighbors in enumerate(cKDTree(coords).query(coords,k=6)[1]):
        for b in neighbors[1:]: pairs.add(tuple(sorted((a,int(b)))))
    edges = np.array(sorted(pairs))
    a,b = edges.T
    length = np.linalg.norm(coords[a]-coords[b],axis=1)
    stiffness = rng.uniform(.65,1.65,len(edges))**2/length
    threshold = rng.uniform(.12,.93,len(edges))
    left = np.flatnonzero(grid[:,0] == 0)
    right = np.flatnonzero(grid[:,0] == 10)
    n = len(coords)
    frames=[]; residuals=[]
    for occupancy in np.linspace(.28,.98,31):
        active = threshold <= occupancy
        aa,bb,kk = a[active],b[active],stiffness[active]
        adj=coo_matrix((np.ones(2*len(aa)),(np.r_[aa,bb],np.r_[bb,aa])),shape=(n,n)).tocsr()
        _,labels=connected_components(adj)
        spanning=np.intersect1d(labels[left],labels[right])
        load=np.zeros(len(edges)); displacement=np.zeros(n)
        front=np.full(n,1.25)
        reachable=np.isin(labels,labels[left])
        if np.any(active):
            weighted=coo_matrix((np.r_[length[active],length[active]],(np.r_[aa,bb],np.r_[bb,aa])),shape=(n,n)).tocsr()
            distance=dijkstra(weighted,directed=False,indices=left,min_only=True)
            finite=distance[np.isfinite(distance)]
            front[reachable]=distance[reachable]/max(float(np.max(finite)),1e-8)
        for group in spanning:
            members=np.flatnonzero(labels==group)
            fixed_left=np.intersect1d(members,left); fixed_right=np.intersect1d(members,right)
            inner=np.setdiff1d(members,np.r_[fixed_left,fixed_right])
            selected=active & (labels[a]==group)
            u,v,k=a[selected],b[selected],stiffness[selected]
            lap=coo_matrix((np.r_[k,k,-k,-k],(np.r_[u,v,u,v],np.r_[u,v,v,u])),shape=(n,n)).tocsr()
            displacement[fixed_right]=1
            if len(inner):
                rhs=-lap[inner][:,fixed_right].sum(axis=1).A1
                displacement[inner]=spsolve(lap[inner][:,inner],rhs)
                residuals.append(float(np.max(np.abs(lap[inner] @ displacement))))
            load[selected]=np.abs(k*(displacement[u]-displacement[v]))
        frames.append({'occupancy':round(float(occupancy),4),'load':load,'front':front,'spans':bool(len(spanning))})
    scale=max(float(np.quantile(np.concatenate([f['load'][f['load']>1e-10] for f in frames if f['spans']]),.985)),1e-8)
    for f in frames:
        f['load']=np.round(np.clip(f['load']/scale,0,1),3).tolist()
        f['front']=np.round(f['front'],3).tolist()
    data={'model':'seeded scalar spring network; graph-Laplacian equilibrium; illustrative normalized forces',
          'seed':291026,'nodes':np.round(coords,5).tolist(),'edges':edges.tolist(),
          'threshold':np.round(threshold,4).tolist(),'left':left.tolist(),'right':right.tolist(),'frames':frames}
    output=ROOT/'static/data/fibernet-flow.json';output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(data,separators=(',',':')),encoding='utf8')
    print(json.dumps({'nodes':n,'edges':len(edges),'states':len(frames),'spanning_states':sum(f['spans'] for f in frames),
                      'max_scalar_equilibrium_residual':max(residuals),'bytes':output.stat().st_size}))

if __name__=='__main__':generate()
