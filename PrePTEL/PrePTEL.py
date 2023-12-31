# Author: Contemelia
# 
# This script is designed for conducting NPTEL mock quiz sessions. Please ensure that you 
# have downloaded the appropriate question material alongside this script. The material is 
# provided in the form of an Excel file, named after the corresponding course. This script is 
# intended to be compatible with similarly structured question materials.




import openpyxl
import os

from random import sample
from subprocess import check_call, CalledProcessError
from sys import exit
from time import sleep




class PrePTEL:
    
    def __init__(self):
        
        self.author = "Contemelia"
        self.appName = "PrePTEL"
        self.appVersion = "1.1c"
        
        if __name__ == '__main__':
            
            self.selectCourse()
            self.loadQuestions()
            self.selectPreference()
            self.askQuestions()
            self.showResults()
            
            input("\n\n\n\nPress enter to exit.")     
    
    
    
    def waterMark(self):
        
        if __name__ == '__main__':
            os.system('cls')
            print(f"Author: {self.author}")
            print(f"Script name: {self.appName}")
            print(f"Script version: {self.appVersion}")
            print("\n\n\n")
    
    
    
    def selectCourse(self):
        
        self.waterMark()
        self.directory = r'./Materials'
        try:
            self.courseList = [course for course in os.listdir(self.directory) if course.endswith('.xlsx')]
        except Exception as error:
            print(f"Error: {error}\nMake sure to include the folder titled 'Materials' within the same directory as the script.")
            sleep(3)
            exit()
        
        if self.courseList:    
            print("Please select a course...")
            for index in range(len(self.courseList)):
                print(f"({index + 1}) {os.path.splitext(self.courseList[index])[0]}")
        else:
            print("You do not have any material for use in a supported format.")
            sleep(3)
            exit()
        
        try:
            preferedCourse = int(input("\nYour choice: "))
            self.preferedCourse = self.courseList[preferedCourse - 1]
        except Exception as error:
            print(f"\nError: {error}\nTry again by selecting a valid index.")
            sleep(3)
            self.selectCourse()
            return
    
    
    
    def loadQuestions(self):
        
        self.workbookPath = self.directory + r'/' + self.preferedCourse
        self.workbook = openpyxl.load_workbook(self.workbookPath)
        self.sheet = self.workbook.active
        
        self.questionBank = []
        for row in self.sheet.iter_rows(values_only = True):
            self.questionBank.append(list(row))
        
        # if len(self.questionBank) != 6:
        #     print(f"\nThe structure of this material is not supported.")
        #     sleep(3)
        #     self.selectCourse()
        #     self.loadQuestions()
        #     return
        
        self.workbook.close()
    
    
    
    def selectPreference(self):
        
        self.waterMark()
        print("Please provide the following details before we start your session...")
        try:
            self.questionCount = int(input("Preferred question count: "))
            if self.questionCount > len(self.questionBank):
                print(f"\nThe maximum number of questions you can have must not exceed {len(self.questionBank)}.")
                sleep(3)
                self.selectPreference()
                return
        except TypeError as error:
            print(f"\nError: {error}\nTry again by providing a number.")
            sleep(3)
            self.selectPreference()
            return
        self.viewScore = input("Would you like to view your score at the end? [Y / N]: ").lower()[0] == 'y'
        self.viewMistakes = input("Would you like to view your mistakes at the end? [Y / N]: ").lower()[0] == 'y'
    
    
    
    def askQuestions(self):
        
        self.wrongAnswers = []
        self.score = 0
        self.questionsToAsk = sample(self.questionBank, self.questionCount)
        choices = ['A', 'B', 'C', 'D']
        
        questionNumber = 1
        for index in range(self.questionCount):
            while True:
                self.waterMark()
                print(f"{questionNumber}. {self.questionsToAsk[index][0]}")
                print("\nPlease select an option...")
                choiceOption = 0
                optionList = []
                choiceIndices = {}
                
                jumbledOption = []
                for option in range(1, 5):
                    jumbledOption.append([self.questionsToAsk[index][option], option])
                jumbledOption = sample(jumbledOption, len(jumbledOption))
                
                for option in jumbledOption:
                    if option[0]:
                        print(f"({choices[choiceOption]}) {option[0]}")
                        choiceIndices[choices[choiceOption]] = option[1]
                        choiceOption += 1
                
                try:
                    choice = input("\nYour choice: ").upper()
                    if choice not in choiceIndices:
                        print("\nChoice error: Please choose a valid option.")
                        sleep(3)
                        continue
                except Exception as error:
                    print("\nChoice error: Please choose a valid option.")
                    sleep(3)
                    continue
                
                if self.questionsToAsk[index][choiceIndices[choice]] == self.questionsToAsk[index][5]:
                    self.score += 1
                else:
                    wrongAnswer = []
                    # for element in self.questionsToAsk[index]:
                    #     wrongAnswer.append(element)
                    wrongAnswer.append(questionNumber)
                    wrongAnswer.append(self.questionsToAsk[index][0])
                    wrongAnswer.append(jumbledOption)
                    wrongAnswer.append(self.questionsToAsk[index][5])
                    wrongAnswer.append(self.questionsToAsk[index][choiceIndices[choice]])
                    self.wrongAnswers.append(wrongAnswer)
                
                questionNumber += 1
                break
    
    
    
    def showResults(self):
        
        self.waterMark()
        
        if self.viewScore:
            print(f"Your score: {self.score} out of {self.questionCount}\n\n")
        
        choices = ['A', 'B', 'C', 'D']
        if self.viewMistakes:
            for wrongAnswer in self.wrongAnswers:
                print(f"{wrongAnswer[0]}. {wrongAnswer[1]}")
                print("\nOption provided were...")
                choiceOption = 0
                choiceIndices = {}
                for option in wrongAnswer[2]:
                    if option[0]:
                        if option[0] == wrongAnswer[4]:
                            wrongIndex = choiceOption
                        elif option[0] == wrongAnswer[3]:
                            correctIndex = choiceOption
                        print(f"({choices[choiceOption]}) {option[0]}")
                        choiceIndices[choices[choiceOption]] = option[1]
                        choiceOption += 1
                print(f"\nYour answer: ({choices[wrongIndex]}) {wrongAnswer[4]}\nCorrect answer: ({choices[correctIndex]}) {wrongAnswer[3]}\n\n")
                





def startUp():
    
    try:
        check_call(['pip', 'install', 'openpyxl'])
        print("openpyxl installed successfully.")
    except CalledProcessError as e:
        print(f"Error installing openpyxl: {e}")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    
    PrePTEL()





if __name__ == '__main__':
    
    try:
        startUp()
    
    except KeyboardInterrupt as error:
        print("Keyboard interrupt encountered. Rerun the script.")
