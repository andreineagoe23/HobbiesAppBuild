c# Template for ECS639U Group Coursework

GROUP 65 

MEMBERS - TASK DIVISION(everyone add the work you guys were assigned and what you did)

Andrei Neagoe - Was assigned Django Model Design: Custom User Model, database models for hobbies and friend requests, initial database setup. Completed: Everything that was said previously + Profile update logic + Partial Signup + Login System + CSS initial start + Initial User List sorting logic.
Chun Yi Ng - 
Halak Sanjaybhai Pandya - 
Joshua Penhaligon - Was assigned: Django views and endpoints. User profile management APIs. Friend request handling logic. Server-side validation. Backend unit tests. Completed: Django views and endpoints (initial start, this was built upon by groupmates). Partial friend request handling logic. Bug fixes in signup. All backend selenium tests. Video link to show them working. Styling of the webapp. 

<!------------------- END OF SECTION -------------------->

LOGIN DETAILS OF THE ADMIN

Admin 
Email - admin@gmail.com
Password - admin


LOGIN DETAILS OF TEST USERS

1. Chun Brown
Email - chun@gmail.com
Password - Cod6N(

2. Joshua Smith
Email - joshua@gmail.com
Password - J05_hua

3. Halak Rodriguez
Email - halak@gmail.com
Password - h11_luck

4. Andrei Johnson
Email - andrei@gmail.com
Password -  _Dr389

5. Beyonce Cooper
Email - beyonce@gmail.com
Password - B3y_C00p 

6. Allyson Bell
Email - allyson@gmail.com
Password - Ally_N_s0n

<!------------------- END OF SECTION -------------------->

RESOURCES:

SELENIUM TEST VIDEO: https://www.youtube.com/watch?v=zmCv9vd88_g


This template should be used as the starting point for your group coursework in the module ECS639U Web Programming (at Queen Mary University of London). Use Git (github.qmul.ac.uk) to collaborate on the coursework with your group members. Module leader: Paulo Oliva <[p.oliva@qmul.ac.uk](mailto:p.oliva@qmul.ac.uk)>

## Local development

To run this project in your development machine, follow these steps:

1. Create and activate a conda environment

2. Download this repo as a zip and add the files to your own private repo.

3. Install Pyhton dependencies (main folder):

    ```console
    $ pip install -r requirements.txt
    ```

4. Create a development database:

    ```console
    $ python manage.py migrate
    ```

5. Install JavaScript dependencies (from 'frontend' folder):

    ```console
    $ npm install
    ```

6. If everything is alright, you should be able to start the Django development server from the main folder:

    ```console
    $ python manage.py runserver
    ```

7. and the Vue server from the 'frontend' sub-folder:

    ```console
    $ npm run dev
    ```

8. Open your browser and go to http://localhost:5173, you will be greeted with a template page.

## OpenShift deployment

Once your project is ready to be deployed you will need to 'build' the Vue app and place it in Django's static folder.

1. The build command in package.json and the vite.config.ts files have already been modified so that when running 'npm run build' the generated JavaScript and CSS files will be placed in the mainapp static folder, and the index.html file will be placed in the templates folder:

    ```console
    $ npm run build
    ```

2. You should then follow the instruction on QM+ on how to deploy your app on EECS's OpenShift live server.

## License

This code is dedicated to the public domain to the maximum extent permitted by applicable law, pursuant to [CC0](http://creativecommons.org/publicdomain/zero/1.0/).
