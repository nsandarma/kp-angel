from app import app,db

class Kriteria(db.Model):
    __tablename__ = 'kriteria'
    id_kriteria = db.Column(db.Integer,primary_key=True)
    nama_kriteria = db.Column(db.String,nullable=False)
    bobot_kriteria = db.Column(db.String,nullable=False)

    def __repr__(self) -> str:
        return {'table':self.__tablename__}

class Pegawai(db.Model):
    __tablename__ = 'pegawai'
    id_pegawai = db.Column(db.Integer,primary_key=True)
    nip = db.Column(db.String,nullable=False,unique=True)
    nama_pegawai = db.Column(db.String,nullable=False)
    jenis_kelamin = db.Column(db.String,nullable=False)
    alamat = db.Column(db.String,nullable=False)
    jabatan = db.Column(db.String,nullable=False)
    nilai = db.Column(db.String,nullable=False)

    def __repr__(self) -> str:
        return {'table':self.__tablename__}




