#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb


db = MySQLdb.connect(host="10.100.100.232",    # your host, usually localhost
                     user="consulta",         # your username
                     passwd="consulta",  # your password
                     db="seiscomp3")        # name of the data base
cur = db.cursor()

#cur.execute("show databases")

cur.execute("\
		SELECT \
			DATE_FORMAT(Origin.time_value, '%Y/%m/%d') AS 'FECHA', \
			DATE_FORMAT(Origin.time_value, '%H:%i:%S') AS 'HORA UTC', \
			ROUND(Magnitude.magnitude_value,1) AS 'Magnitud', \
			Magnitude.type AS 'Tipo Magnitud', \
			Origin.quality_usedPhaseCount AS 'Numero Fases Usadas', \
			ROUND(Origin.latitude_value,2) AS 'Latitud', \
			ROUND(Origin.latitude_uncertainty,2) AS 'Error_Latitud', \
			ROUND(Origin.longitude_value,2) AS 'Longitud', \
			ROUND(Origin.longitude_uncertainty,2) AS 'Error_Longitud', \
			ROUND(Origin.depth_value) AS 'Profundidad', \
			ROUND(Origin.depth_uncertainty,2) AS 'Error_Profundidad', \
			ROUND(Origin.quality_standardError,2) AS 'RMS', \
			Origin.evaluationMode AS 'Estatus', \
			Origin.creationInfo_agencyID AS 'Agencia', \
			Origin.creationInfo_author AS 'Author', \
			PEvent.publicID AS 'ID', \
			DATE_FORMAT(Origin._last_modified, '%Y/%m/%d %H:%i:%S') AS 'MODIF', \
			EventDescription.text AS 'Region' \
		FROM \
			Event, PublicObject AS PEvent, EventDescription, FeltReport, Origin, PublicObject AS POrigin, Magnitude, PublicObject AS PMagnitude \
		WHERE \
			Origin._oid=POrigin._oid \
			AND Event._oid=PEvent._oid \
			AND Magnitude._oid=PMagnitude._oid \
			/*AND POrigin.publicID = OriginReference.originID */\
			/*AND OriginReference._parent_oid = Event._oid */\
			/*AND Magnitude._parent_oid = Origin._oid */\
			AND Event.preferredOriginID=POrigin.publicID \
			AND Event.preferredMagnitudeID=PMagnitude.publicID \
			AND Event._oid=EventDescription._parent_oid \
			AND Event._oid = FeltReport._oid \
			AND FeltReport.report NOT LIKE '' \
			AND Origin.time_value BETWEEN '20180301000000' AND '20180401000000'\
			/*AND ROUND(Origin.latitude_value,2) BETWEEN 7.0 AND 8.0 */\
			/*AND ROUND(Origin.longitude_value,2) BETWEEN -82.0 AND -81.0 */\
			/*AND Origin.depth_value BETWEEN 0 AND 10 */\
			AND ROUND(Magnitude.magnitude_value,1) BETWEEN 0.0 AND 10.0 \
			/*AND Origin.quality_usedPhaseCount BETWEEN 1 AND 20 */\
			/*AND Origin.quality_usedStationCount BETWEEN 1 AND 20 */\
			/*AND ROUND(Origin.latitude_uncertainty,2) BETWEEN 0.00 AND 20.00 */\
			/*AND ROUND(Origin.longitude_uncertainty,2) BETWEEN 0.00 AND 20.00 */\
			/*AND ROUND(Origin.depth_uncertainty,2) BETWEEN 0.00 AND 20.00 */\
			/*AND ROUND(Origin.quality_standardError,2) BETWEEN 0.00 AND 3.00 */\
			/*AND ROUND(Origin.quality_azimuthalGap,2) BETWEEN 0.00 AND 360.00 */\
			/*AND ROUND(Origin.quality_minimumDistance,2) BETWEEN 0.00 AND 10.00 */\
			/*AND Magnitude.type='MLv' */\
			/*AND Origin.evaluationMode='automatic' */\
			/*AND Origin.creationInfo_agencyID='SGC' */\
			/*AND Origin.creationInfo_author='scanloc' */\
			AND (Event.type NOT IN ('not locatable', 'explosion', 'not existing', 'outside of network interest') OR Event.type IS NULL)\
			AND EventDescription.type = 'region name' AND (EventDescription.text LIKE '%Pacífico%' OR EventDescription.text LIKE '%Colombia%' OR EventDescription.text LIKE '%Caribe%' OR EventDescription.text LIKE '%Volcán%')\
			ORDER BY Origin.time_value")
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


#SERVIDOR,232
#BUSQUEDA,Eventos
#TIME_INI,20180301000000
#TIME_END,20180401000000
#LAT_MIN,
#LAT_MAX,
#LON_MIN,
#LON_MAX,
#DEP_MIN,
#DEP_MAX,
#MAG_MIN,0.0
#MAG_MAX,10.0
#PHASE_MIN,
#PHASE_MAX,
#STA_MIN,
#STA_MAX,
#LAT_ERROR_MIN,
#LAT_ERROR_MAX,
#LON_ERROR_MIN,
#LON_ERROR_MAX,
#DEP_ERROR_MIN,
#DEP_ERROR_MAX,
#RMS_MIN,
#RMS_MAX,
#GAP_MIN,
#GAP_MAX,
#DIST_STA_MIN,
#DIST_STA_MAX,
#MAG_TYPE,
#ESTATUS,
#AGENCIA,
#AUTOR,
#TIPO,
#REGION,Boletin







