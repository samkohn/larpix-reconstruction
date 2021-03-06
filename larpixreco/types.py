import numpy as np

class Hit(object):
    ''' The basic primitive type used in larpix-reconstruction represents a single trigger of a larpix channel '''

    def __init__(self, hid, px, py, ts, q, iochain=None, chipid=None, channelid=None, geom=None):
        self.hid = hid
        self.px = px
        self.py = py
        self.ts = ts
        self.q = q
        self.iochain = iochain
        self.chipid = chipid
        self.channelid = channelid
        self.geom = geom

    def __str__(self):
        string = 'Hit(hid={hid}, px={px}, py={py}, ts={ts}, q={q}, iochain={iochain}, '\
            'chipid={chipid}, channelid={channelid}, geom={geom})'.format(**vars(self))
        return string

class HitCollection(object):
    ''' A base class of collected `Hit` types '''
    def __init__(self, hits):
        self.hits = hits
        self.nhit = len(self.hits)
        self.ts_start = min(self.get_hit_attr('ts'))
        self.ts_end = max(self.get_hit_attr('ts'))
        self.q = sum(self.get_hit_attr('q'))

    def __str__(self):
        string = '{}(hits=[\n\t{}]\n\t)'.format(self.__class__.__name__, \
            ', \n\t'.join(str(hit) for hit in self.hits))
        return string

    def __getitem__(self, key):
        '''
        Access to hits or hit attr.
        If key is an int -> returns hit at that index
        If key in a str -> returns attr value of all hits specified by key
        If key is a dict -> returns hits with attr values that match dict
        If key is a list or tuple -> returns hits at indices
        E.g.
        hc = HitCollection(hits=[Hit(0,0,0,0), Hit(1,0,0,0), Hit(1,1,0,0)])
        hc[0] # Hit(0,0,0,0)
        hc['px'] # [0,1,1]
        hc[{'px' : 1}] # [Hit(1,0,0,0), Hit(1,1,0,0)]
        hc[0,1] # [Hit(0,0,0,0), Hit(1,0,0,0)]
        '''
        if isinstance(key, int):
            return self.hits[key]
        elif isinstance(key, str):
            return self.get_hit_attr(key)
        elif isinstance(key, dict):
            return self.get_hit_match(key)
        elif isinstance(key, list) or isinstance(key, tuple):
            return [self.hits[idx] for idx in key]

    def __len__(self):
        return nhit

    def get_hit_attr(self, attr, default=None):
        ''' Get a list of the specified attribute from event hits '''
        if not default is None:
            return [getattr(hit, attr, default) for hit in self.hits]
        else:
            return [getattr(hit, attr) for hit in self.hits]

    def get_hit_match(self, attr_value_dict):
        '''
        Returns a list of hits that match the attr_value_dict 
        attr_value_dict = { <hit attribute> : <value of attr>, ...}
        '''
        return_list = []
        for hit in self.hits:
            if all([getattr(hit, attr) == value for attr, value in \
                        attr_value_dict.items()]):
                return_list += [hit]
        return return_list

class Event(HitCollection):
    '''
    A class for a collection of hits associated by the event builder, contains
    reconstructed objects
    '''
    def __init__(self, evid, hits, reco_objs=None):
        HitCollection.__init__(self, hits)
        self.evid = evid
        if reco_objs is None:
            self.reco_objs = []
        else:
            self.reco_objs = reco_objs

    def __str__(self):
        string = HitCollection.__str__(self)[:-1]
        string += ', evid={evid}, reco_objs={reco_objs})'.format(\
            **vars(self))
        return string

class Track(HitCollection):
    '''
    A class representing a reconstructed straight line segment and associated
    hits
    '''
    def __init__(self, hits, theta, phi, xp, yp, cov=None, start=None, end=None):
        HitCollection.__init__(self, hits)
        self.theta = theta
        self.phi = phi
        self.xp = xp
        self.yp = yp
        self.cov = cov
        self.start = start
        self.end = end
        self.length = np.linalg.norm(start - end)

class Shower(HitCollection):
    ''' A class representing a shower '''
    pass
# etc
