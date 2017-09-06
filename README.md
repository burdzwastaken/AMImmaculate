# AMImmaculate
AMImmaculate will remove unused, old images from *all* AWS regions. 

## deploy
* Install kappa  
```
pip install kappa
```
* Update the following values in `kappa.yml` to match your AWS account:
```
<your_env>
<your_profile>
<your_account_id>
```
* deploy using kappa  
```
kappa --env <your_env> deploy
```
