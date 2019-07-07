#!/bin/sh

# 获取指定项的值
function get_para()
{
    basepath=$(cd `dirname $0`; pwd)
    etcfile=$basepath/../etc/config
    val=`cat $etcfile|grep $1|tr -d [:space:]|awk -F= '{print $NF}'`
    echo $val
}

SYNC=/usr/bin/rsync
APPHOME=$(get_para "apphome")
#USER=root
RHOST=$(get_para "remotehost")
SRCD=$(get_para "localdir")
DESD=$(get_para "remotedir")
LOGFILE=$APPHOME/log/rsync/rsync-`date '+%Y%m%d_%H%M'`.log
$SYNC -avzP --progress --delete --log-file=$LOGFILE $SRCD $RHOST:$DESD

SRCB=$(get_para "localbinlog")
DESB=$(get_para "remotebinlog")
LOGFILEBIN=$APPHOME/log/rsync/rsync_binlog-`date '+%Y%m%d_%H%M'`.log
$SYNC -avzP --progress --delete --log-file=$LOGFILEBIN $SRCB $RHOST:$DESB