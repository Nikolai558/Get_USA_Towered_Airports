import os
import urllib.request
from zipfile import ZipFile
from io import BytesIO



class ToweredAptParse:
    def __init__(self):
        self.userSelectedMonth = None
        self.userSelectedDay = None
        self.userSelectedYear = None

        self.exeDirectory = os.getcwd()
        self.hasAptFile = False
        self.artccDictionary = {}
        self.aptDirectory = os.getcwd()
        self.aptFileName = "APT.TXT"
        self.outputDirectory = os.getcwd()
        self.outputFileName = "Towered_Fields_By_Artcc.txt"

    def getAptTextFile(self):
        aptUrl = f"https://nfdc.faa.gov/webContent/28DaySub/{self.userSelectedYear}-{self.userSelectedMonth}-{self.userSelectedDay}/APT.zip"

        print(f"Downloading APT Text File From:\n\t{aptUrl}")
        aptDownload = urllib.request.urlopen(aptUrl)

        with ZipFile(BytesIO(aptDownload.read())) as aptZipFile:
            for aptFile in aptZipFile.namelist():
                with open(f"{self.aptDirectory}\\{self.aptFileName}", "wb") as output:
                    for line in aptZipFile.open(aptFile).readlines():
                        output.write(line)

        self.hasAptFile = True
        print(f"APT.TXT File Download Complete\n\tLocation: {self.aptDirectory}\\{self.aptFileName}")

    def getToweredAirports(self):
        print(f"Getting all Towered Fields from {self.aptFileName}")

        # responsible artcc index is     674:678
        # airport has tower index is     980:981
        # airport code index is          27:31

        with open(f"{self.aptDirectory}\\{self.aptFileName}", "r", errors='replace') as file:
            airports = file.readlines()

            for airport in airports:
                if airport[0:3] == "APT":
                    if airport[980:981].lower() == "y":
                        if airport[674:678] not in self.artccDictionary.keys():
                            try:
                                self.artccDictionary[airport[674:678]].append(airport[27:31])
                            except KeyError:
                                self.artccDictionary[airport[674:678]] = []
                                self.artccDictionary[airport[674:678]].append(airport[27:31])
                        else:
                            self.artccDictionary[airport[674:678]].append(airport[27:31])
        print(f"Finished getting all Towered Fields from {self.aptFileName}")

    def writeToweredAirports(self):
        print(f"Writing Towered Fields to Text Document\n\tLocation: {self.outputDirectory}\\{self.outputFileName}")
        with open(f"{self.outputDirectory}\\{self.outputFileName}", "w") as output_file:
            for artcc in self.artccDictionary.keys():
                output_file.write(f"{artcc}\n\tTotal Towered Airports: {len(self.artccDictionary[artcc])}\n\t\t{self.artccDictionary[artcc]}\n\n***********\n")
        print("Completed writing towered fields to text document.")

    def validateInput(self, userInput, askAptFile=False, month=False, day=False, year=False):
        if askAptFile:
            validInput = False
            while not validInput:
                askAptFileExists = input("Do you have the FAA APT.txt file?\n\t[Y / N]: ").lower().strip()
                if askAptFileExists == "y" or askAptFileExists == "n":
                    validInput = True
                    if askAptFileExists == "y":
                        self.hasAptFile = True
                    else:
                        self.hasAptFile = False
                else:
                    print(f"'{userInput.lower().strip()}' is not a valid entry, please try again.")

        elif month:
            validInput = False
            while not validInput:

                try:
                    int(userInput)
                    if len(userInput) != 2:
                        print(f"{userInput} is not a valid Month, be sure to use two digits ex: 02 for Feb!")
                        userInput = input("\tMonth: ").strip()
                        validInput = False
                        continue
                    else:
                        validInput = True

                    if int(userInput) > 12 or int(userInput) < 0:
                        print(f"{userInput} is not a valid Month!")
                        userInput = input("\tMonth: ").strip()
                        validInput = False
                        continue
                    else:
                        validInput = True
                except ValueError:
                    print(f"{userInput} is not a valid Month, Be sure you are using only numbers!")
                    userInput = input("\tMonth: ").strip()
                    validInput = False
                    continue

            self.userSelectedMonth = userInput

        elif day:
            validInput = False
            while not validInput:

                try:
                    int(userInput)
                    if len(userInput) != 2:
                        print(f"{userInput} is not a valid Day, be sure to use Two digits ex: 05!")
                        userInput = input("\tDay: ").strip()
                        validInput = False
                        continue
                    else:
                        validInput = True

                    if int(userInput) > 31 or int(userInput) < 0:
                        print(f"{userInput} is not a valid Day!")
                        userInput = input("\tDay: ").strip()
                        validInput = False
                        continue
                    else:
                        validInput = True
                except ValueError:
                    print(f"{userInput} is not a valid Day, Be sure you are using only numbers!")
                    userInput = input("\tDay: ").strip()
                    validInput = False
                    continue

            self.userSelectedDay = userInput

        elif year:

            validInput = False
            while not validInput:

                try:
                    int(userInput)
                    if len(userInput) != 4:
                        print(f"{userInput} is not a valid Year, be sure to use four digits ex: 2020!")
                        userInput = input("\tYear: ").strip()
                        validInput = False
                        continue
                    else:
                        validInput = True

                    if int(userInput) > 9999 or int(userInput) < 1000:
                        print(f"{userInput} is not a valid Year!")
                        userInput = input("\tYear: ").strip()
                        validInput = False
                        continue
                    else:
                        validInput = True
                except ValueError:
                    print(f"{userInput} is not a valid Year, Be sure you are using only numbers!")
                    userInput = input("\tYear: ").strip()
                    validInput = False
                    continue

            self.userSelectedYear = userInput

        else:
            print("Something went wrong, please contact the developer.")


def main():
    # TODO Allow users to change input and output directory

    input("Hello, this program will get all the towered fields for all the ARTCC's listed in the FAA data."
          "\nTo continue press <enter>")
    parse = ToweredAptParse()

    parse.validateInput("", askAptFile=True)

    if not parse.hasAptFile:
        print("That's okay, Please tell me the Airacc Effective Date so I can get it for you:")
        parse.validateInput(input("\tMonth: ").strip(), month=True)
        parse.validateInput(input("\tDay: "), day=True)
        parse.validateInput(input("\tYear: "), year=True)

    print("Awesome, I will start my process now. Standby\n\n\n\n\n\n\n ")

    if not parse.hasAptFile:
        parse.getAptTextFile()
    parse.getToweredAirports()
    parse.writeToweredAirports()

    input("\n\n\n\nCompleted! Press <enter> to exit.")


if __name__ == '__main__':
    main()
