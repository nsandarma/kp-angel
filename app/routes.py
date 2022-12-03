import json
from app import app,render_template,request,session,redirect,Pegawai,db
from app.models import Kriteria
from app.saw import SAW

######################################################################

# Login & Logout
@app.route('/',methods=['GET','POST'])
def home():
    log = session.get('key')
    if log == True:
        return redirect('/dashboard')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username=='admin' and password == 'admin':
            session['key'] = True
            return redirect('/dashboard')
        else:
            session['message'] = 'Username or password Salah'
            return redirect('/')

    return render_template('login.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


####################################################################
#Dashboard
@app.route('/dashboard')
def dashboard():
    log = session.get('key')
    if log == True:

        return render_template('beranda.html')
    else :
        return redirect('/')

####################################################################
# Pegawai
@app.route('/pegawai')
def pegawai():
    log = session.get('key')
    data = Pegawai.query.all()
    
    if log == True:
        return render_template('pegawai/pegawai.html',data=data)
    else :
        return redirect('/')

@app.route('/pegawai/tambah-pegawai',methods=['GET','POST'])
def tambah_pegawai():
    log = session.get('key')
    if log == True:
        if request.method == 'POST':
            nip = request.form['nip']
            nama_pegawai = request.form['nama']
            jenis_kelamin = request.form['jenis_kelamin']
            alamat = request.form['alamat']
            jabatan = request.form['jabatan']
            nilai = ""
            q = Pegawai(nip=nip,nama_pegawai=nama_pegawai,
            alamat=alamat,jenis_kelamin=jenis_kelamin,
            jabatan=jabatan,nilai=nilai)
            db.session.add(q)
            db.session.commit()
            return redirect('/pegawai')
        return render_template('pegawai/tambah_pegawai.html')
    else :
        return redirect('/')

@app.route('/pegawai/detail-pegawai/<nip>')
def detail_pegawai(nip):
    log = session.get('key')
    if log == True:
        data = Pegawai.query.filter_by(nip=nip).first()
        return render_template('pegawai/detail_pegawai.html',data=data)
    else :
        return redirect('/')
@app.route('/pegawai/edit-pegawai/<nip>',methods=['GET','POST'])
def edit_pegawai(nip):
    log = session.get('key')
    if log == True:
        data = Pegawai.query.filter_by(nip=nip).first()
        if request.method =='POST':
            nip = request.form['nip']
            nama_pegawai = request.form['nama']
            jenis_kelamin = request.form['jenis_kelamin']
            alamat = request.form['alamat']
            jabatan = request.form['jabatan']
            nilai = ""
            data.nip = nip
            data.nama_pegawai = nama_pegawai
            data.jenis_kelamin = jenis_kelamin
            data.alamat = alamat
            data.jabatan = jabatan
            data.nilai = nilai
            db.session.commit()
            return redirect('/pegawai')
        return render_template('pegawai/edit_pegawai.html',data=data)
    else :
        return redirect('/')
@app.route('/pegawai/hapus-pegawai/<nip>')
def hapus_pegawai(nip):
    log = session.get('key')
    if log == True:
        q = Pegawai.query.filter_by(nip=nip).first()
        db.session.delete(q)
        db.session.commit()
        return redirect('/pegawai')
    else:
        return redirect('/')

####################################################################
# KRITERIA
@app.route('/kriteria')
def kriteria():
    log = session.get('key')
    if log == True:
        data = Kriteria.query.all()
        return render_template('kriteria/kriteria.html',data=data)
    else :
        return redirect('/')

@app.route('/kriteria/tambah-kriteria',methods=['GET','POST'])
def tambah_kriteria():
    log = session.get('key')
    if log == True:
        if request.method == 'POST':
            nama_kriteria = request.form['nama_kriteria']
            bobot = request.form['bobot']
            bobot = int(bobot)/100
            q = Kriteria(nama_kriteria=nama_kriteria,bobot_kriteria=bobot)
            db.session.add(q)
            db.session.commit()
            return redirect('/kriteria')
            
        return render_template('kriteria/tambah_kriteria.html')
    else :
        return redirect('/')
@app.route('/kriteria/detail-kriteria/<id>')
def detail_kriteria(id):
    log = session.get('key')
    if log == True:
        li = ['86-100','76-85','66-75','51-65','0-50']
        p = [i for i in range(0,len(li))]
        ket = ['Sangat Baik','Baik','Cukup','Kurang','Sangat Kurang']
        nilai = [i for i in range(len(li),0,-1)]
        d = {'list':li,'ket':ket,'nilai':nilai}
        data = Kriteria.query.filter_by(id_kriteria=id).first()
        return render_template('kriteria/detail_kriteria.html',data=data,p=p,d=d)
    else :
        return redirect('/')
    
@app.route('/kriteria/edit-kriteria/<id>',methods=['GET','POST'])
def edit_kriteria(id):
    log = session.get('key')
    if log == True:
        data = Kriteria.query.filter_by(id_kriteria=id).first()
        if request.method == 'POST':
            nama_kriteria = request.form['nama_kriteria']
            bobot_kriteria = request.form['bobot_kriteria']
            data.nama_kriteria = nama_kriteria
            data.bobot_kriteria = bobot_kriteria
            db.session.commit()
            return redirect('/kriteria')
        return render_template('kriteria/edit_kriteria.html',data=data)
    else :
        return redirect('/')

@app.route('/kriteria/hapus-kriteria/<id>')
def hapus_kriteria(id):
    log = session.get('key')
    if log == True:
        q = Kriteria.query.filter_by(id_kriteria=id).first()
        db.session.delete(q)
        db.session.commit()
        return redirect('/kriteria')
    else :
        return redirect('/')


####################################################################
# Penilaian & SAW
@app.route('/penilaian',methods=['GET','POST'])
def penilaian():
    log = session.get('key')
    kr = Kriteria.query.all()
    if log == True:
        dp = Pegawai.query.all()
        if request.method == 'POST':
            u = request.form['user']
            user = Pegawai.query.filter_by(id_pegawai=u).first()
            data_nilai = []
            for i in kr:
                v = request.form[i.nama_kriteria]
                data_nilai.append(v)
            data = json.dumps(data_nilai)
            user.nilai = data
            db.session.commit()

            return redirect(f'/pegawai/detail-pegawai/{user.nip}')
        return render_template('saw/penilaian.html',dp=dp,kr=kr)
    else :
        return redirect('/')

@app.route('/klasifikasi')
def klasifikasi():
    return "klasifikasi"


@app.route('/laporan')
def laporan():
    log = session.get('key')
    if log == True:
        pegawai = Pegawai.query.all()
        kriteria = Kriteria.query.all()
        saw = SAW()
        data = saw.dataframe_awal()
        bobot = saw.dataframe_bobot()
        norm = saw.dataframe_normalisasi()
        rangking = saw.dataframe_perangkingan()

        


        len_data = [int(i) for i in range(len(data))]
        return render_template('saw/laporan.html',len_data=len_data,data_awal=data,data_bobot=bobot,data_norm=norm,rangking=rangking,kriteria=kriteria)
        # return f'{rangking}'
        
        
        

        



        

    else:
        return redirect('/')
    
    

