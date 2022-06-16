# scacchi-pigri-ma-efficienti
Un progetto per analizzare statistiche scacchistiche ed elaborare strategie di gioco personalizzate



## flusso di elaborazione di un pgn

- **notebooks/parse-pgn.ipynb**
  - apri il file
    - con `open(<filepath>)`
  - parse games in dizionario  
    - con `parse_database(<file>,<n_games>,<ply>)`
    - funzione implementata in **src/parsepgn.py**
  - enrich data in dizionario
    - con `enrich_database(<file>,<dizionario>,<n_more_games>,<ply>)`
    - funzione implementata in **src/parsepgn.py**
  - salva dizionario
    - con `%store` magic
    - naming convention: *data_nicknameFile_nGames_ply_nMoreGames*





## come aprire preview markdown on vscode

(Forse con qualche plugin, non ricordo)

- `ctrl shift p` per aprire Command Palette,
- then select `Markdown preview`

shortcut:
- `ctrl shift v`









## come aprire un Jupyter notebook

**Assumptions

First, I assume that you have Jupyter and Python installed (e.g. through Anaconda etc). 
Next, I assume that the Jupyther notebook file .ipynb is saved on your computer. 


**From terminal**

On a terminal, navigate to the folder that contains the jupyter notebook file
Type ``jupyter notebook <namefile>``  
Press ``Enter``  

**Alternative 1**

On a terminal, navigate to the folder that contains the jupyter notebook file
Type ``jupyter notebook`` 
You should now see the name of your file in the Jupyter navigation screen
Select and open the .jpynb file with ``left click``

**Alternative 2** 

Open Jupyter in any way (either from terminal with the command ``jupyter notebook`` or through the OS search bar or through Anaconda, or any other way)  
Navigate in the Jupyter navigation screen, to the folder containing the file
Select and open the .jpynb file

## Issues

Come mai ho cominciato a scrivere in inglese?
