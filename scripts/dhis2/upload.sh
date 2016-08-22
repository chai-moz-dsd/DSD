password=$1

echo "push dhis2 image to the repo"
docker login -u="chaimozdsd" -p=${password}
docker push chaimozdsd/dhis2