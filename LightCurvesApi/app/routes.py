from flask import request,send_file,jsonify, make_response
from flasgger import Swagger
from astropy.coordinates import SkyCoord
from app.catalogs.ps1 import metodos_ps1 as mps1
from app.catalogs.ztf import metodos_ztf as mztf
from app import app

swagger = Swagger(app)


def generic_request(request,nearest=False):
    print(request)

    if "hours" in request.form:
        coord = SkyCoord(request.form['hours'],frame='icrs')
        ra = coord.ra.degree
        dec = coord.dec.degree

    else:
        print("1")
        ra = request.form['ra']
        dec = request.form['dec']

    radius = request.form['radius']
    catalog = request.form['catalog']
    format = request.form['format']

    dic = {}
    if 'ps1' in catalog :
        ps1 = mps1.ps1curves(ra,dec,radius,format,nearest)
        jsonify(ps1)
        dic['curve_ps1'] = ps1

    if 'ztf' in catalog:
        ztf = mztf.zftcurves(ra,dec,radius,format,nearest)
        jsonify(ztf)
        dic['curve_ztf'] = ztf

    return jsonify(dic)


@app.route('/')
def hello_world():
    """ Example for swagger, this rute return a sweet message
        to ChikiMan.
        ---
        definitions:
            mensaje:
                type: string
                                   
        responses:
            200:
                description: Print in rute a message.
            schema:
                $ref: '#/definitions/mensaje'

    """

    return 'Buenos Días, ChikiMan <3!'


#buscar por radio y que devuelva el id en ese catalogo
@app.route('/radio-degree',methods=['POST'])
def radiodegree():
    """ Return in dictionary with all data for the light curve objects from api ztf or ps1 in a radio.
        ---
        parameters:
            - name: ra
              in: formData
              type: string 
              required: true
              default: 139.33444972
              required: true
              default: 68.6350604

            - name: radius
              in : formData
              type: string
              required: true
              default: 0.0002777

            - name: format
              in: formData
              type: string
              enum: ['csv', 'votable']
              required: true
              default: csv

            - name: catalog
              in: formData
              type: string
              required: true
              enum: ['ztf', 'ps1','ztf,ps1']
              required: true
              default: 'ztf,ps1'

        definitions:
            subdictionary:
                type: object
                additionalProperties:
                    type: string
                   

            dictionary:
                type: object
                additionalProperties:
                    type: objetc
                    $ref:  '#/definitions/subdictionary'
                example:
                    {
                        curve_ztf : {
                                id1_object_ztf : data(csv/votable) in string,
                                id2_object_ztf : data(csv/votable) in string,
                            },
                        curve_ps1 : {
                                id1_object_ps1 : data(csv/votable) in string,
                                id2_object_ps1 :  data(csv/votable) in string
                        }
                    }

        responses:
            200:
                description: Dictionary with contein first value:key, with value is a catalog selected and value is
                                a dictionary with key:value when key is a id in respective catalog and key is information in
                                format request
                
               
                schema:
                    $ref: '#/definitions/dictionary'

    """
    format = request.form['format']

    if format not in {'csv','votable'}: 
        return "Record not found", status.HTTP_400_BAD_REQUEST 

    res = generic_request(request,False)    
    return make_response(res)

@app.route('/radio-degree-nearest',methods=['POST'])
def radio_degree_nearest():
    """ Return in dictionary with all data for the light curve objects from api ztf or ps1 in a radio.
        ---
        parameters:
            - name: ra
              in: formData
              type: string 
              required: true
              default: 139.33444972

            - name: dec
              in: formData
              type: string 
              required: true
              default: 68.6350604

            - name: radius
              in : formData
              type: string
              required: true
              default: 0.0002777

            - name: format
              in: formData
              type: string
              enum: ['csv', 'votable']
              required: true
              default: csv

            - name: catalog
              in: formData
              type: string
              required: true
              enum: ['ztf', 'ps1','ztf,ps1']
              required: true
              default: 'ztf,ps1'

        responses:
            200:
                description: Dictionary with contein first value:key, with value is a catalog selected and value is
                                a dictionary with key:value when key is a id in respective catalog and key is information in
                                format request, in this case return only object if this exist in nearest radio selected.
                
               
                schema:
                    $ref: '#/definitions/dictionary'

    """
    format = request.form['format']

    if format not in {'csv','votable'}: 
        return "Record not found", status.HTTP_400_BAD_REQUEST 

@app.route('/radio-hours',methods=['POST'])
def radiohours():
    """ Return in dictionary with all data for the light curve objects from api ztf or ps1 in a radio.
        ---
        parameters: 
            - name: hours
              in: formData
              type: string 
              required: true
              default: 1h12m43.2s +1d12m43s

            - name: radius
              in : formData
              type: string
              required: true
              default: 0.0002777

            - name: format
              in: formData
              type: string
              enum: ['csv', 'votable']
              required: true
              default: csv

            - name: catalog
              in: formData
              type: string
              required: true
              enum: ['ztf', 'ps1','ztf,ps1']
              required: true
              default: 'ztf,ps1'

        responses:
            200:
                description: Dictionary with contein first value:key, with value is a catalog selected and value is
                                a dictionary with key:value when key is a id in respective catalog and key is information in
                                format request
                
               
                schema:
                    $ref: '#/definitions/dictionary'

    """
    print("?????????????????????????????????")
    format = request.form['format']

    if format not in {'csv','votable'}: 
        return "Record not found", status.HTTP_400_BAD_REQUEST 
    
    res = generic_request(request,False)    
    return make_response(res)


@app.route('/radio-hours-nearest',methods=['POST'])
def radiohoursnearest():
    """ Return dictionary of dictionaries with all data for the light curve object most nearest in radio from api ztf or ps1.
        ---
        parameters:
            - name: hours
              in: formData
              type: string 
              required: true
              default: 1h12m43.2s +1d12m43s

            - name: radius
              in : formData
              type: string
              required: true
              default: 0.0002777

            - name: format
              in: formData
              type: string
              enum: ['csv', 'votable']
              required: true
              default: csv

            - name: catalog
              in: formData
              type: string
              required: true
              enum: ['ztf', 'ps1','ztf,ps1']
              required: true
              default: 'ztf,ps1'

        responses:
            200:
                description: Dictionary with contein first value:key, with value is a catalog selected and value is
                                a dictionary with key:value when key is a id in respective catalog and key is information in
                                format request, in this case return only object if this exist in nearest radio selected.
                
               
                schema:
                    $ref: '#/definitions/dictionary'

    """
    format = request.form['format']

    if format not in {'csv','votable'}: 
        return "Record not found", status.HTTP_400_BAD_REQUEST 
    
    res = generic_request(request,True)    
    return make_response(res)