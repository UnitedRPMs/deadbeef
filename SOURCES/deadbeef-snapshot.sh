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
git clone -b ${tag_name} --depth 1 https://github.com/Alexey-Yakovenko/${package}.git
cd ${package}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=`echo ${tag_name} | tr -d 'v'`
cd ${tmp}
tar Jcf "$pwd"/${name}-${version}-${date}-${tag}.tar.xz ${package}
