#  Python Socket Chat Application
  

##  Description

This chat app allows users to connect to a server and communicate in real-time. Users can choose a nickname, send messages to other users, and receive connection and disconnection notifications. The app uses sockets for network communication and is ideal for learning about network programming in Python.


##  Features

- **Real-time connection**: Users can send and receive messages instantly.

- **Multiple users**: Allows multiple users to connect and chat at the same time.

- **Custom colors**: Each user receives a unique color that is applied to their messages.

- **Connection management**: Handle user connections and disconnections efficiently.

- **Event logging**: Important events are recorded in log files for easy debugging.

  

##  Technologies Used

- **Python**: Primary programming language.

- **Sockets**: For network communication.

- **Threading**: To handle multiple connections simultaneously.

- **Colorama**: To add color to text output on the console.

- **Logging**: To log events and errors.
  

##  How to Run

1. Clone the repository:

```bash
git clone https://github.com/Alexx6MR/ChatGroup
cd ChatGroup
```
2. Create a folder logs at root-level if it does not exist:

```bash
+logs -> new folder
src/
```
3. Create a virtual environment (recommended):

```bash
windows: python -3 -m venv .venv
```
4. Activate the virtual environment:

```bash
Windows: .venv\Scripts\activate
Mac: source venv/bin/activate
```
5. Install the dependencies:

```bash
pip install -r requirements.txt
```
6. Run the server and client (OBS: I recommend doing it on different terminals):

```bash
py src/server.py
py src/client.py
```
