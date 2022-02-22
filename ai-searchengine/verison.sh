#!/bin/bash
# bash verison.sh prod/nginx-test-deployment.yaml "bug"

dr=$PWD
echo "${dr}"
cd /root/kubernetes && git reset --hard && git pull
cd $dr

version=$(grep 'image:' $1); version=${version//*image: /}; echo "$version"
major=0
minor=0
build=0

# break down the version number into it's components
regex="(.*-v)([0-9]+).([0-9]+).([0-9]+)"
if [[ $version =~ $regex ]]; then
  appname="${BASH_REMATCH[1]}" 
  major="${BASH_REMATCH[2]}"
  minor="${BASH_REMATCH[3]}"
  build="${BASH_REMATCH[4]}"
fi

# check paramater to see which number to increment
if [[ "$2" == "feature" ]]; then
  minor=$(echo $minor + 1 | bc)
elif [[ "$2" == "bug" ]]; then
  build=$(echo $build + 1 | bc)
elif [[ "$2" == "major" ]]; then
  major=$(echo $major+1 | bc)
else
  echo "usage: ./version.sh version_number [major/feature/bug]"
  exit -1
fi

# echo the new version number
value="${appname}${major}.${minor}.${build}"
echo "${value}"
docker build -t ${value} .
docker push ${value}

sed -ri 's/^(\s*)(image\s*:\s*.*\s*$)/\1image: '$(echo "${value}" | sed -e 's/\//\\\//g')'/' $1

cd /root/kubernetes && git add . -A
cd /root/kubernetes && git commit -m "${value}"
cd /root/kubernetes && git push origin main
