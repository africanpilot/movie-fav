Rancher desktop dev

kubectl
- kubectl apply -f deployment/tr-skeleton
- kubectl delete deployment jade-shooter
- kubectl delete service jade-shooter
- kubectl delete ingress jade-shooter

nerdctl build
- nerdctl build --namespace k8s.io -t $d ./microservices/.
- nerdctl build -t $d ./microservices/.


https://devops.stackexchange.com/questions/13379/use-one-helm-chart-for-all-microservices

1) create templete chart 
   ```bash
      helm create tr-app
   ```

2) render chart
```bash
    helm template test ./deployment/tr-app/
```

- use `helm lint ./deployment/tr-app/` to check files
- do a dry run of the chart
  ```bash
      helm install --dry-run --debug ./deployment/tr-app/ --generate-name
  ```
- deploy
  ```bash
    helm upgrade -i --timeout 20s skeleton ./deployment/tr-app/
  ```
 - delete
  ```bash
      helm delete skeleton
  ```