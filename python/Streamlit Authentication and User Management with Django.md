Streamlit Authentication and User Management with Django — Part 2
https://medium.com/@data.dev.backyard/streamlit-authentication-and-user-management-with-django-part-2-fe6eed32ebf

Introduction
This tutorial is the continuation of the part 1 tutorial on how to create a login, register, and log-out functionality for a Streamlit client with the help of Django. In the first tutorial, installing the required libraries, creating a boilerplate Streamlit application as well as the initial setup for the Django application including changes in models, settings, and URL files are shown.

Part 2 of this tutorial is dedicated to completing the Streamlit client as well as the Django application to reach a working application like the following:


Demo of the final application
I publish every week technical articles in this channel, so please follow me, and subscribe to my channel. Please check my other articles from my listings related to Spark and Scala, Streamlit, React, Django, AWS, Startup, Cheatsheets and miscellaneous development topics.


Photo by Antonio Batinić: https://www.pexels.com/photo/black-screen-with-code-4164418/
Note: You need to first follow part 1 of this tutorial before reading part 2.

Streamlit Authentication Functions
On the Streamlit side, a dropdown menu is used for choosing to log in, register, and log out functionality. Token-based authentication is utilized to manage a user. After receiving the right username and password information, Django sends a token to the Stremalit application for the user to log in.

Login function
The login function has the job to check if the user is authenticated to see the content or not. If the token exists, then it should be possible for the user to see the provided content. The first if statement determines if the token exists or not and if it exists, then you can fill the block with the content which you want to show to the user. Otherwise, the user needs to log in i.e., send an email and password and click a submit button.

def login_page(applicant_token):
    if(applicant_token):

        st.write("the user is logged in!")

        st.write("login content and logic comes here")

        

    else:
        with st.form("my_form"):



            
            email = st.text_input(label ='email')

            password = st.text_input(label ='password', type="password")

            submit_res = st.form_submit_button(label='Login')

            if submit_res:

                st.write("login clicked!")

                

                headers = {"Content-Type": "application/json; charset=utf-8"}
                response = requests.post('http://127.0.0.1:8000/api/accounts/api_auth/',
                  headers=headers, json={"email":email,"password":password})

                response_json = response.json()

                if response.status_code == 200:
                    
                    applicant_token = response_json["token"]

                    if applicant_token:
                       
                       st.session_state.key = 'applicant-token'
                       st.session_state['applicant-token'] = applicant_token
                       st.experimental_rerun()
Let me break down the code slightly to explain it further. In case of not having a token, the user should submit an email and password to log in through the following code:

with st.form("my_form"):
            
            email = st.text_input(label ='email')

            password = st.text_input(label ='password', type="password")

            submit_res = st.form_submit_button(label='Login')
which corresponds to the following form:


User does not have the token
After entering the credentials and submitting the login button, the following code snippet handles the submission:

if submit_res:

                st.write("login clicked!")
                headers = {"Content-Type": "application/json; charset=utf-8"}
                response = requests.post('http://127.0.0.1:8000/api/accounts/api_auth/',
                  headers=headers, json={"email":email,"password":password})
The above function uses the requests library to send a post request of type “application/json” to the service at address ‘http://127.0.0.1:8000/api/accounts/api_auth/'. Django service is supposed to be running on the localhost i.e., http://127.0.0.1:8000. Requests with the prefix ‘/api/accounts/’ are forwarded to the accounts application in the Django project. In the accounts application, ‘api_auth’ has a view for checking the user credentials and returning a token. For now, you can imagine that the Django service (or any other possible authentication service) will have the duty of sending a token to Streamlit. Below, you can find the corresponding URL patterns in the accounts application of Django.


api_auth runs the api_getToken view
Now, let us have a look at the response code snippet:

response_json = response.json()

if response.status_code == 200:
    applicant_token = response_json["token"]

    if applicant_token:
       st.session_state.key = 'applicant-token'
       st.session_state['applicant-token'] = applicant_token
       st.experimental_rerun()
