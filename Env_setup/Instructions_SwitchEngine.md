1. Create Ubuntu 18.04 machine on switch engine
2. login using ubuntu@ipaddress
3. curl -O https://raw.githubusercontent.com/guiwitz/Python_image_processing/master/Env_setup/switch_engine_install.bsh
4. Check address using host XX.XXX.XXX.XX and copy it
5. vim switch_engine_install.bsh
6. Replace the address yourhub.xxx.com with the address copied in 5.
7. chmod u+x switch_engine_install.bsh
8. /switch_engine_install.bsh
9. Create an nbgitpuller link on this model by replacing the jupyterhub address: https://fl-6-195.zhdk.cloud.switch.ch/hub/user-redirect/git-pull?repo=https://github.com/guiwitz/Python_image_processing&app=lab
10. Go to Env_setup and open the Data_download notebook and execute it (this takes some time)
11. You should be all set !

