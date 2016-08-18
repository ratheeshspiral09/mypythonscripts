# mypythonscripts
Some interesting utility scripts



#file.py 
-----------

This will copy all  files in a particular extension from a folder mentioned to subfolders having not more than a particlualr size inside another folder


try like  :   

python file.py <<source_folder_path>> <<extension>> <<size_in_mb>> <<destination_path>> <<command: copy/move>


Example
---------------------------------------------
"python file.py /home/ratheesh/Desktop/prajeesh/ .mp3 20 /home/ratheesh/Desktop/ copy"




This will copy all mp3 files in folder /home/ratheesh/Desktop/prajeesh/ to subfolders having not more than 20mb in folder /home/ratheesh/Desktop/



#rankbrand.py
-------------------

Installation Instructions
-------------------------------------

(1) Create a VirtualENV
(2) Execute " pip install requests bs4 "
(3) Download and copy the script "scarp.py"  to a folder 
(4) Run   python scrap.py "hair fall shampoo,hair conditioner"


Output
---------------------------------------


{
    "result": [
        {
            "position": {
                "Himalaya": 1,
                "TRESemme": 2,
                "L'Oreal Paris": 3
            },
            "keyword": "hair fall shampoo"
        },
        {
            "position": {
                "Himalaya": 12,
                "TRESemme": 2,
                "L'Oreal Paris": 10
            },
            "keyword": "hair conditioner"
        }
    ]
}
