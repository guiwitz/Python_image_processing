1. Install miniconda on your system following these instructions: https://conda.io/docs/user-guide/install/index.html
2. Clone or download this repository: https://github.com/guiwitz/Python_image_processing
3. cd (your location)/Python_image_processing/Env_setup 
4. Exectute the install scritpt:
    ```
    ./local_install.bsh
    ```
5. Only if above doesn't work:
    ```
    chmod u+x local_install.bsh
    ```
6. Activate the conda environement:
    ```
    source activate pyimageprocessing
    ```
7. Start a jupyterlab session:
    ```
    jupyter lab
    ```
8. Open the Data_setup_local.ipynb notebook and execute all cells
9. Now you can close everything and stop Jupyterlab (Ctrl+C in the Terminal)

Now, whenever you want to use the course material:
1. Open the Terminal
2. Activate the conda environement:
    ```
    source activate pyimageprocessing
    ```
3. Start Jupyter notebook or Jupyterlab:
    ```
    jupyter notebook
    Jupyter lab
    ```
4. Navigate to course material and execute notebooks