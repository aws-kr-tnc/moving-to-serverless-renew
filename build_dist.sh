#!/usr/bin/env bash
WORK_DIR=/tmp/cloudalbum_dist
CWD=`pwd`
echo "building.. './resources/cloudalbum-mts-dist-src.zip' file. "
echo "-----------------------------------------------------------"
mkdir -p ${WORK_DIR}/cloudalbum-mts-dist-src/cloudalbum-mts-dist-src/frontend/cloudalbum
rsync -q -av --progress ./LAB01/frontend/cloudalbum ${WORK_DIR}/cloudalbum-mts-dist-src/frontend/ --exclude node_modules --exclude dist
mkdir -p ${WORK_DIR}/cloudalbum-mts-dist-src/LAB01/backend
cp -r ./LAB01/backend/ ${WORK_DIR}/cloudalbum-mts-dist-src/LAB01/
mkdir -p ${WORK_DIR}/cloudalbum-mts-dist-src/LAB02/backend
cp -r ./LAB01/backend/ ${WORK_DIR}/cloudalbum-mts-dist-src/LAB02/
mkdir -p ${WORK_DIR}/cloudalbum-mts-dist-src/LAB03/
cp -r ./LAB03/ ${WORK_DIR}/cloudalbum-mts-dist-src/LAB03/
mkdir -p ${WORK_DIR}/cloudalbum-mts-dist-src/LAB04/
cp -r ./LAB04/ ${WORK_DIR}/cloudalbum-mts-dist-src/LAB04/
# Remove temporary files.
find ${WORK_DIR} -name ".pytest_cache" -exec rm -rf {} \; 2>/dev/null
find ${WORK_DIR} -name "__pycache__" -exec rm -rf {} \; 2>/dev/null
# Make a zip file
cd ${WORK_DIR} && zip -r ${CWD}/resources/cloudalbum-mts-dist-src.zip *
echo "-----------------------------------------------------------"
echo "Now, updated : resources/cloudalbum-mts-dist-src.zip"
