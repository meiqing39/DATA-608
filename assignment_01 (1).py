#Q1 Fix all the syntax and logical errors in the given source code 
#add comments to explain your reasoning

# This program gets three test scores and displays their average.  It congratulates the user if the 
# average is a high score. The high score variable holds the value that is considered a high score.

HIGH_SCORE = 95
 
# Get the test scores. 
test1 = int(input('Enter the score for test 1: ')) #add int function around input so input number remains as a integer and not as a string
test2 = int(input('Enter the score for test 2: '))
test3 = int(input('Enter the score for test 3: ')) # Adding a input as the average ask for three test scores
# Calculate the average test score.

average = (test1 + test2 + test3)/3
# Print the average.
print ("The average score is", average)
# If the average is a high score,
# congratulate the user.
if average >= HIGH_SCORE:      # Fix high_score to HIGH_SCORE as that was defined on line 7 and is the correct variable name
    print('Congratulations!')
print('That is a great average!')

#Q2
#The area of a rectangle is the rectangle’s length times its width. Write a program that asks for the length and width of two rectangles and prints to the user the area of both rectangles. 

rectangle1_length= input("Enter length of rectangle 1:")
rectangle1_width = input("Enter width of rectangle 1:")
rectangle2_length= input("Enter length of rectangle 2:")
rectangle2_width = input("Enter width of rectangle 2:")

area1 = float(rectangle1_length)*float(rectangle1_width)
area2= float(rectangle2_length)*float(rectangle2_width)

print("Area of rectangle 1 is", area1, "and Area of rectangle 2 is", area2)


#Q3 
#Ask a user to enter their first name and their age and assign it to the variables name and age. 
name = input("Please enter your first name:")
age=int(input("Please enter your age:"))
#The variable name should be a string and the variable age should be an int.  
print(type(name))
print(type(age))
#Using the variables name and age, print a message to the user stating something along the lines of:
# "Happy birthday, name!  You are age years old today!"
print("Happy birthday, " +name+ "! You are", age, "years old today!")


