# SecureStorage-HIDS Usage Manual

To get the system up and running, it's essential to have Neo4J Desktop installed, which serves as the project's database. Below is a brief guide on how to install it:

1. **Download the Application:**
   - Visit [Neo4j Download Page](https://neo4j.com/download/).
   - Fill out the form to initiate the download process.

2. **Copy Neo4j Desktop Activation Key:**
   - Copy the Neo4j Desktop Activation Key; you'll need it to activate your Neo4j Desktop account.

3. **Install Neo4j Desktop:**
   - On Windows:
     - After downloading, you'll get a file named "Neo4j Desktop Setup X.Y.Z.exe," where X.Y.Z corresponds to the Neo4j version.
     - Execute the .exe file.
     - Start Neo4j.

   - On Linux:
     - After downloading, you'll get a file named "neo4j-desktop-X.Y.Z-x86_86.AppImage."
     - AppImage packages don't need installation; they run directly.
     - To execute it, give execution permissions to the downloaded file and run it from a terminal:
       ```bash
       chmod a+x neo4j-desktop-X.Y.Z-x86_64.AppImage
       ./neo4j-desktop-X.Y.Z-x86_64.AppImage
       ```

4. **Register the Software:**
   - Enter the key copied earlier to register the software. This can also be done through the menu options.
  
5. **Create DB:**
   - On the GUI pulse on the market bottom and save the password.
  ![image](https://github.com/US-SSII/SecureStorage-HIDS/assets/72869496/e9c59aff-895b-433a-8fc6-934b420cb6db)
   - The password must be also set on the config.ini.
   ![image](https://github.com/US-SSII/SecureStorage-HIDS/assets/72869496/195e22ff-2bb1-4e15-88fd-fa7a7af1acd5)

5. **Install Project Dependencies:**
   - In a terminal, execute the following command to install the project dependencies:
     ```bash
     pip install -r requirements.txt
     ```

6. **Run main.py:**
   - Finally, execute `main.py` located at "src/main/python/main.py." You can do this from a development environment like PyCharm or Visual Studio Code or from the terminal.
   
   - On Windows:
     ```bash
     python main.py
     ```

   - On Linux:
     ```bash
     chmod +x main.py
     ./main.py
     ```

This guide ensures the setup of Neo4j and the project's dependencies, allowing you to run the system seamlessly.