First, the response is converted to a JSON (). Next, if the status code is 200 which means everything went alright then we get the token from the response_json object. After receiving the token, it is saved in Streamlit’s session state by st.session_state dictionary. After receiving the token, it is required to reload the application to show the legitimate view to the user. As such, st.experimental_rerun() can help us with that. st.experimental_rerun() will rerun the Streamlit code.

Register Function
The user of the Streamlit application should have the functionality to send a username and a password to the Django backend for registration. Django can use its internal mechanism i.e., alluath and SQLite to safely store the user credentials.

Let us have a look a the Streamlit code for registration:

def register(applicant_token):

    if applicant_token:

        with st.form("my_form"):

                    st.write("You need to first logout before registering!")

                    submit_res = st.form_submit_button(label='Logout here') 
            
                    if submit_res:

                        st.write("You are now logged out!")
                        del st.session_state['applicant-token']
                        time.sleep(3)


                        
                        st.experimental_rerun()

    else:

        with st.form("my_form"):



            
            email = st.text_input(label ='email')

            username = st.text_input(label='username')

            password = st.text_input(label ='password', type="password")

            submit_res = st.form_submit_button(label='Register')

            if submit_res:
    
                st.write("registered clicked!")

                headers = {"Content-Type": "application/json; charset=utf-8"}
                response = requests.post('http://127.0.0.1:8000/api/accounts/api_register/',
                  headers=headers, json={"email":email, "username": username,"password":password})

                if response.status_code == 200:
                    st.experimental_rerun()
The piece of code may seem daunting; however, the logic is pretty straightforward. The first part, the case in which a user token exists, logs out and deletes the user token from the session state; afterward, it would possible to register a user. That is kind of a pre-check before continuing with the user registration. In other words, first, the following view is shown to the user:


First logging out
Logging out is kind of equivalent to the deletion of the token from the Streamlit session state. After removing the token from the session state, the following piece of code which is a form is responsible for getting the email, username, and password:

with st.form("my_form"):

            
    email = st.text_input(label ='email')

    username = st.text_input(label='username')

    password = st.text_input(label ='password', type="password")

    submit_res = st.form_submit_button(label='Register')

The above form is the equivalent of the following screen:


Register form
If the register button is clicked, then the following code snippet handles sending the entered information to the Django backend:

if submit_res:
    
      st.write("registered clicked!")

      headers = {"Content-Type": "application/json; charset=utf-8"}
      response = requests.post('http://127.0.0.1:8000/api/accounts/api_register/',
        headers=headers, json={"email":email, "username": username,"password":password})

      if response.status_code == 200:
          st.experimental_rerun()
In the above, a POST request is sent to the Django running at port 8000 on the localhost, and it hits the URL of the accounts service i.e., “/api/accounts/”. Afterward, it hits the “api_register” URL and the corresponding view will be executed.

Log out function
We already saw the logic of the log-out function in some parts of the register function. The log-out function looks like the following:

def log_out(applicant_token):
    
    if applicant_token:
        
             with st.form("my_form"):

                st.write("Do you want to log out?")

                submit_res = st.form_submit_button(label='Logout here') 
        
                if submit_res:

                    if 'applicant-token' in st.session_state:
                        del st.session_state['applicant-token']
                    st.write("You are now logged out!")
The logout function shows a log-out button. When the log-out button is clicked, the token is removed from the session state and a message is printed on the screen. Below is an initial screenshot of the log-out view:


Logout view before submitting the log out button
Main.py function — Streamlit Code
As for the reference, below one can find all the code — explained in previous sections — related to the Streamlit application:

import streamlit as st 
import requests 
import time 


