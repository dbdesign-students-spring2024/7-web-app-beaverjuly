# Social App: Mini Valley
For people who love nature but cannot quit social media to get to know each other.

### Link to Ddeployed Copy on NYU i6:
http://i6.cims.nyu.edu/home/jy3813/public_html/7-web-app-beaverjuly

## Functionality Description

This application includes several routes that manage user sessions, profiles, and interactive content creation. Below is a detailed description of each route:

### Home Route
- **Endpoint:** `/home`
- **Functionality:** 
  - Redirects users to the login page if they are not already logged in (`'username' not in session`).
  - In other words, user cannot post messages or have a profile page unless they log in first.
  - If logged in, the `home.html` template is rendered.

### Login Route
- **Endpoint:** `/login`
- **Method:** `GET`, `POST`
- **Functionality:** 
  - **GET Request:** Displays the login page.
  - **POST Request:** Handles user login attempts. Users can either set a username (`name_myself`) or proceed anonymously (`be_nameless`).
    - If the username does not exist in the database, a new user record is created.
  - Redirects to the user's profile page upon successful login or prompts for login again on failure.

### Logout Route
- **Endpoint:** `/logout`
- **Method:** `POST`
- **Functionality:** 
  - Logs out the user by removing `'username'` from the session.
  - Redirects to the login page.

### Profile Route
- **Endpoint:** `/profile`
- **Functionality:** 
  - Fetches and displays the profile of the logged-in user, including user bio.

### User Profile Route
- **Endpoint:** `/user/<username>`
- **Functionality:** 
  - Displays the profile for the given username.
  - If the user does not exist, flashes a message and redirects to a read page.

### Update Bio Route
- **Endpoint:** `/update_bio`
- **Method:** `POST`
- **Functionality:** 
  - Allows logged-in users to update their bio.
  - Redirects to the user's profile page after the update.

### Delete Bio Route
- **Endpoint:** `/delete_bio`
- **Method:** `POST`
- **Functionality:** 
  - Allows logged-in users to delete their bio, setting it to an empty string.
  - Redirects to the user's profile page after deletion.

### Read Route
- **Endpoint:** `/read`
- **Functionality:** 
  - Displays posts or 'echoes' sorted by creation time, showing the most recent first.

### Create Route
- **Endpoint:** `/create`
- **Method:** `GET`, `POST`
- **Functionality:** 
  - **GET Request:** Displays a form for creating a new post if the user is logged in.
  - **POST Request:** Processes the form to create a new post with the user's input, saves it in the database with a timestamp, and redirects to the read page.

### Edit Route
- **Endpoint:** `/edit/<mongoid>`
- **Method:** `GET`
- **Functionality:**
  - Displays an edit form for a specific post identified by the MongoDB Object ID (`mongoid`).
  - Ensures that only the user who created the post can access the edit form.

### Edit POST Route
- **Endpoint:** `/edit/<mongoid>`
- **Method:** `POST`
- **Functionality:**
  - Updates the specified post with new content submitted through the edit form.
  - Redirects to the read page to display the updated post.

### Delete Route
- **Endpoint:** `/delete/<mongoid>`
- **Method:** `GET`
- **Functionality:**
  - Allows the deletion of a post specified by its MongoDB Object ID (`mongoid`).
  - Ensures that only the user who created the post can delete it.
  - Redirects to the read page after deletion.

  ## Note on Styling
I styled the texts and backgrounds both directly in the html files and in the separate css file; for the purpose of general and more specified styling, respectively.
 
 ## Citations
- The font for the main header can be found on the following link: https://fonts.google.com/selection/embed;
- Photo for the background is downloaded from the following link: https://cdn.wallpapersafari.com/21/19/6WrNXf.jpg

## The above work is completed individually. 