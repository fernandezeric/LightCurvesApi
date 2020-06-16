from flask import Flask,request,send_file,jsonify, make_response
from methods.metodos_ps1 import *
from methods.metodos_ztf import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Buenos Días, ChikiMan <3!'

#buscar por radio y que devuelva el id en ese catalogo
@app.route('/radio-degree',methods=['POST'])
def radiodegree():

    ra = request.form['ra']
    dec = request.form['dec']
    radius = request.form['radius']
    format = request.form['format']

    if format not in {'csv','votable'}: 
        return "Record not found", status.HTTP_400_BAD_REQUEST 
    
    dic = {}
    if 'ps1' in request.form['catalog']:
        ps1 = ps1curves(ra,dec,radius,format,False)
        jsonify(ps1)
        dic['curve_ps1'] = ps1

    if 'ztf' in request.form['catalog']:
        ztf = zftcurves(ra,dec,radius,format,False)
        jsonify(ztf)
        dic['curve_ztf'] = ztf
        
    return make_response(jsonify(dic))

@app.route('/radio-degree-nearest',methods=['POST'])
def radio_degree_nearest():
    ra = request.form['ra']
    dec = request.form['dec']
    radius = request.form['radius']
    format = request.form['format']

    if (checkformat(format)): 
        return "Bad value for format" 
    
    dic = {}
    if 'ps1' in request.form['catalog']:
        ps1 = ps1curves(ra,dec,radius,format,True)
        jsonify(ps1)
        dic['curve_ps1'] = ps1

    if 'ztf' in request.form['catalog']:
        ztf = zftcurves(ra,dec,radius,format,True)
        jsonify(ztf)
        dic['curve_ztf'] = ztf

    return make_response(jsonify(dic))

@app.route('/radio-hours',methods=['POST'])
def radiohours():
    coord = SkyCoord(request.form['hours'],frame='icrs')
    ra = coord.ra.degree
    dec = coord.dec.degree
    radius = request.form['radius']
    format = request.form['format']

    if (checkformat(format)): 
        return "Bad value for format" 
    
    dic = {}
    if 'ps1' in request.form['catalog']:
        ps1 = ps1curves(ra,dec,radius,format,False)
        jsonify(ps1)
        dic['curve_ps1'] = ps1

    if 'ztf' in request.form['catalog']:
        ztf = zftcurves(ra,dec,radius,format,False)
        jsonify(ztf)
        dic['curve_ztf'] = ztf

    return make_response(jsonify(dic))


if __name__ == "__main__":
 app.run()

