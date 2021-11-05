import logging
from timeit import default_timer as timer
import importlib
import os
from boxsdk import JWTAuth, Client
from boxsdk.network.default_network import DefaultNetwork
from pprint import pformat

# Function to handle uploading files to Box
def uploadToBox(client, folder_id, filename):
    folder = client.folder(folder_id=folder_id)
    items = folder.get_items()
    for item in items:
        if item.name == filename:
            updated_file = client.file(item.id).update_contents(item.name)
            print('Box: File "{0}" has been updated'.format(updated_file.name))
            return
    uploaded_file = folder.upload(filename)
    print('Box: File "{0}" has been uploaded'.format(uploaded_file.name))


# Runs all state scripts that are currently available
if __name__ == '__main__':
    # disabledStates = ["arizona", "virginia"]
    #logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)
    # Currently working states <-- ADD STATES BELOW
    currentStates = ["alabama", "illinois", "south_carolina",
                     "tennessee", "north_carolina", "rhode_island",
                     "louisiana"]

    # Run with Box integration flag (defaults to True)
    useBox = True


    if useBox:
        try:
            auth = JWTAuth.from_settings_file('jwt_auth.json')
            client = Client(auth)
        except Exception as e:
            print("Error creating Box client: %s" % e)
    else:
        print("Box integration disabled.")

    # Set-up necessary subdirectories
    for localFolder in ["temp", "out"]:
        if not os.path.isdir(localFolder):
            try:
                os.mkdir(localFolder)
            except OSError:
                #logging.error("Failed to create directory %s", localFolder, exc_info=False)

    # Import module for each state script
    modules = {}
    for state in currentStates:
        try:
            modules[state] = importlib.import_module(state)
            #logging.info("Successfully Imported %s", state, exc_info=False)
        except ImportError:
            #logging.error("Failed to import %s", state, exc_info=True)

    # Lists to store scripts that either fail or succeed in running
    successes = []
    failures = []

    startTimer = timer()  # Begin timer

    # Run scripts for each working state, catch and denote failures
    for state in currentStates:
        try:
            exec("modules['{stateName}'].main()".format(stateName=state))
            successes.append(state)
            #logging.info("Successfully Fetched %s", state, exc_info=False)
        except Exception:
            #logging.error("Failed to fetch %s", state, exc_info=True)
            failures.append(state)

    endTimer = timer()  # End timer
    elapsed = endTimer - startTimer  # Calculate elapsed time to fetch state data

    if useBox:
        # Upload to Box
        outputDir = 'out'
        uploadSuccess = True
        for outFile in os.listdir(outputDir):
            outFilePath = os.path.join(outputDir, outFile)
            rootBoxFolder = '135929332730'
            try:
                if os.path.isfile(outFilePath) and client:
                    uploadToBox(client, rootBoxFolder, outFilePath)
                else:
                    uploadSuccess = False
                    print("Error uploading file to Box: " + outFile)
            except Exception as e:
                uploadSuccess = False
                print("Upload failed: %s" % e)

        # Clear output folder
        if uploadSuccess:
            deleteSuccess = True
            for outFile in os.listdir(outputDir):
                outFilePath = os.path.join(outputDir, outFile)
                try:
                    if os.path.isfile(outFilePath) or os.path.islink(outFilePath):
                        os.unlink(outFilePath)
                except Exception as e:
                    deleteSuccess = False
                    print("Failed to delete %s. Exception: %s" % (outFile, e))
            if deleteSuccess:
                print("Successfully cleared output folder.")

    # Print results
    #logging.info("Fetched data for " + str(successes) + " in " + str(elapsed) + " seconds.", exc_info=False)
    #logging.info("Failed to fetch: " + str(failures), exc_info=False)
