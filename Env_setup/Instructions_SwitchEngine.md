1. Create Ubuntu 18.04 machine on switch engine

2. login using
    
    ```
    ubuntu@ipaddress
    ```
    
    
3. Download the bash script from the github repository:
    
    ```curl -O https://raw.githubusercontent.com/guiwitz/Python_image_processing/master/Env_setup/switch_engine_install.bsh
    ```
    
    
4. Check address using code below and copy it: 

    ```host yourIPaddress
    ```


5. Open the downloaded script (e.g. with vim):

    ```
    vim switch_engine_install.bsh
    ```
     
     
6. On line 18 replace the address yourhub.yourdomain.edu with the address copied in 4.  
   On line 17 repliace your.email.address with your email address  
   On line 14 replace choose_admin_name with your chosen admin name  

7. Make script executable

    ```
    chmod u+x switch_engine_install.bsh
    ```


8. Execute the script:

    ```
    ./switch_engine_install.bsh
    ```


9. Answer yes to all questions

10. Create an nbgitpuller link on this model by replacing the jupyterhub address (https://hubaddress.cloud.switch.ch) with your hub address (see point 4) in : https://hubaddress.cloud.switch.ch/hub/user-redirect/git-pull?repo=https://github.com/guiwitz/Python_image_processing&app=lab

11. Go to Env_setup and open the Data_download notebook and execute it (this takes some time)

12. You should be all set !

