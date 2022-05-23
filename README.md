# <left><img width="80" src="images/PSA_logo.png"></left> Pressure Swing Adsorption (PSA) project

The PSA application was developed by Mário H. Moura-Neto and Mateus F. Monteiro, both chemical engineering doctoral students of the Federal University of Rio Grande do Norte ([PPGEQ/UFRN](https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?id=106)). The project was supervised by Prof. Dr. [Ivanovitch M. D. Silva](https://github.com/ivanovitchm) ([PPgEEC/UFRN](https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?id=103)) along the Machine Learning course.
We'll be looking at the efficiency of Nitrogen (N<sub>2</sub>) separation from a CH<sub>4</sub>-N<sub>2</sub> feed stream by a distillation column. Twelve parameters were monitored in order to determine their influence on N<sub>2</sub> separation.

<p align="center"><strong> Simplified schematics of a PSA unit. </strong></p>
<p align="center"> <img width="600" src="images/PSA_unit.png"> </p>

From: [Parker Balston](https://www.parker.com)

:small_blue_diamond: **PSA parameters (input):**
| Name of the parameter | Variable name in the code and in the Heroku's .json input | Default value | Limits | 
| ------ | ------ | ------ | ------ |
| Adsorption pressure (bar) | Adsorp_pres | 5.2 | [4,6] | 
| Co-current blowdown pressure (bar) | CoCur_BlowPres | 4.5 | [4,6] | 
| Counter-current blowdown pressure (bar) | CountCur_pres | 0.13 | [0.1,0.2] | 
| Adsorption time (s) | Adsorp_time | 53.5 | [20,60] | 
| Co-current desorption time (s) | CoCur_desorp_time | 30.5 | [10,50] | 
| Counter-current desorption time (s) | CountCur_desorp_time | 33.0 | [10,50] | 
| Compression time (s) | Compres_time | 21.9 | [20,30] | 
| Volumetric flow (m<sup>3</sup>·s<sup>-1</sup>) | Vol_flow | 0.001 | [0.001, 0.003] | 
| Temperature (K) | Temp | 296.3 | [273,323] | 
| Column length (m) | Col_length | 1.3 | [1,3] | 
| Column diameter (m) | Col_diam | 0.26 | [0.1,0.3] | 
| Feed nitrogen mole fraction | Feed_N2_mf | 0.76 | [0.1,0.9] | 

:small_orange_diamond: **PSA parameter (output):**

| Name of the parameter | Variable name in the code and in the Heroku's .json input | Limits | 
| ------ | ------ | ------ |
| N<sub>2</sub> mole fraction in the purified stream | PurStream_N2_mf | [0,1] | 

## :computer: Development

This application was developed and published online regarding the following tools:
- [Google Colaboratory](https://colab.research.google.com)
- [Conda](https://docs.conda.io/en/latest/) 
- [FastAPI](https://fastapi.tiangolo.com/)
- [Jupyter Notebook](https://jupyter.org/)
- [Weights & Biases](https://wandb.ai/site)
- [Github](https://github.com/)
- [Heroku](https://www.heroku.com/)

## :rotating_light: Attention
- The application shall be used whithin the studied parameter's limits.
- The obtained calculation results should be interpreted with the adequate care and analysis.   

## :grey_exclamation: Important Material

| Material | Hyperlink |
| ------ | ------ |
| Database publisher | [Paper, Sant'Anna et al. (2017)](https://www.sciencedirect.com/science/article/abs/pii/S0098135417302053) |
| Web Application | [Online App](https://n2-purity-app.herokuapp.com/docs) |


## :bookmark_tabs: License

GNU General Public License v3.0 - [Legal](https://www.gnu.org/licenses/gpl-3.0.html)

**Feel free to test and use the application!**

[//]: # (If desired to use multiple references along the markdown file, the links used in the body of the note can be substituted by keywords, then the links get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. For example:)
   [repo]: <https://github.comr>
