#!/usr/bin/env bash
WORK_DIR=/tmp/cloudalbum_dist
CWD=`pwd`
ZIP_FOR_EB=cloudalbum_v1.0.zip
ZIP_FOR_EB_V2=cloudalbum_without_rds_efs_v1.0.zip
ZIP_FOR_LAB=cloudalbum-mts-dist-src.zip
ZIP_FOR_QL=cloudalbum-mts-dist-src-QL.zip
echo "-----------------------------------------------------------"
rm -rf ${WORK_DIR}/* 2> /dev/null

# Copy frontend
mkdir -p ${WORK_DIR}/cloudalbum-mts-dist-src/frontend/cloudalbum
rsync -q -av --progress ./LAB01/frontend/cloudalbum ${WORK_DIR}/cloudalbum-mts-dist-src/frontend/ --exclude node_modules --exclude dist

# Copy LAB01/backend
mkdir -p ${WORK_DIR}/cloudalbum-mts-dist-src/LAB01/backend
cp -r ./LAB01/backend/ ${WORK_DIR}/cloudalbum-mts-dist-src/LAB01/backend/

# Copy LAB01/backend for LAB02/backend
mkdir -p ${WORK_DIR}/cloudalbum-mts-dist-src/LAB02/backend
# Copy backend application of LAB01/backend
cp -r ./LAB01/backend/ ${WORK_DIR}/cloudalbum-mts-dist-src/LAB02/backend/
# Copy .ebextentions and wsgi.py for LAB02
cp -r ./LAB02/backend/ ${WORK_DIR}/cloudalbum-mts-dist-src/LAB02/backend/

# Copy LAB03/backend
mkdir -p ${WORK_DIR}/cloudalbum-mts-dist-src/LAB03/
cp -r ./LAB03/ ${WORK_DIR}/cloudalbum-mts-dist-src/LAB03/

# Copy LAB04/backend
mkdir -p ${WORK_DIR}/cloudalbum-mts-dist-src/LAB04/
cp -r ./LAB04/ ${WORK_DIR}/cloudalbum-mts-dist-src/LAB04/
rm -r ${WORK_DIR}/cloudalbum-mts-dist-src/LAB04/02-CloudAlbum-Chalice/cloudalbum/.chalice/deployed
rm -r ${WORK_DIR}/cloudalbum-mts-dist-src/LAB04/02-CloudAlbum-Chalice/cloudalbum/.chalice/deployments

# Remove temporary files.
find ${WORK_DIR} -name ".pytest_cache" -exec rm -rf {} \; 2>/dev/null
find ${WORK_DIR} -name "__pycache__" -exec rm -rf {} \; 2>/dev/null
find ${WORK_DIR} -name ".DS_Store" -exec rm -rf {} \; 2>/dev/null

# Make a zip file for hands-on lab
cd ${WORK_DIR} && zip -r ${WORK_DIR}/${ZIP_FOR_LAB} *
cp ${WORK_DIR}/${ZIP_FOR_LAB} ${CWD}/resources/${ZIP_FOR_LAB}

# Make a zip file for hands-on lab(QL)
cp ${CWD}/resources/config_for_qwiklab.json ${WORK_DIR}/cloudalbum-mts-dist-src/LAB04/02-CloudAlbum-Chalice/cloudalbum/.chalice/config.json
cd ${WORK_DIR} && zip -r ${WORK_DIR}/${ZIP_FOR_QL} *
cp ${WORK_DIR}/${ZIP_FOR_QL} ${CWD}/resources/${ZIP_FOR_QL}

# Make a zip file for ElasticBeanstalk deploy
cd ${WORK_DIR}/cloudalbum-mts-dist-src/LAB02/backend/ && zip -r ${WORK_DIR}/${ZIP_FOR_EB} *
cp ${WORK_DIR}/${ZIP_FOR_EB} ${CWD}/resources/${ZIP_FOR_EB}

# Make a zip file for ElasticBeanstalk depoly (DDB, S3, Cognito, X-Ray)
cd ${WORK_DIR}/cloudalbum-mts-dist-src/LAB03/04-Xray/backend/ && zip -r ${WORK_DIR}/${ZIP_FOR_EB_V2} *
cp ${WORK_DIR}/${ZIP_FOR_EB_V2} ${CWD}/resources/${ZIP_FOR_EB_V2}

echo "-----------------------------------------------------------"
echo "Now, updated : resources/${ZIP_FOR_LAB}"
echo "Now, updated : resources/${ZIP_FOR_QL}"
echo "Now, updated : resources/${ZIP_FOR_EB}"
echo "Now, updated : resources/${ZIP_FOR_EB_V2}"
