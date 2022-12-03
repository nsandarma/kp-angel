import json
from app.models import Pegawai,Kriteria
import pandas as pd


                
def conv(j):
    if j > 85 and j <= 100:
        return 5
    elif j > 75 and j <= 85:
        return 4
    elif j > 65 and j <= 75:
        return 3
    elif j > 50 and j <= 65:
        return 2
    else:
        return 1


class SAW():
    def __init__(self):
        pegawai = Pegawai.query.all()
        kriteria = Kriteria.query.all()
        nama = []
        nip = []
        nilai = []
        for i in pegawai:
            nama.append(i.nama_pegawai)
            nip.append(i.nip)
            v_n = json.loads(i.nilai)
            
            v = [int(i) for i in v_n]
            nilai.append(v)
        n_kriteria = []
        data_kriteria = {}
        c = 1
        for j in kriteria:
            n_kriteria.append(f'c{c}')
            data_kriteria[f'c{c}'] = int(float(j.bobot_kriteria)*100)
            
            c+=1
        df = pd.DataFrame(nilai)
        df.columns = [str(j) for j in n_kriteria ]
        df.insert(loc=0,value=nip,column='NIP')
        df.insert(loc=1,value=nama,column='Nama')
        self.data = df
        self.nama = nama
        self.nip = nip
        self.nilai = nilai
        self.n_kriteria = n_kriteria
        self.data_kriteria = data_kriteria


    def dataframe_awal(self):
        return self.data
    def dataframe_bobot(self):
        nilai = []
        
        for i in self.nilai:
            v = []
            for j in i:
                v.append(conv(int(j)))
                
            nilai.append(v)
        df = pd.DataFrame(nilai)
        name_kriteria = self.n_kriteria
        df.columns = [str(j) for j in name_kriteria]
        df.insert(loc=0,value=self.nip,column='NIP')
        df.insert(loc=1,value=self.nama,column='Nama')
        self.n_2 = nilai
        return df
    def dataframe_normalisasi(self):
        
        data  = self.dataframe_bobot()
        X = data.drop(columns=['Nama','NIP'])
        nilai_norm = []
        for j in X:
            X[j] = X[j] / X[j].max()
            

        X.insert(loc=0,value=self.nip,column='NIP')
        X.insert(loc=1,value=self.nama,column='Nama')


        return X
    def dataframe_perangkingan(self):
        data = self.dataframe_normalisasi()
        data_kriteria = self.data_kriteria
        X = data.drop(columns=['Nama','NIP'])
        
        for j in X:
            X[j] = X[j] * data_kriteria[j]
            X[j] = X[j].astype('int')


        X['Total'] = X.sum(axis=1)
        X.insert(loc=0,value=self.nip,column='NIP')
        X.insert(loc=1,value=self.nama,column='Nama')
        X = X.sort_values(by=['Total'],ascending=False)
        X = X.reset_index(drop=True)
        X['Rangking'] = X.index+1
        

        

        
        return X
    def dataframe_hasil(self):
        data_rangking = self.dataframe_perangkingan()
        df = data_rangking.sort_values(by=['Nama'],ascending=True)
        # df['Rangking'] = [j for j in len(df["Nama"])]
        return df


    

        


    

        
    
    


