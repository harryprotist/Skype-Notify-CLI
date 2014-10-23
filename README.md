#SkypeNotifyCLI
=================
A simple command line client to check unread Skype notifications and online friends.

##Usage
###Server
To launch the server, just run: `./skypenotify-server.py <PORT (optional)>`
You can run this in the background by appending an `&`.
###Client
To run the client, run: `./skypenotify.py <unread,online,exit,clear> <PORT (optional)>`.
 * "unread" returns the unread count.
 * "online" returns a list of your online contacts' display names.
 * "exit" kills the server
 * "clear" clears your unread messages
