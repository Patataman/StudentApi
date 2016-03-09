# -*- coding: utf-8 -*-

from ldapApi import LdapApi
import config

class Student:
    """Represent a Student of University"""
    def __init__(self, uid=None, name=None, email=None):
        self.name = name
        self.uid = int(uid)
        self.email = email

def getStudent(cn):
    ldap = LdapApi(config.LDAP_URI)
    studentList = ldap.search(config.LDAP_DN, cn, config.LDAP_FIELDS)

    if len(studentList) == 1:
        name = studentList[0][1].get('cn')[0]
        student = Student(studentList[0][1].get('uid')[0], name.title(), studentList[0][1].get('uc3mCorreoAlias')[0])
        return [student]

    elif len(studentList) >1:
        students = []
        
        for studentValue in studentList:
            name = studentValue[1].get('cn')[0]
            student = Student(studentValue[1].get('uid')[0], name.title(), studentValue[1].get('uc3mCorreoAlias')[0])
            students.append(student)
        return students
