from flask import request,send_file,jsonify, make_response,abort
from flasgger import Swagger
from astropy.coordinates import SkyCoord
from app.catalogs.ps1 import metodos_ps1 as mps1
from app.catalogs.ztf import metodos_ztf as mztf
from app import app


app.config['SWAGGER'] = {
    'title': 'LC API',
    'version': 0.3,
    'uiversion': 3,
    'schemes': ['https','http'],
    'description' : 'Lc API(beta name) es una api que tiene la finalidad de proporcionar la informacion de las curvas \
                      de luz de objetos pertenecientes a diferentes api\'s, actualmente facilita la obtencion de \
                        las apis de pan-starss (ps1) y ztf.'
}

swagger = Swagger(app)


def generic_request(request,nearest=False): 
    # print("******",request,"******")

    #if request is 'hms-degree' and not 'ra,dec'
    if "hms" in request.form:
        coord = SkyCoord(request.form['hms'],frame='icrs') #transform coord
        ra = coord.ra.degree
        dec = coord.dec.degree

    #if request is 'ra,dec'
    else:
        ra = request.form['ra']
        dec = request.form['dec']

    radius = request.form['radius']
    catalog = request.form['catalog']
    format = request.form['format']

    #create empty dictionary
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

def cheack_format(format):
  if format in {'csv','votable','json'}: 
    return True
  else: 
    return False

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route('/')
def hello_world():
    """ Example for swagger, this rute return a sweet message
        to ChikiMan.
        ---
        tags:
          - home
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
    """ Retorna todos los datos de curva de luz perteneciente a los objetos encontrados en el radio indicado, bajo
        la busqueda por ra,dec.
        ---

        tags:
          - degree
        parameters:
            - name: ra
              in: formData
              type: number 
              required: true
              default: 139.33444972

            - name: dec
              in: formData
              type: number 
              required: true
              default: 68.6350604

            - name: radius
              in : formData
              type: number
              required: true
              default: 0.0002777

            - name: format
              in: formData
              type: string
              enum: ['csv', 'votable','json']
              required: true
              description : Seleccionar formato de entrega 
              default: csv

            - name: catalog
              in: formData
              type: string
              required: true
              enum: ['ztf', 'ps1','ztf,ps1']
              required: true
              description : Seleccionar catalogos a consultar
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
                description: Retorna un diccionario que en su interior contiene un diccionario por cada catalogo consultado, dentro de estos
                              ultimos diccionarios corresponderan a la combinacion clave:valor - > id_objeto : datos_curva_de_luz, el formato del valor
                              (datos de la curva), corresponde al indicado en 'format'.
                
                schema:
                    $ref: '#/definitions/dictionary'

    """   
    if not cheack_format(request.form['format']):
        abort(404, description="Format not found")
        return jsonify(resource)

    res = generic_request(request,False)    
    return make_response(res)

@app.route('/radio-degree-nearest',methods=['POST'])
def radio_degree_nearest():
    """ Retorna todos los datos de curva de luz perteneciente a el objeto mas cercano encontrado en el radio indicado, bajo
        la busqueda por ra,dec.
        ---

        tags:
          - degree
        parameters:
            - name: ra
              in: formData
              type: number 
              required: true
              default: 139.33444972

            - name: dec
              in: formData
              type: number 
              required: true
              default: 68.6350604

            - name: radius
              in : formData
              type: number
              required: true
              default: 0.0002777

            - name: format
              in: formData
              type: string
              enum: ['csv', 'votable','json']
              required: true
              description : poner descripcion
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
                description: Retorna un diccionario que en su interior contiene un diccionario por cada catalogo consultado, dentro de estos
                              ultimos diccionarios corresponderan a la combinacion clave:valor - > id_objeto : datos_curva_de_luz, el formato del valor
                              (datos de la curva), corresponde al indicado en 'format'. En caso de existir devuelve unicamente el objeto mas cercano a ra,dec
                              seleccionado por cada catalogo.
                
               
                schema:
                    $ref: '#/definitions/dictionary'

    """
    if not cheack_format(request.form['format']):
        abort(404, description="Format not found")
        return jsonify(resource)
    
    res = generic_request(request,True)    
    return make_response(res)

@app.route('/radio-hms',methods=['POST'])
def radiohms():
    """ Retorna todos los datos de curva de luz perteneciente a los objetos encontrados en el radio indicado, bajo
        la busqueda por formato hms.
        ---

        tags:
          - hms
        parameters: 
            - name: hms
              in: formData
              type: string 
              required: true
              default: 1h12m43.2s +1d12m43s
              description: Transform hms to ra,dec form with skycoord and set frame in 'icrs'

            - name: radius
              in : formData
              type: number
              required: true
              default: 0.0002777

            - name: format
              in: formData
              type: string
              enum: ['csv', 'votable','json']
              required: true
              description : 
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
                description: Retorna un diccionario (json), que en su interior contiene un diccionario por cada catalogo consultado, dentro de estos
                              ultimos diccionarios corresponderan a la combinacion clave:valor - > id_objeto : datos_curva_de_luz, el formato del valor
                              (datos de la curva), corresponde al indicado en 'format'.
                
               
                schema:
                    $ref: '#/definitions/dictionary'

    """
    if not cheack_format(request.form['format']):
        abort(404, description="Format not found")
        return jsonify(resource)
    
    res = generic_request(request,False)    
    return make_response(res)


@app.route('/radio-hms-nearest',methods=['POST'])
def radiohmsnearest():
    """ Retorna todos los datos de curva de luz perteneciente a el objeto mas cercano encontrado en el radio indicado, bajo
        la busqueda por hms.
        ---

        tags:
          - hms
        parameters:
            - name: hms
              in: formData
              type: string 
              required: true
              default: 1h12m43.2s +1d12m43s
              description: Transform hms to ra,dec form with skycoord and set frame in 'icrs'

            - name: radius
              in : formData
              type: number
              required: true
              default: 0.0002777

            - name: format
              in: formData
              type: string
              enum: ['csv', 'votable','json']
              required: true
              description : poner descripcion
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
                description: Retorna un diccionario que en su interior contiene un diccionario por cada catalogo consultado, dentro de estos
                              ultimos diccionarios corresponderan a la combinacion clave:valor - > id_objeto : datos_curva_de_luz, el formato del valor
                              (datos de la curva), corresponde al indicado en 'format'. En caso de existir devuelve unicamente el objeto mas cercano a ra,dec
                              seleccionado por cada catalogo.
                
               
                schema:
                    $ref: '#/definitions/dictionary'

    """
    if not cheack_format(request.form['format']):
        abort(404, description="Format not found")
        return jsonify(resource)
    
    res = generic_request(request,True)    
    return make_response(res)