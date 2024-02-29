"""
Print answers to the following

1. Your name
2. Your program / year
3. What are your academic interests? (research/coursework)
4. What programming languages do you have experience with?
5. What is your experience with Python?  (is is ok to have no experience)
6. What time zone are you in? (Chicago is UTC -5)
7. What is something you would like to learn in this course?
8. Do you have any questions or concerns you would like to share?
"""
a = 'Shiqian Xu'
b = 'Master in Computational and Applied Mathematics / 2025'
c = 'Research: Applying machine learning and mathematical modeling on weather prediction, coursework: pure coding'
d = 'Python, Matlab'
e = 'I took only one basic python class during my undergraduate, one basic python class = no experience'
f = 'UTC -5'
g = 'Data structure, data analysis'
h = 'I prefer to work with someone I know for the project. Also, can you hire my friend who is a computer science student be the TA? Can you use submitty(from Rensselaer Polytechnic Institute) to check our code?'
list_of_questions = [a,b,c,d,e,f,g,h]
for x in range(1,9):
  print('{}. <{}>'.format(x,list_of_questions[x-1]))
