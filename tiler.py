import numpy as np 
from copy import deepcopy
class tiler:
    def __init__(self,img,n,m,overlap=0):
        self.img=img
        self._index=-1
        self.n=n
        self.m=m
        self.nx=0
        self.ny=0
        self.xPadn=0
        self.yPadn=0
        self.overlap=overlap
        self.y,self.x=img.shape
        self.tiles=self.tile(self.img,self.n, self.m,self.overlap)

    def __iter__(self):
        return self
    def __next__(self):
        self._index+=1
        if self._index>=len(self.tiles):
            self._index-=1
            raise StopIteration
        else:
            return self.tiles[self._index]
    def __list__(self):
        t=deepcopy(self.tiles)
        return t
    def __getitem__(self,item):
        return self.tiles[item]


    
    def tile(self,img,n,m,overlap=0):
        """
        Used to turn an image into tiles of size n x m where n is the number of pixels in the vertical, and m the horizontal pixels
        """
        out=[]
        T=[] #coord bounds of usable data
        R=[] #true coord bounds of 
        
        if type(img)==list:
            img=np.array(img)
        y,x=img.shape
        xPadn=x%m
        yPadn=y%n

        self.xPadn=xPadn
        self.yPadn=yPadn

        if xPadn:
            xPadn+=-1
            xPad=np.zeros((y,xPadn))
            img=np.hstack((img,xPad))
        if yPadn:
            yPadn+=-1
            if xPadn:
                yPad=np.zeros((yPadn,x+xPadn))
            else:
                yPad=np.zeros((yPadn,x))
            img=np.vstack((img,yPad))

        py,px=img.shape
        nx=int(px/m)
        ny=int(py/n)
        self.nx=nx
        self.ny=ny
        #at this point, image is ready, & have number of tiles
        if overlap:
            oxPad=np.zeros((py,overlap))
            img=np.hstack((oxPad,img,oxPad))

            oyPad=np.zeros((overlap,px+overlap*2))
            img=np.vstack((oyPad,img,oyPad))

        for i in range(overlap,ny+overlap):
            for j in range(overlap,nx+overlap):
                sel=img[(i-overlap)*n:(i-overlap)*n+n+overlap*2,(j-overlap)*m:(j-overlap)*m+m+overlap*2]
                out.append(sel)


        return out
        
    def untile(self,tiles):
        """
        Used to untile the image, where y and x are the dimensions of the original image
        """
        y=self.y
        x=self.x
        nx=self.nx
        ny=self.ny
        n=self.n
        m=self.m
        overlap=self.overlap
        img=np.zeros((y+self.yPadn,x+self.xPadn))
        c=0
        for i in range(ny):
            for j in range(nx):
                img[i*n:i*n+n,j*m:j*m+m]=tiles[c][overlap:-overlap,overlap:-overlap]
                c+=1

        if self.xPadn:
            img=img[:,0:-self.xPadn]
        if self.yPadn:
            img=img[0:-self.yPadn,:]
        return img