def login_page(applicant_token):
    if(applicant_token):

        st.write("the user is logged in!")

        st.write("login content and logic comes here")

        

    else:
        with st.form("my_form"):



            
            email = st.text_input(label ='email')

            password = st.text_input(label ='password', type="password")

            submit_res = st.form_submit_button(label='Login')

            if submit_res:

                st.write("login clicked!")

                

                headers = {"Content-Type": "application/json; charset=utf-8"}
                response = requests.post('http://127.0.0.1:8000/api/accounts/api_auth/',
                  headers=headers, json={"email":email,"password":password})

                response_json = response.json()

                if response.status_code == 200:
                    
                    applicant_token = response_json["token"]

                    if applicant_token:
                       
                       st.session_state.key = 'applicant-token'
                       st.session_state['applicant-token'] = applicant_token
                       st.experimental_rerun()

def register(applicant_token):

    if applicant_token:

        with st.form("my_form"):

                    st.write("You need to first logout before registering!")

                    submit_res = st.form_submit_button(label='Logout here') 
            
                    if submit_res:

                        st.write("You are now logged out!")
                        del st.session_state['applicant-token']
                        time.sleep(3)


                        
                        st.experimental_rerun()

    else:

        with st.form("my_form"):



            
            email = st.text_input(label ='email')

            username = st.text_input(label='username')

            password = st.text_input(label ='password', type="password")

            submit_res = st.form_submit_button(label='Register')

            if submit_res:
    
                st.write("registered clicked!")

                headers = {"Content-Type": "application/json; charset=utf-8"}
                response = requests.post('http://127.0.0.1:8000/api/accounts/api_register/',
                  headers=headers, json={"email":email, "username": username,"password":password})

                if response.status_code == 200:
                    st.experimental_rerun()



def log_out(applicant_token):
    
    if applicant_token:
        
             with st.form("my_form"):

                st.write("Do you want to log out?")

                submit_res = st.form_submit_button(label='Logout here') 
        
                if submit_res:

                    if 'applicant-token' in st.session_state:
                        del st.session_state['applicant-token']
                    st.write("You are now logged out!")
                    #st.experimental_rerun()

                    

    else:

        st.write("You are now logged out!")

        

       

def load_view():

    add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Login", "Register","Log out")
    )


    applicant_token =''


    if 'applicant-token' in st.session_state:
        
        applicant_token = st.session_state['applicant-token']


    if add_selectbox == 'Login':
        
        login_page(applicant_token=applicant_token) 

    elif add_selectbox == 'Register':

        register(applicant_token=applicant_token)

    elif add_selectbox == 'Log out':

        log_out(applicant_token=applicant_token)


if __name__ == '__main__':
    load_view()
Django Backend
In part 1 of this tutorial, it is shown how to enrich a Django service with an application responsible for accounts i.e., accounts application, create a custom user model, and prepare the URLs for directing the requests to the Django application. So, I highly recommend checking part 1 of this tutorial.

In the following, the api_auth and the api_register views are explained:

api_getToken view
Let us first have a look at the api_getToken view which is responsible for checking the user credentials and generating tokens:

