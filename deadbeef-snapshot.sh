#!/bin/bash

tag_name=0.7.2

set -x

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
date=$(date +%Y%m%d)
package=deadbeef
name=deadbeef

pushd ${tmp}
git clone https://github.com/Alexey-Yakovenko/${package}.git
cd ${package}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=`echo ${tag_name} | tr -d 'v'`
cd ${tmp}
tar Jcf "$pwd"/${name}-${version}-${date}-${tag}.tar.xz ${package}

popd
upload_source=$( curl --upload-file ${name}-${version}-${date}-${tag}.tar.xz https://transfer.sh/${name}-${version}-${date}-${tag}.tar.xz )

if [ -n "$upload_source" ]; then
GCOM=$( sed -n '/Source0:/=' ${name}.spec)
sed -i "${GCOM}s#.*#Source0:	${upload_source}#" ${name}.spec
fi
