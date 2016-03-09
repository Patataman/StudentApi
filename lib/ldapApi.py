# -*- coding: utf-8 -*-

import ldap
import config

SCOPE = ldap.SCOPE_SUBTREE

class LdapApi:
    def __init__(self, uri, nia=None, password=None, port="389"):
        self.port = port
        self.ldapCon = ldap.initialize(uri + ":" +self.port)
        self.nia = nia
        self.password = password

    def search(self, dn, filt='(objectClass=*)', attrlist=None):
        result = self.ldapCon.search_s(dn,SCOPE,filt,attrlist)
        return result

    def auth(self):
        data = self.search(config.LDAP_DN, '(uid=*' + str(self.nia) + '*)', config.LDAP_FIELDS)
        data = data[0][0]
        try:
            self.ldapCon.simple_bind_s(data, self.password)
            return 0
    	except ldap.LDAPError as e:
			return 1
