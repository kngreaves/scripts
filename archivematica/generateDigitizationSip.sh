#!/usr/bin/env bash

# input refid
read -p "Enter the ArchivesSpace refid: " refid

#  create directory and subdirectories
# set top level directory (directly below home)
topDirectory='archivematica_test'

# move to home directory
cd ~

# make Archivematica transfer directory and subdirectories
mkdir ${topDirectory}/archivematica_sip_${refid}
targetDirectory="${topDirectory}/archivematica_sip_${refid}"
mkdir ${targetDirectory}/logs ${targetDirectory}/metadata
mkdir -p ${targetDirectory}/objects/access
# mkdir ${targetDirectory}/objects/service

# find master files and copy master files to objects folder
array=(`ls ${topDirectory}/byRefId/${refid}/master`)
for i in ${array[@]}
do
	echo ${topDirectory}/byRefId/${refid}/master/$i
	cp ${topDirectory}/byRefId/${refid}/master/$i ${targetDirectory}/objects
done
rm ${targetDirectory}/objects/${refid}_001.tif

# find service edited files and copy service edited files to /access folder (and objects folder if concatenated file)
array=(`ls ${topDirectory}/byRefId/${refid}/service_edited`)
if [[ " ${array[*]} " == *".jpg"* ]]; then
    echo "access copies are jpgs"
	for i in ${array[@]}
	do
		echo $i
		cp ${topDirectory}/byRefId/${refid}/service_edited/$i ${targetDirectory}/objects/access/${i/_se/}
		# check that access directory is not empty
	done
	rm ${targetDirectory}/objects/access/${refid}_001.jpg
fi
if [[ " ${array[*]} " == *".pdf"* ]]; then
    echo "access copies are pdfs"
	for i in ${array[@]}
	do
		echo $i
		cp ${topDirectory}/byRefId/${refid}/service_edited/$i ${targetDirectory}/objects/access/${i/_se/}
		cp ${topDirectory}/byRefId/${refid}/service_edited/$i ${targetDirectory}/objects/${i/_se/}
		# check number of files in access directory equal number of files in objects directory
	done
	pdftk ${targetDirectory}/objects/access/${refid}.pdf cat 2-end output ${targetDirectory}/objects/access/${refid}_trimmed.pdf
	mv ${targetDirectory}/objects/access/${refid}_trimmed.pdf ${targetDirectory}/objects/access/${refid}.pdf
	pdftk ${targetDirectory}/objects/${refid}.pdf cat 2-end output ${targetDirectory}/objects/${refid}_trimmed.pdf
	mv ${targetDirectory}/objects/${refid}_trimmed.pdf ${targetDirectory}/objects/${refid}.pdf
fi

# find master edited files and copy master edited files to /service folder
# array=(`ls ${topDirectory}/byRefId/${refid}/master_edited`)
# for i in ${array[@]}
# do
# 	echo $i
# 	cp ${topDirectory}/byRefId/${refid}/master_edited/$i ${targetDirectory}/objects/service/${i/_me/}
# 	# check number of files in service directory equal number of files in objects directory
# done

rm ${targetDirectory}/objects/*mbs.db
master_filelist_count=(`ls ${targetDirectory}/objects/ | wc -l`)
echo "There are ${master_filelist_count} files and directories in the /objects directory"

# rm ${targetDirectory}/objects/service/Thumbs.db
# service_filelist_count=(`ls ${targetDirectory}/objects/service/ | wc -l`)
# echo "There are ${service_filelist_count} files and directories in the /objects/service directory"

rm ${targetDirectory}/objects/access/*mbs.db
access_filelist_count=(`ls ${targetDirectory}/objects/access/ | wc -l`)
echo "There are ${access_filelist_count} files and directories in the /objects/access directory"