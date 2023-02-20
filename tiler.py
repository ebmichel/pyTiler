import numpy as np 

class tiler:
    def __init__(self,img,n,m):
        self.img=img
        self._index=-1
        self.n=n
        self.m=m
        self.y,self.x=img.shape
        self.tiles=self.tile(self.img,self.n, self.m)

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
        return tiles
    def __getitem__(self,item):
        return self.tiles[item]
    def tile(self,img,n,m):
        """
        #Used to turn an image into tiles of size n x m where n is the number of pixels in the vertical, and m the horizontal
        """
        out=[]
        
        if type(img)==list:
            img=np.array(img)
        y,x=img.shape
        xPadn=x%m
        yPadn=y%n
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
        for i in range(ny):
            for j in range(nx):
                sel=img[i*n:i*n+n,j*m:j*m+m]
                out.append(sel)


        return out
        
    def untile(self,tiles):
        """
        Used to untile the image, where y and x are the dimensions of the original image
        """
        y=self.y
        x=self.x
        img=np.zeros((y,x))
        n,m=tiles[0].shape
        xPadn=x%m
        yPadn=y%n
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

        nx=int((xPadn+x)/m)
        ny=int((yPadn+y)/n)
        c=0
        for i in range(ny):
            for j in range(nx):
                img[i*n:i*n+n,j*m:j*m+m]=tiles[c]
                c+=1

        if xPadn:
            img=img[:,0:-xPadn]
        if yPadn:
            img=img[0:-yPadn,:]
        return img


if __name__ == '__main__':
    c=retTest([1,2,3,4])
    for i in c:
        print(i)