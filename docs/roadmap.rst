=======
Roadmap
=======

This is the general plan for how this project will be built out.

- Define the structure and behavior of the application **(Done)**
- Get a command line version of the game working to implement the game logic.

    - Write the game code **(In Progress)**
    - Define a JSON schema for sending messages about the game state
    - Implement a rough framework for interpreting the JSON schema and printing to the terminal

- Display the game state in a browser

    - Add a web server that sends out the game state
    - Write a basic Javascript client to interpret and display the game state

- Add interactivity to the browser client (the entire game is played in a single browser)

    - Define a JSON schema for sending player choices to the server
    - Write the web server code for two-way communication with a single client using websockets

- Allow each player to connect from a different device
- Add user management (persistent usernames, passwords, etc)
- Make browser interface not ugly
