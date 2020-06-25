import requests
import io

from astropy.io import ascii
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy import units as u

#https://ps1images.stsci.edu/ps1_dr2_api.html
def ps1cone(ra,dec,radius,table="mean",release="dr1",format="csv",columns=None,
           baseurl="https://catalogs.mast.stsci.edu/api/v0.1/panstarrs",
           **kw):
    """Do a cone search of the PS1 catalog

    Parameters
    ----------
    ra (float): (degrees) J2000 Right Ascension
    dec (float): (degrees) J2000 Declination
    radius (float): (degrees) Search radius (<= 0.5 degrees)
    table (string): mean, stack, or detection 
    release (string): dr1 or dr2 
    format: csv, votable, json
    columns: list of column names to include (None means use defaults)
    baseurl: base URL for the request
    verbose: print info about request
    **kw: other parameters (e.g., 'nDetections.min':2)
    """
    data = kw.copy()
    data['ra'] = ra
    data['dec'] = dec
    data['radius'] = radius
    return ps1search(table=table,release=release,format=format,columns=columns,
                    baseurl=baseurl, **data)

#https://ps1images.stsci.edu/ps1_dr2_api.html
def ps1search(format,table="mean",release="dr1",columns=None,
           baseurl="https://catalogs.mast.stsci.edu/api/v0.1/panstarrs",
           **kw):
    """Do a general search of the PS1 catalog (possibly without ra/dec/radius)
    
    Parameters
    ----------
    table (string): mean, stack, or detection
    release (string): dr1 or dr2
    format: csv, votable, json
    columns: list of column names to include (None means use defaults)
    baseurl: base URL for the request
    verbose: print info about request
    **kw: other parameters (e.g., 'nDetections.min':2).  Note this is required!
    """
    data = kw.copy()
    url = f"{baseurl}/{release}/{table}.{format}"
    data['columns'] = '[{}]'.format(','.join(columns))
    # either get or post works
    r = requests.get(url, params=data)
    r.raise_for_status()
    if format == "json":
        return r.json()
    else:
        return r.text

def ps1ids(ra,dec,radius,nearest):
    """Get ids (ps1 id) of objects in a radius with respect to ra and dec

    Parameters
    ----------
    ra (float): (degrees) J2000 Right Ascension
    dec (float): (degrees) J2000 Declination
    radius (float): (degrees) Search radius (<= 0.5 degrees)
    nearest (boolean): Indicate if return the id object most closest to point select with ra, dec.
    """
    constraints = {'nDetections.gt':1}
    columns = ['objID','raMean','decMean']
    results = ps1cone(ra,dec,radius,release='dr2',columns=columns,**constraints)

    if len(results) <= 0:
        return -1
    results = ascii.read(results)


    if nearest is True:
        #poner en otro lado, mas general
        angle = []
        c1 = SkyCoord(ra=ra,dec=dec,unit=u.degree)
        for re in results:
            c2 = SkyCoord(ra=re['raMean'],dec=re['decMean'],unit=u.degree)
            angle.append(c1.separation(c2))
        minps1 = angle.index(min(angle))
        #por mientras
        temp = []
        temp.append(results[minps1]['objID'])
        return temp

    else :
        return results['objID']


def ps1curves(ra,dec,radius,format,nearest):
    """Get light curves of objects in specific radio with respect ra and dec, and possible return the object most nearest to radio


    Parameters
    ----------
    ra (float): (degrees) J2000 Right Ascension
    dec (float): (degrees) J2000 Declination
    radius (float): (degrees) Search radius (<= 0.5 degrees)
    format: csv, votable
    nearest: Indicate if return the object most closest to point select with ra, dec.
    """
    ids = ps1ids(ra,dec,radius,nearest)
    ps1dic = {}
    if ids == -1 :
        ps1dic['0'] = 'not found'
        return ps1dic

    for id in ids:
        dconstraints = {'objID': id}
        dcolumns = ("""objID,detectID,filterID,obsTime,ra,dec,psfFlux,psfFluxErr,psfMajorFWHM,psfMinorFWHM,
                    psfQfPerfect,apFlux,apFluxErr,infoFlag,infoFlag2,infoFlag3""").split(',')
        dcolumns = [x.strip() for x in dcolumns]
        dcolumns = [x for x in dcolumns if x and not x.startswith('#')]
        dresults = ps1search(format,table='detection',release='dr2',columns=dcolumns,**dconstraints)
        if(format == 'csv'):
            dresults = ascii.read(dresults)
            buf = io.StringIO()
            ascii.write(dresults,buf,format='csv')
            ps1dic[str(id)] =  buf.getvalue()
        else :
            ps1dic[str(id)] = dresults
    return ps1dic

