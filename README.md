# AMImmaculate
AMImmaculate will remove unused, old images from *all* AWS regions. 

## deploy
* Install kappa  
```
pip install kappa
```
* Update the values in `kappa.yml` to match your AWS account  
* deploy using kappa  
```
kappa --env your_env deploy
```
