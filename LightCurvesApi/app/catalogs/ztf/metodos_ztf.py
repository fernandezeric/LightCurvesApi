import requests
import io

from astropy.io import ascii
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.io.votable import parse,parse_single_table,from_table, writeto


def id_nearest (ra,dec,radius,results):
    """ Get object id most closet to ra dec

    Parameters
    ----------
    ra
    dec
    radius
    results
    """
    angle = []
    c1 = SkyCoord(ra=ra,dec=dec,unit=u.degree)
    for group in results.groups:
        c2 = SkyCoord(group['ra'][0],group['dec'][0],unit=u.degree)
        angle.append(c1.separation(c2))
    return angle.index(min(angle))

def zftcurves(ra,dec,radius,format,nearest):
    """ Get light curves of ztf objects 

    Parameters
    ----------
    ra (float): (degrees) 
    dec (float): (degrees) 
    radius: (float): (degrees) 
    format: csv, votable
    nearest: Indicate if return the object most closest to point select with ra, dec.
    """
    baseurl="https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves"
    data = {}
    data['POS']=f'CIRCLE {ra} {dec} {radius}'
    #data['BANDNAME']='r'
    data['FORMAT'] = format
    result = requests.get(baseurl,params=data)
    ztfdic = {}

    if result.status_code != 200:
        ztfdic['0'] = 'not found' 
        return ztfdic #'not found'
    
    elif format == 'csv':
        #print(result.text)
        result = ascii.read(result.text)

        if len(result) <= 0:
            ztfdic['0'] = 'not found' 
            return ztfdic #'not found'

        results = result.group_by('oid')

        if nearest is True:

            minztf = id_nearest(ra,dec,radius,results)
            
            buf = io.StringIO()
            ascii.write(results.groups[minztf],buf,format='csv')
            ztfdic[str(results.groups[minztf]['oid'][0])] =  buf.getvalue()
            return ztfdic

        else:
            for group in results.groups:
                buf = io.StringIO()
                ascii.write(group,buf,format='csv')
                ztfdic[str(group['oid'][0])] =  buf.getvalue()
            return ztfdic

    else:
        votable = result.text.encode(encoding='UTF-8')
        bio = io.BytesIO(votable)
        votable = parse(bio)
        table = parse_single_table(bio).to_table()

        if len(table) <= 0:
            ztfdic['0'] = 'not found' 
            return ztfdic #'not found'

        tablas = table.group_by('oid')

        if nearest is True:
            
            minztf = id_nearest(ra,dec,radius,tablas)

            buf = io.BytesIO()
            votable = from_table(tablas.groups[minztf])
            writeto(votable,buf)
            ztfdic[str(tablas.groups[minztf]['oid'][0])] = (buf.getvalue().decode("utf-8"))
            return ztfdic
        else :
            for group in tablas.groups:
                buf = io.BytesIO()
                votable = from_table(group)
                writeto(votable,buf)
                ztfdic[str(group['oid'][0])] = (buf.getvalue().decode("utf-8"))
            return ztfdic