@api_view(('POST',))
@permission_classes([AllowAny])
def api_getToken(request, *args, **kwargs):

    email = request.data['email']
    password = request.data.get("password")

    if email is None or password is None:
        return JsonResponse({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
    if not email:
        return JsonResponse({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
    userobject = User.objects.filter(email=email)

    user = userobject[0]


    print("userobject", userobject)
    print("user", user)

    if(userobject):
        token, created = Token.objects.get_or_create(
            user=userobject[0])  # Create token for the user

        if(user.check_password(password)):
            print("I am coming from second if")
            return JsonResponse({'status': 'ok', 'token': token.key}, status=HTTP_200_OK)
        else:
            return JsonResponse({'status': 'fail', 'token': ''}, status=HTTP_400_BAD_REQUEST)
    else:

        return JsonResponse({'status': 'fail', 'response': 'user could not be found!'})
Let me breakdown the function to have a better understanding of the details:

@api_view(('POST',))
@permission_classes([AllowAny])
def api_getToken(request, *args, **kwargs):

    email = request.data['email']
    password = request.data.get("password")

    if email is None or password is None:
        return JsonResponse({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
    if not email:
        return JsonResponse({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
    userobject = User.objects.filter(email=email)

    user = userobject[0]
@api_view decorator identifies which type of request to receive; here a POST request. @permission_classes identifies who can reach this view; here AllowAny is specified which means that this API is open to everyone.

Next, email and password are fetched from the request and a few checks are applied with regard to an empty email and password. Next, the userobject corresponding to the email addressed is found using User.objects.filter(email=email). User is the imported object from the models.py.

Afterwards, we get or create a token for the corresponding userobject, and here Django Rest helps us by using the Token object. It is also checked if the received password from the POST request is the same as the one saved in the database. Django provides a function check_password which safely check this process. If everything works fine, the token is sent back to the Streamlit application.

if(userobject):
        token, created = Token.objects.get_or_create(
            user=userobject[0])  # Create token for the user

        if(user.check_password(password)):
            print("I am coming from second if")
            return JsonResponse({'status': 'ok', 'token': token.key}, status=HTTP_200_OK)
        else:
            return JsonResponse({'status': 'fail', 'token': ''}, status=HTTP_400_BAD_REQUEST)
    else:

        return JsonResponse({'status': 'fail', 'response': 'user could not be found!'})
api_register_view
Now, it is time to go through the register view which has the code snippet as follows:

@api_view(('POST',))
@permission_classes([AllowAny])
def api_register_view(request, *args, **kwargs):

    data = request.data

    user = User(email=data['email'], username=data['username'])
    user.set_password(data['password'])

    user.save()
    if user.pk is not None:

        return JsonResponse({'status': 'ok', 'response': 'The account is created!'}, status=HTTP_200_OK)
The api_register_view has the same decorator as the api_auth view. It fetches the email, username, and password from the request. It uses the User object model from the models.py to create a user object. Next, it sets the password by using the set_password function provided by Django. Finally, it saves the model to the SQLite database.

Views.Py — Django Views Code
For the reference for the reader as well as having access to all imports, below you can find all the code related to the views.py file for the api_register_view as well as api_auth views:

from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.http import (JsonResponse)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from .models import User

@api_view(('POST',))
@permission_classes([AllowAny])
def api_getToken(request, *args, **kwargs):

    email = request.data['email']
    password = request.data.get("password")

    if email is None or password is None:
        return JsonResponse({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
    if not email:
        return JsonResponse({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
    userobject = User.objects.filter(email=email)

    user = userobject[0]


    print("userobject", userobject)
    print("user", user)

    if(userobject):
        token, created = Token.objects.get_or_create(
            user=userobject[0])  # Create token for the user

        if(user.check_password(password)):
            print("I am coming from second if")
            return JsonResponse({'status': 'ok', 'token': token.key}, status=HTTP_200_OK)
        else:
            return JsonResponse({'status': 'fail', 'token': ''}, status=HTTP_400_BAD_REQUEST)
    else:

        return JsonResponse({'status': 'fail', 'response': 'user could not be found!'})

@api_view(('POST',))
@permission_classes([AllowAny])
def api_register_view(request, *args, **kwargs):

    data = request.data

    user = User(email=data['email'], username=data['username'])
    user.set_password(data['password'])

    user.save()
    if user.pk is not None:

        return JsonResponse({'status': 'ok', 'response': 'The account is created!'}, status=HTTP_200_OK)
Summary
In part 2 of this tutorial series, the complete code snippet for both the Streamlit and Django applications is explained step by step. Part 2 is the continuation of part 1 for user authentication and management in Streamlit with the help of Django.

Authentication and user management are essential parts of any Web service. As an entrepreneur, R&D developer, researcher, or practitioner, one requires to develop such functionality for his/her service. With the advent of Streamlit, developing a visual prototype of an application is easier than ever; however, creating specific functionalities can still be a headache for a developer as Streamlit is still a novice framework. In parts 1 and part 2 of this tutorial series, authentication and user management are covered.

I have written other tutorials useful for coders developing applications with Streamlit. You can check my other tutorials:

_ Email Form using Python and Streamlit — Sending emails with attachment using best practices
_ Streamlit Download Button: Downloading Zip Files from AWS S3
