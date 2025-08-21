docker build -t johnlenon003/api-processor:v3 . 

docker push johnlenon003/api-processor:v3  

oc apply -k infra/     