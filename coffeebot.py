#!/usr/bin/python2.7
import socket
from collections import Counter
# Some basic variables used to configure the bot
server = "irc.freenode.net" # Server
port = 6667
channel = "#zuloo" # Channel
botnick = "coffeebot" # Your bots nick

order = {};

# This is our first function! It will respond to server Pings.
def ping():
  ircsock.send("PONG :pingis\n")

# This is the send message function, it simply sends messages to the channel.
def sendmsg(chan , msg):
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")

# This function is used to join channels.
def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

# This function responds to a user that inputs "Hello Mybot"
def hello():
  ircsock.send("PRIVMSG "+ channel +" :Ready to take your orders!\n")


def commands(message):
  global order
  nick=message.split('!')[0][1:]
  channel=message.split(' PRIVMSG ')[-1].split(' :')[0]
  if ircmsg.find('!order')!=-1:
    order[nick] = message.split('!order ')[-1]
  elif ircmsg.find('!reset')!=-1:
    order = {}
    hello()
  elif ircmsg.find('!bill')!=-1:
    drinks = Counter()
    empty = True
    for v in order.values():
      empty = False
      drinks[v]+=1
    sendmsg(channel,"{nick}: the order:".format(nick=nick))
    if empty:
        sendmsg(channel,"  no drinks ordered")
    for k in drinks:
      sendmsg(channel,"  {value} {key}".format(key=k, value=str(drinks[k]).rjust(3)))
  elif ircmsg.find(botnick+":")!=-1 or ircmsg.find("!help")!=-1:
    sendmsg(channel, "!order drink - order the drink")
    sendmsg(channel, "!bill - show the summed orders")
    sendmsg(channel, "!reset - reset the orders")


# Here we connect to the server using the port 6667
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, port))
# user authentication
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :coffeebot\n")
# here we actually assign the nick to the bot
ircsock.send("NICK "+ botnick +"\n")

# Join the channel using the functions we previously defined
joinchan(channel)

hello()

# Be careful with these! it might send you to an infinite loop
while 1:
  # receive data from the server
  ircmsg = ircsock.recv(2048)
  # removing any unnecessary linebreaks.
  ircmsg = ircmsg.strip('\n\r')
  # Here we print what's coming from the server
  #print(ircmsg)
  if ircmsg.find(' PRIVMSG ')!=-1:
    commands(ircmsg)

  # if the server pings us then we've got to respond!
  if ircmsg.find("PING :") != -1:
    ping()
