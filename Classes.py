from myImports import *

class PersisMod():
    def __init__(self, data, rval=None):
        self.data = data
        self.pd = self.calcpersis(self.data)
        self.mapping = rval
    def calcpersis(self,data):
        diag = ripser.ripser(data)["dgms"]
        df = pd.DataFrame()
        for i in range(len(diag)):
            temp = pd.DataFrame(diag[i],columns=["Birth","Death"])
            temp["HomologyG"] = i
            df = pd.concat([df,temp])
        return df
    
    def distance_to(self, target, metric):
        if metric == "bottleneck":
            source_df = self.pd[self.pd["Death"] != float("inf")]
            target_df = target.pd[target.pd["Death"] != float("inf")]
            res = persim.bottleneck(source_df[["Birth","Death"]].values, target_df[["Birth","Death"]].values)
        return res

    def showGs(self):
        fig, ax = plt.subplots(1, 2,figsize=(7.5, 4))
        fig.tight_layout(pad=5)
        #Scatter
        ax[0].set_title("Point Cloud")
        ax[0].set_xlabel("x")
        ax[0].set_ylabel("y")
        ax[0].scatter(self.data[:,0],self.data[:,1],s=10)
        #PD
        df = self.pd.copy(deep=True)
        infrep = list(df["Death"].nlargest(2))[1]*1.02
        df.replace(float("inf"), infrep, inplace=True)
        diagonal = np.linspace(0, infrep, 250)
        infline = np.linspace(0, infrep, 250)
        ax[1].plot(diagonal,diagonal, linestyle="dashed",color="black", zorder=1)
        ax[1].plot(infline,[infrep for i in infline], linestyle="dashed",color="black",zorder=1)
        ax[1].set_title("Persistence Diagram")
        ax[1].set_xlabel("Birth")
        ax[1].set_ylabel("Death")
        hom1 = ax[1].scatter(df[df["HomologyG"]==0].Birth,df[df["HomologyG"]==0].Death,color="#83aff0",s=10)
        hom1.set_label("H0")
        hom2 = ax[1].scatter(df[df["HomologyG"]==1].Birth,df[df["HomologyG"]==1].Death,color="#2c456b",s=10)
        hom2.set_label("H1")
        
        ax[1].legend([hom1,hom2],["H0", "H1"],loc='lower right')
        plt.show()