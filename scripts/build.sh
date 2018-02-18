#!/bin/bash
set -e

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

SRC_DIR=${DIR}/..
WHL_DIR=build/wheelhouse
OUTPUT=dist/onelogin-aws-login

cd $SRC_DIR

pip wheel . -w $WHL_DIR

pex --no-pypi -f $WHL_DIR onelogin_aws_cli -e onelogin_aws_cli.main:main -o $OUTPUT --disable-cache --platform linux_x86_64 --platform linux_i686 --platform macosx_10_11_x86_64
echo "Created ${OUTPUT}"
