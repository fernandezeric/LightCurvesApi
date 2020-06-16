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

    data = kw.copy()
    data['ra'] = ra
    data['dec'] = dec
    data['radius'] = radius
    return ps1search(table=table,release=release,format=format,columns=columns,
                    baseurl=baseurl, **data)

def ps1search(format,table="mean",release="dr1",columns=None,
           baseurl="https://catalogs.mast.stsci.edu/api/v0.1/panstarrs",
           **kw):
           
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

def addfilter(dtab):
    """Add filter name as column in detection table by translating filterID
    
    This modifies the table in place.  If the 'filter' column already exists,
    the table is returned unchanged.
    """
    if 'filter' not in dtab.colnames:
        # the filterID value goes from 1 to 5 for grizy
        id2filter = np.array(list('grizy'))
        dtab['filter'] = id2filter[(dtab['filterID']-1).data]
        #print("FILTROOO")
    return dtab

def ps1ids(ra,dec,radius,nearest):
    constraints = {'nDetections.gt':1}
    columns = ['objID','raMean','decMean']
    results = ps1cone(ra,dec,radius,release='dr2',columns=columns,**constraints)
    results = ascii.read(results)

    if len(results) <= 0:
        return -1

    elif nearest is True:
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

    ids = ps1ids(ra,dec,radius,nearest)
    ps1dic = {}
    #print(ids)
    if id == -1 :
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
            #print(buf.getvalue())
            ps1dic[str(id)] =  buf.getvalue()
        else :
            ps1dic[str(id)] = dresults
    #print(ps1dic)
    return ps1dic

