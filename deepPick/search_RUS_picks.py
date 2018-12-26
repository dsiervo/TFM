#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb


db = MySQLdb.connect(host="10.100.100.232",    # your host, usually localhost
                     user="consulta",         # your username
                     passwd="consulta",  # your password
                     db="seiscomp3")        # name of the data base
cur = db.cursor()

#cur.execute("show databases")

cur.execute("Select  \
 Pick.waveformID_stationCode,\
Pick.phaseHint_code,Pick.phaseHint_used,Pick.evaluationMode,Pick.time_value, Pick.time_value_ms\
 from Event AS EvMF left join PublicObject AS POEv ON EvMF._oid = POEv._oid \
left join PublicObject as POOri ON EvMF.preferredOriginID=POOri.publicID \
left join Origin ON POOri._oid=Origin._oid left join PublicObject as POMag on EvMF.preferredMagnitudeID=POMag.publicID \
left join Magnitude ON Magnitude._oid = POMag._oid \
left join Arrival on Arrival._parent_oid=Origin._oid \
left join PublicObject as POOri1 on POOri1.publicID = Arrival.pickID \
left join Pick on Pick._oid= POOri1._oid \
where \
(Pick.phaseHint_used = 1 AND Pick.evaluationMode = 'manual' AND Pick.waveformID_stationCode = 'RUS' AND Origin.latitude_value between -4 and 14 AND Origin.longitude_value between -82 AND -67 ) \
and Origin.time_value between '2018-03-10 00:00:00' and '2018-04-14 23:59:59'")
i=0
contenido1 = ''

for fila in cur.fetchall():
	contenido1 += str(fila)+'\n'
	i+=1 
	#print fila

archivo1=open('sc_report.out',"w")
archivo1.write(contenido1.decode('iso-8859-1').encode('UTF-8', 'strict'))

cur.close()
db.close()








