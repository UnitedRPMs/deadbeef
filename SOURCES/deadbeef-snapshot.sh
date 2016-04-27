#!/bin/bash

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
git clone --depth 1 https://github.com/Alexey-Yakovenko/${package}.git
cd ${package}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=$(cat ChangeLog | grep 'version [0-9]' | awk -F 'version' '{print $2}' | sort | tail -1 | sed 's|^ *||g')
cd ${tmp}
tar Jcf "$pwd"/${name}-${version}-${date}-${tag}.tar.xz ${package}
