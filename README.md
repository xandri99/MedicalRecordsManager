# MedicalRecordsManager


**To do list:**
---

1. Medical Form

    - [x] Graphic interface.
        - [ ] Fields must still be added according to the template provided.
             - [ ] Solve problems of visualitzation of the patient data in the engine searcher.
    - [x] Saving the data locally.
        - [x] Saved in a .txt following the structure of a DataFrame.
        - [x] Checking if the patinent already exists or if it's a new patient.
            - [x] Solve synchronization problems with the database.
        - [x] Implement a way to update patient records. (It depends on how the database is implemented)
        - [x] Save it to a SQLite database.
            - [x] Merge between database and graphical interface done correctly --> V2.0
    - [ ] Glitches
        - [x] Allow closing the form without closing the program.
        - [x] Resize the entire window without losing usability.
        - [x] Image size as a background.


2. Start Menu.

    - [x] Graphic interface.
    - [x] Functional buttons that link with the other interfaces.
    - [x] Add automatic opening in case of closing the other interfaces.
    - [ ] Option to choose the language


3. Statistics

    - [ ] To be defined.
 
 
4. Synchronization module

    - [X] Push from client to server.
        - [X] Merge new records into main DB.
    - [X] Pull from server to client.
    - [X] Data encryption
    - [x] Exception handling.
    - [x] Connect to GUI.
